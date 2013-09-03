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
# benötigt das Modul Geohash (z.B. über easy_install)
import Geohash
import urllib
import json
import xml.etree.ElementTree
import os

import mysql.connector
db = mysql.connector.connect(user='root', host='127.0.0.1', database='kloster')
db2 = mysql.connector.connect(user='root', host='127.0.0.1', database='kloster')
db3 = mysql.connector.connect(user='root', host='127.0.0.1', database='kloster')
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



minYear = 700
maxYear = 1810
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
		if doc[prefix + "_von"] != minYear and doc[prefix + "_von"] != maxYear:
			doc[prefix + "_verbal"] = str(doc[prefix + "_von"])
		
		if doc[prefix + "_bis"] != minYear and doc[prefix + "_bis"] != maxYear:
			if doc[prefix + "_von"] != doc[prefix + "_bis"]:
				doc[prefix + "_verbal"] += '/' +  str(doc[prefix + "_bis"])



def improveZeitraumForDocument (doc, prefix):
	if doc[prefix + "_von_von"]:
		if not doc[prefix + "_von_bis"]:
			doc[prefix + "_von_bis"] = doc[prefix + "_von_von"]
	else:
		doc[prefix + "_von_von"] = minYear
		if not doc[prefix + "_von_bis"]:
			doc[prefix + "_von_bis"] = minYear
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
			doc[prefix + "_bis_von"] = maxYear
			doc[prefix + "_bis_bis"] = maxYear
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
	tx_gs_domain_model_bearbeitungsstatus.name as bearbeitungsstatus,
	tx_gs_domain_model_personallistenstatus.name as personallistenstatus
FROM 
	tx_gs_domain_model_kloster AS kloster,
	tx_gs_domain_model_band AS band,
	tx_gs_domain_model_bearbeitungsstatus,
	tx_gs_domain_model_personallistenstatus
WHERE
	(band.uid = kloster.band_uid OR (kloster.band_uid IS NULL AND band.uid = 1)) AND
	tx_gs_domain_model_bearbeitungsstatus.uid = kloster.bearbeitungsstatus_uid AND
	tx_gs_domain_model_personallistenstatus.uid = kloster.personallistenstatus_uid
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
	docKloster["id"] = 'kloster-' + str(docKloster["kloster_id"])
	docKloster["url"] = []
	docKloster["url_bemerkung"] = []
	docKloster["url_art"] = []
	docKloster["url_relation"] = []
	docKloster["url_wikipedia"] = []
	docKloster["gnd"] = []

	queryBandURL = """
	SELECT
		url.url, url.bemerkung, url.art
	FROM
		tx_gs_domain_model_url AS url,
		tx_gs_band_url_mm AS relation		
	WHERE
		relation.uid_local = %s AND
		url.uid = relation.uid_foreign
	"""
	if docKloster.has_key("band_id"):
		cursor2.execute(queryBandURL, [str(docKloster["band_id"])])
		docURLs = {}
		for values2 in cursor2:
			docURL = dict(zip(cursor2.column_names, values2))
			docURLs[docURL["art"]] = docURL["url"]

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
		url.url, url.bemerkung, url.art
	FROM
		tx_gs_domain_model_url AS url,
		tx_gs_kloster_url_mm AS relation
	WHERE
		url.uid = relation.uid_foreign AND
		relation.uid_local = %s
	"""
	cursor2.execute(queryKlosterURL, [str(docKloster["sql_uid"])])
	for values2 in cursor2:
		docURL = dict(zip(cursor2.column_names, values2))
		
		if docURL["art"] != "Wikipedia":
			docKloster["url"] += [docURL["url"]]
			docKloster["url_bemerkung"] += [docURL["bemerkung"]]
			docKloster["url_art"] += [docURL["art"]]
			docKloster["url_relation"] += ["kloster"]
		else:
			docKloster["url_wikipedia"] += [docURL["url"]]
		
		if docURL["art"] == "GND":
			components = docURL["url"].split("/gnd/")
			if len(components) > 1:
				docKloster["gnd"] += [components[1]]
			else:
				print "keine GND URL: " + docURL["url"]

	docKlosterBasic = copy.deepcopy(docKloster)

	
	literaturDict = {}
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
		tx_gs_domain_model_kloster_standort AS standort,
		tx_gs_domain_model_ort AS ort,
		tx_gs_domain_model_land AS land,
		tx_gs_domain_model_zeitraum AS zeitraum,
		tx_gs_domain_model_bistum AS bistum
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
			geohash = Geohash.encode(breite, laenge)
			i = 1
			while (i <= len(geohash)):
				docStandort["geohash"] += [('%02d' % i) + "-" + geohash[0:i]]
				i += 1
			
		del docStandort["standort_laenge"]
		del docStandort["standort_breite"]
		del docStandort["ort_laenge"]
		del docStandort["ort_breite"]
		
		# ohne bistum_uid sind die Felder zum Bistum Fake -> leeren
		if not docStandort["bistum_uid"]:
			docStandort["bistum_uid"] = -1
			docStandort["bistum"] = 'nicht erfasst'
			docStandort["kirchenprovinz"] = ''
			docStandort["ist_erzbistum"] = ''
		
		docStandort["url"] = []
		docStandort["url_bemerkung"] = []
		docStandort["url_art"] = []
		docStandort["url_relation"] = []
		improveZeitraumForDocument(docStandort, "standort")
		
		queryOrtURL = """
		SELECT
			url.url, url.bemerkung AS url_bemerkung, url.art AS url_art
		FROM
			tx_gs_domain_model_url AS url,
			tx_gs_ort_url_mm AS relation
		WHERE
			url.uid = relation.uid_foreign AND
			relation.uid_local = %s
		"""
		cursor3.execute(queryOrtURL, [str(docStandort["ort_uid"])])
		for values3 in cursor3:
			docURL = dict(zip(cursor3.column_names, values3))
			docURL["geonames"] = []
			if docURL["url_art"] == "Geonames":
				docURL["geonames"] += [docURL["url"].split("geonames.org/")[1]]
			mergeDocIntoDoc(docURL, docStandort)
		 
						
		queryLiteratur = """
		SELECT 
			literatur.uid, literatur.beschreibung, bibitem.bibitem
		FROM
			tx_gs_domain_model_literatur AS literatur,
			tx_gs_domain_model_bibitem AS bibitem,
			tx_gs_kloster_standort_literatur_mm AS relation
		WHERE
			relation.uid_local = %s AND
			relation.uid_foreign = literatur.uid AND
			bibitem.uid = literatur.bibitem_uid
		"""
		cursor3.execute(queryLiteratur, [str(docStandort["standort_uid"])])
		literaturDict2 = {}
		for values3 in cursor3:
			docLiteratur = dict(zip(cursor3.column_names, values3))
			literatur = docLiteratur["bibitem"]
			if docLiteratur["beschreibung"]:
				literatur += ", " + docLiteratur["beschreibung"]
			if literatur:
				literaturDict[literatur] = True
		


		mergeDocIntoDoc(docStandort, docKloster)
		doc2 = copy.deepcopy(docStandort)
		doc2["id"] = "kloster-standort-" + str(doc2["standort_uid"])
		doc2["sql_uid"] = doc2["standort_uid"]
		doc2["kloster_id"] = docKloster['id']
		doc2["literatur"] = literaturDict.keys()
		del doc2["standort_uid"]
		doc2["typ"] = "kloster-standort"
		docs += [doc2]
		standorte += [copy.deepcopy(docStandort)]
		
		
	queryOrden = """
	SELECT
		kloster_orden.uid AS kloster_orden_uid, kloster_orden.bemerkung AS bemerkung_orden,
		orden.orden, orden.ordo AS orden_ordo, orden.symbol AS orden_symbol, orden.graphik AS orden_graphik,
		ordenstyp.ordenstyp AS orden_typ,
		kloster_status.status AS kloster_status,
		zeitraum.uid AS zeitraum_uid, zeitraum.von_von AS orden_von_von, zeitraum.von_bis AS orden_von_bis,
		zeitraum.von_verbal AS orden_von_verbal, zeitraum.bis_von AS orden_bis_von,
		zeitraum.bis_bis AS orden_bis_bis, zeitraum.bis_verbal AS orden_bis_verbal
	FROM
		tx_gs_domain_model_kloster_orden AS kloster_orden,
		tx_gs_domain_model_orden AS orden,
		tx_gs_domain_model_klosterstatus AS kloster_status,
		tx_gs_domain_model_ordenstyp AS ordenstyp,
		tx_gs_domain_model_zeitraum AS zeitraum
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
		if docOrden['orden'] and docOrden['orden'] != 'evangelisches Kloster/Stift':
			# Facettenfeld mit allen außer den evangelischen füllen.
			docOrden['orden_facet'] = docOrden['orden']
		improveZeitraumForDocument(docOrden, "orden")
		mergeDocIntoDoc(docOrden, docKloster)
		doc2 = copy.deepcopy(docOrden)
		doc2["id"] = "kloster-orden-" + str(doc2["kloster_orden_uid"])
		doc2["sql_uid"] = doc2["kloster_orden_uid"]
		doc2["kloster_id"] = docKloster['id']
		del doc2["kloster_orden_uid"]
		doc2["typ"] = "kloster-orden"
		docs += [doc2]
		orden += [copy.deepcopy(docOrden)]
	
	docKloster["literatur"] = literaturDict.keys()
	
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
				doc['literatur'] = literaturDict.keys()
				
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
import solr
index = solr.Solr('http://localhost:8080/solr/germania-sacra')
index.delete_query('*:*')
index.add_many(docs)
index.commit()

index = solr.Solr('http://vlib.sub.uni-goettingen.de/solr/germania-sacra')
index.delete_query('*:*')
index.add_many(docs)
index.commit()
