#! /usr/bin/env python
#coding=utf-8
"""
Skript zur Indexierung der Germania Sacra Daten.
Liest die Daten aus MySQL,
denormalisiert sie in Solr Dokumente
und spielt sie in Solr Index(e).

2013 Sven-S. Porst, SUB Göttingen <porst@sub.uni-goettingen.de>
"""

import copy
import pprint
import urllib
import json
import xml.etree.ElementTree
import os

# benötigt das Modul python-geohash
import geohash
# benötigt das Modul solrpy
import solr
# benötigt das Modul mysql.connector
import mysql.connector

mysql_username = 'germaniasacra'
mysql_host = '127.0.0.1'
mysql_password = 'germaniasacra'
mysql_db = 'mydb'

db = mysql.connector.connect(user=mysql_username, host=mysql_host, password=mysql_password, database=mysql_db)
db2 = mysql.connector.connect(user=mysql_username, host=mysql_host, password=mysql_password, database=mysql_db)
db3 = mysql.connector.connect(user=mysql_username, host=mysql_host, password=mysql_password, database=mysql_db)
cursor = db.cursor()
cursor2 = db2.cursor()
cursor3 = db3.cursor()


# Informationen aus der Personendatenbank als JSON laden und lesen
personenURL = 'http://personendatenbank.germania-sacra.de/export/export.json'
personenPath = '../Personendatenbank/export.json'
urllib.urlretrieve(personenURL, personenPath)
os.system("json_pp < " + personenPath + " > ../Personendatenbank/export-pp.json ")
jsonFile = open(personenPath)
personen = json.load(jsonFile)
jsonFile.close()


distantPast = -10000
minYear = 700
maxYear = 1810
distantFuture = 10000
yearStep = 10


def addValueForKeyToDict (value, key, myDict):
	if not myDict.has_key(key):
		myDict[key] = []
	insertValue = value
	if value == None:
		insertValue = ''
	myDict[key] += [value]


def mergeDocIntoDoc (new, target):
	for key in new.keys():
		value = new[key]
		if type(value) == list:
			for item in value:
				addValueForKeyToDict(item, key, target)
		else:
			addValueForKeyToDict(value, key, target)


def improveZeitraumVerbalForDocument (doc, prefix):
	if not doc[prefix + "_verbal"]:
		if doc[prefix + "_von"]:
			if doc[prefix + "_von"] != distantPast and doc[prefix + "_von"] != distantFuture:
				doc[prefix + "_verbal"] = str(doc[prefix + "_von"])

		if doc[prefix + "_bis"]:
			if doc[prefix + "_bis"] != distantPast and doc[prefix + "_bis"] != distantFuture:
				if doc[prefix + "_von"] != doc[prefix + "_bis"]:
					doc[prefix + "_verbal"] += '/' +  str(doc[prefix + "_bis"])



def improveZeitraumForDocument (doc, prefix):
	if doc[prefix + "_von_von"]:
		if not doc[prefix + "_von_bis"]:
			doc[prefix + "_von_bis"] = doc[prefix + "_von_von"]
	else:
		doc[prefix + "_von_von"] = distantPast
		if not doc[prefix + "_von_bis"]:
			doc[prefix + "_von_bis"] = distantPast
		else:
			print "Warnung: von_bis ohne von_von " + str(doc)
	von = int(doc[prefix + "_von_von"])
	improveZeitraumVerbalForDocument(doc, prefix + "_von")
	
	if doc[prefix + "_bis_von"]:
		if not doc[prefix + "_bis_bis"]:
			doc[prefix + "_bis_bis"] = doc[prefix + "_bis_von"]
	else:
		if doc[prefix + "_bis_bis"]:
			doc[prefix + "_bis_von"] = von
		else:
			doc[prefix + "_bis_von"] = distantPast
			doc[prefix + "_bis_bis"] = distantFuture
	bis = int(doc[prefix + "_bis_bis"])
	improveZeitraumVerbalForDocument(doc, prefix + "_bis")
	
	# Jahr 50
	jahr50 = {}
	start = minYear
	while start < maxYear:
		if von < (start + yearStep) and start <= bis:
			jahr50[start] = True
		start += yearStep
	doc[prefix + "_jahr50"] = jahr50.keys()
	if not doc.has_key("jahr50"):
		doc["jahr50"] = []
	for j in jahr50:
		if not j in doc["jahr50"]:
			doc["jahr50"] += [j]
	

docs = []


# kloster
queryKloster = """
SELECT
	kloster.uid AS sql_uid, kloster.kloster_id as kloster_id, kloster.kloster,
	kloster.patrozinium, kloster.bemerkung AS bemerkung_kloster,
	kloster.text_gs_band, kloster.band_uid AS band_id, kloster.band_seite,
	band.nummer AS band_nummer, band.titel AS band_titel,
	band.kurztitel AS band_kurztitel, band.sortierung AS band_sortierung,
	tx_germaniasacra_domain_model_bearbeitungsstatus.name as bearbeitungsstatus,
	tx_germaniasacra_domain_model_personallistenstatus.name as personallistenstatus
FROM 
	tx_germaniasacra_domain_model_kloster AS kloster,
	tx_germaniasacra_domain_model_band AS band,
	tx_germaniasacra_domain_model_bearbeitungsstatus,
	tx_germaniasacra_domain_model_personallistenstatus
WHERE
	(band.uid = kloster.band_uid OR (kloster.band_uid IS NULL AND band.uid = 1)) AND
	tx_germaniasacra_domain_model_bearbeitungsstatus.uid = kloster.bearbeitungsstatus_uid AND
	tx_germaniasacra_domain_model_personallistenstatus.uid = kloster.personallistenstatus_uid
ORDER BY
	sql_uid
"""
cursor.execute(queryKloster)
for values in cursor:
	standorte = []
	orden = []
	
	docKloster = dict(zip(cursor.column_names, values))
	if not docKloster["band_id"]:
		del docKloster["band_id"]
		del docKloster["band_nummer"]
		del docKloster["band_titel"]
		del docKloster["band_kurztitel"]
		del docKloster["band_sortierung"]
	else:
		bandSortName = ('%04d' % docKloster["band_sortierung"]) + '####' + docKloster["band_nummer"] + ' ' + docKloster["band_kurztitel"]
		docKloster["band_facet"] = [bandSortName, "hat_band"]

	docKloster["typ"] = "kloster"
	docKloster["id"] = str(docKloster["kloster_id"])
	docKloster["url"] = []
	docKloster["url_bemerkung"] = []
	docKloster["url_typ"] = []
	docKloster["url_relation"] = []
	docKloster["url_wikipedia"] = []
	docKloster["url_quelle"] = []
	docKloster["url_quelle_titel"] = []
	docKloster["gnd"] = []

	queryBandURL = """
	SELECT
		url.url, url.bemerkung,
		url_typ.name AS url_typ
	FROM
		tx_germaniasacra_domain_model_url AS url,
		tx_germaniasacra_domain_model_url_typ AS url_typ,
		tx_germaniasacra_band_url_mm AS relation		
	WHERE
		url.url_typ_uid = url_typ.uid AND
		relation.uid_local = %s AND
		url.uid = relation.uid_foreign
	"""
	if docKloster.has_key("band_id"):
		cursor2.execute(queryBandURL, [str(docKloster["band_id"])])
		docURLs = {}
		for values2 in cursor2:
			docURL = dict(zip(cursor2.column_names, values2))
			docURLs[docURL["url_typ"]] = docURL["url"]

		if docURLs.has_key('Handle'):
			docKloster['band_url'] = [docURLs['Handle']]
		else:
			docKloster['band_url'] = ['']
		if docURLs.has_key('Dokument'):
			docKloster['band_url'] = [docURLs['Dokument']]
		if docURLs.has_key('Findpage'):
			docKloster['band_url_seitengenau'] = [docURLs['Findpage']]
		else:
			docKloster['band_url_seitengenau'] = ['']

	queryKlosterURL = """
	SELECT
		url.url, url.bemerkung,
		url_typ.name AS url_typ
	FROM
		tx_germaniasacra_domain_model_url AS url,
		tx_germaniasacra_domain_model_url_typ AS url_typ,
		tx_germaniasacra_kloster_url_mm AS relation
	WHERE
		url.url_typ_uid = url_typ.uid AND
		url.uid = relation.uid_foreign AND
		relation.uid_local = %s
	"""
	cursor2.execute(queryKlosterURL, [str(docKloster["sql_uid"])])
	for values2 in cursor2:
		docURL = dict(zip(cursor2.column_names, values2))
		
		if docURL["url_typ"] == "Wikipedia":
			docKloster["url_wikipedia"] += [docURL["url"]]
		elif docURL["url_typ"] == "Quelle":
			docKloster["url_quelle"] += [docURL["url"]]
			docKloster["url_quelle_titel"] += [docURL["bemerkung"]]
		else:
			docKloster["url"] += [docURL["url"]]
			docKloster["url_bemerkung"] += [docURL["bemerkung"]]
			docKloster["url_typ"] += [docURL["url_typ"]]
			docKloster["url_relation"] += ["kloster"]
		
		if docURL["url_typ"] == "GND":
			components = docURL["url"].split("/gnd/")
			if len(components) > 1:
				docKloster["gnd"] += [components[1]]
			else:
				print "keine GND URL: " + docURL["url"]

	queryLiteratur = """
	SELECT 
		literatur.uid, literatur.citekey, literatur.beschreibung
	FROM
		tx_germaniasacra_domain_model_literatur AS literatur,
		tx_germaniasacra_kloster_literatur_mm AS relation
	WHERE
		relation.uid_local = %s AND
		relation.uid_foreign = literatur.uid
	ORDER BY
		literatur.citekey ASC
	"""
	literaturDict = {}
	literaturCitekeys = []
	cursor2.execute(queryLiteratur, [str(docKloster["sql_uid"])])
	for values2 in cursor2:
		docLiteratur = dict(zip(cursor2.column_names, values2))
		if literaturDict.has_key(docLiteratur["citekey"]):
			literaturDict[docLiteratur["citekey"]] += ' / ' + docLiteratur["beschreibung"]
		else:
			literaturDict[docLiteratur["citekey"]] = docLiteratur["beschreibung"]
	
	docKloster["literatur_citekey"] = sorted(literaturDict.keys())
	docKloster["literatur_beschreibung"] = []
	for citekey in docKloster["literatur_citekey"]:
		docKloster["literatur_beschreibung"] += [literaturDict[citekey]]

	docKlosterBasic = copy.deepcopy(docKloster)

	
	queryStandort = """
	SELECT
		standort.uid AS standort_uid, standort.gruender,
		standort.breite AS standort_breite, standort.laenge AS standort_laenge,
		ort.uid AS ort_uid, ort.ort, ort.gemeinde, ort.kreis, ort.bistum_uid AS bistum_uid, ort.wuestung, ort.breite AS ort_breite, ort.laenge AS ort_laenge,
		land.land, land.ist_in_deutschland,
		zeitraum.uid AS zeitraum_uid,
		zeitraum.von_von AS standort_von_von, zeitraum.von_bis AS standort_von_bis, zeitraum.von_verbal AS standort_von_verbal,
		zeitraum.bis_von AS standort_bis_von, zeitraum.bis_bis AS standort_bis_bis, zeitraum.bis_verbal AS standort_bis_verbal,
		bistum.bistum, bistum.kirchenprovinz, bistum.ist_erzbistum
	FROM 
		tx_germaniasacra_domain_model_kloster_standort AS standort,
		tx_germaniasacra_domain_model_ort AS ort,
		tx_germaniasacra_domain_model_land AS land,
		tx_germaniasacra_domain_model_zeitraum AS zeitraum,
		tx_germaniasacra_domain_model_bistum AS bistum
	WHERE
		standort.kloster_uid = %s AND
		standort.ort_uid = ort.uid AND
		ort.land_uid = land.uid AND
		(ort.bistum_uid = bistum.uid OR (ort.bistum_uid IS NULL AND bistum.uid = 1)) AND
		standort.zeitraum_uid = zeitraum.uid
	ORDER BY
		zeitraum.von_von,
		zeitraum.von_bis,
		zeitraum.bis_von,
		zeitraum.bis_bis
	"""
	cursor2.execute(queryStandort, [str(docKloster["sql_uid"])])
	for values2 in cursor2:
		docStandort = dict(zip(cursor2.column_names, values2))
		breite = None
		laenge = None
		if docStandort["standort_laenge"] and docStandort["standort_breite"]:
			breite = docStandort["standort_breite"]
			laenge = docStandort["standort_laenge"]
			docStandort["koordinaten_institutionengenau"] = True
		elif docStandort["ort_laenge"] and docStandort["ort_breite"]:
			breite = docStandort["ort_breite"]
			laenge = docStandort["ort_laenge"]
			docStandort["koordinaten_institutionengenau"] = False
		if breite and laenge:
			docStandort["koordinaten"] = str(breite) + "," + str(laenge)
			docStandort["geohash"] = []
			gHash = geohash.encode(float(breite), float(laenge))
			i = 1
			while (i <= len(gHash)):
				docStandort["geohash"] += [('%02d' % i) + "-" + gHash[0:i]]
				i += 1
			
		del docStandort["standort_laenge"]
		del docStandort["standort_breite"]
		del docStandort["ort_laenge"]
		del docStandort["ort_breite"]
		
		if docStandort["bistum_uid"]:
			queryBistumURL = """
			SELECT
				url.url, url.bemerkung,
				url_typ.name AS url_typ
			FROM
				tx_germaniasacra_domain_model_url AS url,
				tx_germaniasacra_domain_model_url_typ AS url_typ,
				tx_germaniasacra_bistum_url_mm AS relation
			WHERE
				url.url_typ_uid = url_typ.uid AND
				url.uid = relation.uid_foreign AND
				relation.uid_local = %s
			"""
			bistum_gnd = ''
			bistum_wikipedia = ''
			cursor3.execute(queryBistumURL, [str(docStandort["bistum_uid"])])
			for values3 in cursor3:
				docURL = dict(zip(cursor3.column_names, values3))
		
				if docURL["url_typ"] == "GND":
					components = docURL["url"].split("/gnd/")
					if len(components) > 1:
						docStandort["bistum_gnd"] = components[1]
					else:
						print "keine GND URL: " + docURL["url"]
				elif docURL["url_typ"] == "Wikipedia":
					bistum_wikipedia = docURL["url"]
			docStandort["bistum_gnd"] = [bistum_gnd]
			docStandort['bistum_wikipedia'] = [bistum_wikipedia]
		else:
			# ohne bistum_uid sind die Felder zum Bistum Fake -> leeren
			docStandort["bistum_uid"] = -1
			docStandort["bistum"] = 'nicht erfasst'
			docStandort["kirchenprovinz"] = ''
			docStandort["ist_erzbistum"] = ''
		
		
		docStandort["url"] = []
		docStandort["url_bemerkung"] = []
		docStandort["url_typ"] = []
		docStandort["url_relation"] = []
		docStandort["geonames"] = []
		improveZeitraumForDocument(docStandort, "standort")
		
		queryOrtURL = """
		SELECT
			url.url,
			url.bemerkung AS url_bemerkung,
			url_typ.name AS url_typ
		FROM
			tx_germaniasacra_domain_model_url AS url,
			tx_germaniasacra_domain_model_url_typ AS url_typ,
			tx_germaniasacra_ort_url_mm AS relation
		WHERE
			url.url_typ_uid = url_typ.uid AND
			url.uid = relation.uid_foreign AND
			relation.uid_local = %s
		"""
		cursor3.execute(queryOrtURL, [str(docStandort["ort_uid"])])
		geoname = ''
		for values3 in cursor3:
			docURL = dict(zip(cursor3.column_names, values3))
			if docURL["url_typ"] == "Geonames":
				geoname = docURL["url"].split("geonames.org/")[1]		
			mergeDocIntoDoc(docURL, docStandort)
		docStandort["geonames"] += [geoname]
		
		mergeDocIntoDoc(docStandort, docKloster)
		doc2 = copy.deepcopy(docStandort)
		doc2["id"] = "kloster-standort-" + str(doc2["standort_uid"])
		doc2["sql_uid"] = doc2["standort_uid"]
		doc2["kloster_id"] = docKloster['id']
		del doc2["standort_uid"]
		doc2["typ"] = "kloster-standort"
		docs += [doc2]
		standorte += [copy.deepcopy(docStandort)]
		
		
	queryOrden = """
	SELECT
		kloster_orden.uid AS kloster_orden_uid, kloster_orden.bemerkung AS bemerkung_orden,
		orden.uid AS orden_uid, orden.orden, orden.ordo AS orden_ordo,
		orden.symbol AS orden_symbol, orden.graphik AS orden_graphik,
		ordenstyp.ordenstyp AS orden_typ,
		kloster_status.status AS kloster_status,
		zeitraum.uid AS zeitraum_uid, zeitraum.von_von AS orden_von_von, zeitraum.von_bis AS orden_von_bis,
		zeitraum.von_verbal AS orden_von_verbal, zeitraum.bis_von AS orden_bis_von,
		zeitraum.bis_bis AS orden_bis_bis, zeitraum.bis_verbal AS orden_bis_verbal
	FROM
		tx_germaniasacra_domain_model_kloster_orden AS kloster_orden,
		tx_germaniasacra_domain_model_orden AS orden,
		tx_germaniasacra_domain_model_klosterstatus AS kloster_status,
		tx_germaniasacra_domain_model_ordenstyp AS ordenstyp,
		tx_germaniasacra_domain_model_zeitraum AS zeitraum
	WHERE
		kloster_orden.kloster_uid = %s AND
		kloster_orden.orden_uid = orden.uid AND
		kloster_orden.klosterstatus_uid = kloster_status.uid AND
		orden.ordenstyp_uid = ordenstyp.uid AND
		kloster_orden.zeitraum_uid = zeitraum.uid
	ORDER BY
		zeitraum.von_von,
		zeitraum.von_bis,
		zeitraum.bis_von,
		zeitraum.bis_bis
	"""
	cursor2.execute(queryOrden, [str(docKloster["sql_uid"])])
	for values2 in cursor2:
		docOrden = dict(zip(cursor2.column_names, values2))
		if docOrden['orden'] and docOrden['orden'] != 'evangelisches Kloster/Stift' and docOrden['orden'] != 'Reformiertes Stift (calvinistisch)':
			# Facettenfeld mit allen außer den evangelischen füllen.
			docOrden['orden_facet'] = docOrden['orden']
		improveZeitraumForDocument(docOrden, "orden")
		
		queryOrdenURL = """
		SELECT
			url.url, url.bemerkung,
			url_typ.name AS url_typ
		FROM
			tx_germaniasacra_domain_model_url AS url,
			tx_germaniasacra_domain_model_url_typ AS url_typ,
			tx_germaniasacra_orden_url_mm AS relation
		WHERE
			url.url_typ_uid = url_typ.uid AND
			url.uid = relation.uid_foreign AND
			relation.uid_local = %s
		"""
		cursor3.execute(queryOrdenURL, [str(docOrden["orden_uid"])])
		orden_gnd = ''
		orden_wikipedia = ''
		for values3 in cursor3:
			docURL = dict(zip(cursor3.column_names, values3))
		
			if docURL["url_typ"] == "GND":
				components = docURL["url"].split("/gnd/")
				if len(components) > 1:
					orden_gnd = components[1]
				else:
					print "keine GND URL: " + docURL["url"]
			elif docURL["url_typ"] == "Wikipedia":
				orden_wikipedia = docURL["url"]
		del docOrden['orden_uid']

		docOrden['orden_gnd'] = [orden_gnd]
		docOrden['orden_wikipedia'] = [orden_wikipedia]
		
		mergeDocIntoDoc(docOrden, docKloster)
		doc2 = copy.deepcopy(docOrden)
		doc2["id"] = "kloster-orden-" + str(doc2["kloster_orden_uid"])
		doc2["sql_uid"] = doc2["kloster_orden_uid"]
		doc2["kloster_id"] = docKloster['id']
		del doc2["kloster_orden_uid"]
		doc2["typ"] = "kloster-orden"
		docs += [doc2]
		orden += [copy.deepcopy(docOrden)]
		
	if docKloster.has_key('ort') and len(docKloster['ort']) > 0:
		docKloster['ort_sort'] = docKloster['ort'][0]
	
	# Informationen aus der Personendatenbank in den Index einfügen.
	if personen.has_key(str(docKloster["sql_uid"])):
		klosterPersonen = personen[str(docKloster["sql_uid"])]
		for person in klosterPersonen:
			mergeDocIntoDoc(person, docKloster)

	# Standorte und Ordenszugehörigkeiten »ausmultiplizieren« und eigene Datensätze für die Kombinationen erzeugen
	standortOrdenCount = 1
	for myOrden in orden:
		for myStandort in standorte:
			if myOrden['orden_von_von'] < myStandort['standort_bis_bis'] \
				and myStandort['standort_von_von'] < myOrden['orden_bis_bis']:
				doc = copy.deepcopy(docKlosterBasic)
				
				# von/bis und Jahr 50
				doc['orden_standort_von'] = max(myOrden['orden_von_von'], myStandort['standort_von_von'])
				doc['orden_standort_bis'] = min(myOrden['orden_bis_bis'], myStandort['standort_bis_bis'])
				doc['orden_standort_jahr50'] = []
				start = minYear
				while start < maxYear:
					if doc['orden_standort_von'] < (start + yearStep) and start <= doc['orden_standort_bis']:
						doc['orden_standort_jahr50'] += [start]
					start += yearStep
				
				# Orden und Standort Felder
				mergeDocIntoDoc(myOrden, doc)
				mergeDocIntoDoc(myStandort, doc)
				
				# Verwaltungsfelder
				doc['typ'] = 'standort-orden'
				doc['kloster_id'] = str(docKloster["id"])
				doc['id'] = 'standort-orden-' + str(docKloster["kloster_id"]) + '-' + str(standortOrdenCount)
				standortOrdenCount += 1
				docs += [doc]
	
	
	# von und bis Felder hinzufügen
	if docKloster.has_key('standort_von_von') and docKloster.has_key('orden_von_von'):
		docKloster['von'] = min(docKloster['standort_von_von'] + docKloster['orden_von_von'])
	if docKloster.has_key('standort_bis_bis') and docKloster.has_key('orden_bis_bis'):
		docKloster['bis'] = min(docKloster['standort_bis_bis'] + docKloster['orden_bis_bis'])
	
	docs += [docKloster]
	

# Replace None by empty strings
for doc in docs:
	for item in doc.itervalues():
		if type(item) == list:
			for i, value in enumerate(item):
				if value == None:
					item[i] = ""



# MySQL Verbindungen schließen
cursor3.close()
cursor2.close()	
cursor.close()
db3.close()
db2.close()
db.close()


#pprint.pprint(docs)
# Indexieren
index = solr.Solr('http://localhost:8080/solr/germania-sacra')
index.delete_query('*:*')
index.add_many(docs)
index.commit()

index = solr.Solr('http://vlib.sub.uni-goettingen.de/solr/germania-sacra')
index.delete_query('*:*')
index.add_many(docs)
index.commit()
