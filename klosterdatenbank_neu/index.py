#! /usr/bin/env python
#coding=utf-8
"""
Skript zur Indexierung der Germania Sacra Daten.
Liest die Daten aus MySQL,
denormalisiert sie in flache Solr Dokumente
und spielt sie in einen Solr Index.

2013 Sven-S. Porst, SUB Göttingen <porst@sub.uni-goettingen.de>
"""

import copy
import pprint

import solr
#index = solr.Solr('http://localhost:8080/solr/gs')
index = solr.Solr('http://vlib.sub.uni-goettingen.de/solr/germania-sacra')

import mysql.connector
db = mysql.connector.connect(user='root', host='127.0.0.1', database='kloster')
db2 = mysql.connector.connect(user='root', host='127.0.0.1', database='kloster')
db3 = mysql.connector.connect(user='root', host='127.0.0.1', database='kloster')
cursor = db.cursor()
cursor2 = db2.cursor()
cursor3 = db3.cursor()


def addValueForKeyToDict (value, key, myDict):
    if not myDict.has_key(key):
        myDict[key] = []
    myDict[key] += [value]

def mergeDocIntoDoc (new, target):
    for key in new.keys():
        value = new[key]
        if type(value) == list:
            for item in value:
                addValueForKeyToDict(item, key, target)
        else:
            addValueForKeyToDict(value, key, target)

def improveZeitraumForDocument (doc, prefix):
    start = 500
    if not doc.has_key("jahr50"):
        doc[prefix + "_jahr50"] = []
        if doc.has_key(prefix + "_von_von") and doc[prefix + "_von_von"]:    
            von = int(doc[prefix + "_von_von"])
            bis = 0
            if doc.has_key(prefix + "_bis_bis") and doc[prefix + "_bis_bis"]:
                bis = int(doc[prefix + "_bis_bis"])
            elif doc.has_key(prefix + "_bis_von") and doc[prefix + "_bis_von"]:
                bis = int(doc[prefix + "_bis_von"])
            else:
                bis = von

            while start < 2500:
                if von < (start + 50) and start <= bis:
                    doc[prefix + "_jahr50"] += [start]
                start += 50


docs = []


# kloster
queryKloster = """
SELECT
    kloster.uid AS sql_uid, kloster.kloster, kloster.patrozinium, kloster.bemerkung AS bemerkung_kloster,
    kloster.text_gs_band, kloster.band_uid
FROM 
    tx_gs_domain_model_kloster AS kloster
"""
cursor.execute(queryKloster)
for values in cursor:
    docKloster = dict(zip(cursor.column_names, values))
    
    docKloster["typ"] = "kloster"
    docKloster["id"] = 'kloster-' + str(docKloster["sql_uid"])
    docKloster["url"] = []
    docKloster["url_bemerkung"] = []
    docKloster["url_art"] = []
    docKloster["url_relation"] = []
    docKloster["gnd"] = []

    queryBandURL = """
    SELECT
        url.url, url.bemerkung, url.art
    FROM
        tx_gs_domain_model_url AS url,
        tx_gs_band_url_mm AS relation        
    WHERE
        url.uid = relation.uid_foreign AND
        relation.uid_local = %s
    """
    cursor2.execute(queryBandURL, [str(docKloster["band_uid"])])
    for values2 in cursor2:
        docURL = dict(zip(cursor2.column_names, values2))
        docKloster["url"] += [docURL["url"]]
        docKloster["url_bemerkung"] += [docURL["bemerkung"]]
        docKloster["url_art"] += [docURL["art"]]
        docKloster["url_relation"] += ["band"]
    
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
        docKloster["url"] += [docURL["url"]]
        docKloster["url_bemerkung"] += [docURL["bemerkung"]]
        docKloster["url_art"] += [docURL["art"]]
        docKloster["url_relation"] += ["kloster"]
        
        if docURL["art"] == "GND":
            components = docURL["url"].split("/gnd/")
            if len(components) > 1:
                docKloster["gnd"] += [components[1]]
            else:
                print "keine GND URL: " + docURL["url"]
    
    
    queryStandort = """
    SELECT
        standort.uid AS standort_uid, standort.gruender, standort.bemerkung_standort,
        standort.breite AS standort_breite, standort.laenge AS standort_laenge,
        ort.uid AS ort_uid, ort.ort, ort.gemeinde, ort.kreis, ort.bistum_uid AS bistum_uid, ort.wuestung, ort.breite AS ort_breite, ort.laenge AS ort_laenge,
        land.land, land.ist_in_deutschland,
        zeitraum.uid AS zeitraum_uid,
        zeitraum.von_von AS standort_von_von, zeitraum.von_bis AS standort_von_bis, zeitraum.von_verbal AS standort_von_verbal,
        zeitraum.bis_von AS standort_bis_von, zeitraum.bis_bis AS standort_bis_bis, zeitraum.bis_verbal AS standort_bis_verbal,
        bistum.bistum, bistum.kirchenprovinz, bistum.bemerkung AS bemerkung_bistum, bistum.ist_erzbistum
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
    """
    cursor2.execute(queryStandort, [str(docKloster["sql_uid"])])
    for values2 in cursor2:
        docStandort = dict(zip(cursor2.column_names, values2))
        if docStandort["standort_laenge"] and docStandort["standort_breite"]:
            docStandort["laenge"] = docStandort["standort_laenge"]
            docStandort["breite"] = docStandort["standort_breite"]
        else:
            docStandort["laenge"] = docStandort["ort_laenge"]
            docStandort["breite"] = docStandort["ort_breite"]
        del docStandort["standort_laenge"]
        del docStandort["standort_breite"]
        del docStandort["ort_laenge"]
        del docStandort["ort_breite"]
        
        # ohne bistum_uid sind die Felder zum Bistum Fake -> löschen
        if not docStandort["bistum_uid"]:
            del docStandort["bistum"]
            del docStandort["kirchenprovinz"]
            del docStandort["bemerkung_bistum"]
            del docStandort["ist_erzbistum"]
        
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
            if docURL["url_art"] == "Geonames":
                docURL["geonames"] += [docURL["url"].split("geonames.org/")[1]]
            mergeDocIntoDoc(docURL, docStandort)
         
                        
        queryLiteratur = """
        SELECT 
            literatur.beschreibung, bibitem.bibitem
        FROM
            tx_gs_domain_model_literatur AS literatur,
            tx_gs_domain_model_bibitem AS bibitem,
            tx_gs_kloster_standort_literatur_mm AS relation
        WHERE
            relation.uid_local = %s AND
            relation.uid_foreign = literatur.uid AND
            bibitem.uid = literatur.bibitem_uid
        """
        cursor3.execute(queryOrtURL, [str(docStandort["ort_uid"])])
        for values3 in cursor3:
            docLiteratur = dict(zip(cursor3.column_names, values3))
            mergeDocIntoDoc(docLiteratur, docStandort)
        
        mergeDocIntoDoc(docStandort, docKloster)
        doc2 = copy.deepcopy(docStandort)
        doc2["id"] = "kloster-standort-" + str(doc2["standort_uid"])
        doc2["sql_uid"] = doc2["standort_uid"]
        del doc2["standort_uid"]
        doc2["typ"] = "kloster-standort"
        docs += [doc2]
        
        
    queryOrden = """
    SELECT
	    kloster_orden.uid AS kloster_orden_uid, kloster_orden.status, kloster_orden.bemerkung AS bemerkung_orden,
        orden.orden, orden.ordo, orden.symbol,
        ordenstyp.ordenstyp,
        zeitraum.uid AS zeitraum_uid, zeitraum.von_von AS orden_von_von, zeitraum.von_bis AS orden_von_bis, zeitraum.von_verbal AS orden_von_verbal, zeitraum.bis_von AS orden_bis_von, zeitraum.bis_bis AS orden_bis_bis, zeitraum.bis_verbal AS orden_bis_verbal
    FROM
	    tx_gs_domain_model_kloster_orden AS kloster_orden,
    	tx_gs_domain_model_orden AS orden,
    	tx_gs_domain_model_ordenstyp AS ordenstyp,
    	tx_gs_domain_model_zeitraum AS zeitraum
    WHERE
    	kloster_orden.kloster_uid = %s AND
    	kloster_orden.orden_uid = orden.uid AND
    	orden.ordenstyp_uid = ordenstyp.uid AND
        kloster_orden.zeitraum_uid = zeitraum.uid
    """
    cursor2.execute(queryOrden, [str(docKloster["sql_uid"])])
    for values2 in cursor2:
        docOrden = dict(zip(cursor2.column_names, values2))
        improveZeitraumForDocument(docOrden, "orden")
        mergeDocIntoDoc(docOrden, docKloster)
        doc2 = copy.deepcopy(docOrden)
        doc2["id"] = "kloster-orden-" + str(doc2["kloster_orden_uid"])
        doc2["sql_uid"] = doc2["kloster_orden_uid"]
        del doc2["kloster_orden_uid"]
        doc2["typ"] = "kloster-orden"
        docs += [doc2]
        
    docs += [docKloster]


pprint.pprint(docs)

index.add_many(docs)


index.commit()

cursor3.close()
cursor2.close()	
cursor.close()
db3.close()
db2.close()
db.close()
