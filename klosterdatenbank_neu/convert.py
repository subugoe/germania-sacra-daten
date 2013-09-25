#! /usr/bin/env python
#coding=utf-8
"""
Skript zum Import des Access SQL Dumps in MySQL
mit Anpassung an das neue Datenbankschema:
    * stärkere Normalisiserung
    * Anpassung an TYPO3 Felder

2013 Sven-S. Porst, SUB Göttingen <porst@sub.uni-goettingen.de>
"""


import re
import copy
import pprint
import mysql.connector
from mysql.connector.errors import Error
db = mysql.connector.connect(user='root', host='127.0.0.1')
cursor = db.cursor()
import urllib
import time

readPrefix = 'Klosterdatenbank.tbl'
writePrefix = 'kloster`.`tx_gs_'

bearbeiterDict = {
	1: 31, # Christian Popp
	2: 33, # Juliane Michael
	3: 37, # Lara Räuschel
	5: 34, # Jasmin Hoven
	6: 35, # Natalie Kruppa
	7: 20, # Bärbel Kröger
	8: 36, # Anna Renziehausen
	9: 32, # Fenna Campen
}

bearbeitungsstatusDict = {
	u'Angaben unklar': 0,
	u'Daten importiert': 1,
	u'Quellenlage unvollständig': 2,
	u'Geprüft (bei Eingabe)': 3,
	u'Redaktionell geprüft': 4,
	u'Neuaufnahme, unvollständig': 5,
	u'Online': 6
}

defaultDate = int(time.mktime(time.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')))
defaultFields = {
	'tstamp': int(time.time()),
	'crdate': defaultDate,
	'cruser_id': 0,
	'deleted': 0,
	'hidden': 0,
	'starttime': 0,
	'endtime': 0,
	't3ver_oid': 0,
	't3ver_id': 0,
	't3ver_wsid': 0,
	't3ver_label': '',
	't3ver_state': 0,
	't3ver_stage': 0,
	't3ver_count': 0,
	't3ver_tstamp': 0,
	't3ver_move_id': 0,
	't3_origuid': 0,
	'sys_language_uid': 0,
	'l10n_parent': 0,
	'l10n_diffsource': None,
	'pid': 0
}


# from http://docs.python.org/2/library/csv.html
import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def addRecordsToTable (records, tableName):
	global db, cursor
	print u"\n\nTabelle »" + tableName + u"«: " + str(len(records)) + u" Datensätze"

	if len(records) > 0:
		for record in records:
			prefix = writePrefix
			if tableName[-3:] != '_mm':
				prefix += 'domain_model_'
			
				# add default fields to record
				for fieldName in defaultFields:
					if not record.has_key(fieldName):
						record[fieldName] = defaultFields[fieldName]

			fieldNames = '(' + ', '.join(record.keys()) + ')'
			values = '(%(' + ')s, %('.join(record.keys()) + ')s)'
			insertStatement = "INSERT INTO `" + prefix + tableName + "` " + fieldNames + " VALUES " + values
			#print tableName
			#pprint.pprint(record)
			if tableName == 'bistum':
				cursor.execute('SET foreign_key_checks = 0')
			cursor.execute(insertStatement, record)
			if tableName == 'bistum':
				cursor.execute('SET foreign_key_checks = 1')
			# print cursor.statement
			
		db.commit()


def addGNDURLToDoc (row, fieldName, doc, note, relationDict):
	urls = row[fieldName]
	if urls:
		urls = urls.replace(chr(9), ' ').replace('http:// ', '').replace(' http', ';http').replace(';', '#').split('#')
		for myURL in urls:
			myURL = myURL.strip().strip('# ')
			GNDID = re.sub(r'http://d-nb.info/gnd/', '', myURL)
			URLRelation = makeURLData(myURL, note + ' [' + GNDID + ']', 'GND', doc['uid'])
			if URLRelation:
				key = str(URLRelation['uid_local']) + '-' + str(URLRelation['uid_foreign'])
				relationDict[key] = URLRelation



def addWikipediaURLToDoc (row, fieldName, doc, relationDict):
	urls = row[fieldName]
	if urls:
		urls = urls.replace('http:// ', '').replace(';', '#').split('#')
		for myURL in urls:
			lemma = re.sub(r'.*/wiki/' , '', myURL).replace('_', ' ')
			lemma = urllib.unquote(str(lemma))
			lemma = lemma.decode('utf-8')
			URLRelation = makeURLData(myURL, lemma, 'Wikipedia', doc['uid'])
			if URLRelation:
				key = str(URLRelation['uid_local']) + '-' + str(URLRelation['uid_foreign'])
				relationDict[key] = URLRelation



def makeURLData (URL, bemerkung, art, record_uid):
	global urlDict
	URLRelation = None
	if URL:
		if not urlDict.has_key(URL):
			urlDict[URL] = {
				'uid': len(urlDict) + 1,
				'url': URL,
				'bemerkung': bemerkung,
				'art': art
			}
			# print u"INFO: neue URL »" + URL + u"«"
		else:
			print u"INFO: URL »" + URL + u"« existiert bereits: doppelt nutzen."
			
		URLRelation = {
			'uid_local': record_uid,
			'uid_foreign': urlDict[URL]['uid']
		}

	return URLRelation


urlDict = {}
zeitraum = []



# CSV Datei mit Mapping Literaturdaten auf citekeys lesen
citekeyDict = {}
with open('GS-citekeys.csv', 'rb') as citekeysCSV:
	citekeyReader = UnicodeReader(citekeysCSV, delimiter=',')
	columnDict = {}
	for row in citekeyReader:
		if row[0] == 'uid':
			# Spaltennummern für Felder feststellen
			for index, value in enumerate(row):
				columnDict[value] = index
		else:
			citeInfo = {
				'titel': row[columnDict['titel']],
				'citekey': row[columnDict['citekey']],
				'detail': row[columnDict['detail']]
			}
			citekeyDict[citeInfo['titel']] = citeInfo


# Bistümer
tabelle = readPrefix + 'Bistum'
query = "SELECT * from " + tabelle
cursor.execute(query)

bistumDict = {}
bistum_has_urlDict = {}
for values in cursor:
	row = dict(zip(cursor.column_names, values))
	ist_erzbistum = (row['ErzbistumAuswahlfeld'] == 'Erzbistum')
	r = {
		'uid': row['ID'],
		'bistum': row['Bistum'],
		'kirchenprovinz': row['Kirchenprovinz'],
		'bemerkung': row['Bemerkung'],
		'ist_erzbistum': ist_erzbistum,
		'shapefile': row['Shapefile'],
		'ort_uid': row['Bistumssitz']
	}
	
	GNDLabel = ''
	if r['ist_erzbistum']:
		GNDLabel = 'Erzbistum'
	else:
		GNDLabel = 'Bistum'
	GNDLabel += ' ' + r['bistum']
	addGNDURLToDoc(row, 'GND_Dioezese', r, r['bistum'], bistum_has_urlDict)
	addWikipediaURLToDoc(row, 'Wikipedia_Dioezese', r, bistum_has_urlDict)
	
	bistumDict[row['ID']] = r
	



# Bände
tabelle = readPrefix + 'GSBaende'
query = "SELECT * from " + tabelle
cursor.execute(query)

band = []
band_has_urlDict = {}
for values in cursor:
	row = dict(zip(cursor.column_names, values))
	uid = row['ID_GSBand']
	r = {
		'uid': uid,
		'nummer': row['Bandnummer'],
		'sortierung': row['Sortierung'],
		'titel': row['Kurztitel'],
		'kurztitel': row['KurztitelFacette'],
		'bistum_uid': row['Bistum']
	}
	band += [r]
	
	urls = row['url']
	buchtitel = 'Germania Sacra ' + r['nummer'] + ': ' + r['titel']
	if urls:
		urls = urls.split('#')
		#for myURL in urls:
		myURL = urls[0]
		myURL = myURL.strip().strip('# ')
		URLRelation = makeURLData(myURL, buchtitel, 'Dokument', uid)
		if URLRelation:
			key = str(URLRelation['uid_local']) + '-' + str(URLRelation['uid_foreign'])
			band_has_urlDict[key] = URLRelation
	if row['handle']:
		URLRelation = makeURLData(row['handle'].strip('#'), buchtitel, 'Handle', uid)
		if URLRelation:
			key = str(URLRelation['uid_local']) + '-' + str(URLRelation['uid_foreign'])
			band_has_urlDict[key] = URLRelation
	if row['findpage']:
		URLRelation = makeURLData(row['findpage'].strip('#').split('#')[0].strip('/'), buchtitel, 'Findpage', uid)
		if URLRelation:
			key = str(URLRelation['uid_local']) + '-' + str(URLRelation['uid_foreign'])
			band_has_urlDict[key] = URLRelation


# Kloster Stammblatt
tabelle = readPrefix + 'KlosterStammblatt'
query = "SELECT * from " + tabelle + " ORDER BY Klosternummer"
cursor.execute(query)

klosterDict =  {}
kloster_has_urlDict = {}
personallistenstatusDict = {}
for values in cursor:
	row = dict(zip(cursor.column_names, values))
	uid = row['Klosternummer']
	
	if uid != None:
		crdate = None
		if row['Datensatz angelegt'] != None:
			crdate = int(time.mktime(time.strptime(str(row['Datensatz angelegt']), '%Y-%m-%d %H:%M:%S')))
		if not crdate:
			crdate = defaultDate
		cruser_id = 1
		
		if bearbeiterDict.has_key(row['Bearbeiter']):
			cruser_id = bearbeiterDict[row['Bearbeiter']]
		else:
			print u"WARNUNG: ungültige Bearbeiter ID »" + str(row['Bearbeiter']) + u"« in klosterStammblatt " + str(uid) + u". Verwende: 1"
				
		bearbeitungsstatus = 0
		if bearbeitungsstatusDict.has_key(row['Status']):
			bearbeitungsstatus = bearbeitungsstatusDict[row['Status']]
		else:
			print u"WARNUNG: ungültiger Bearbeitungstatus »" + str(row['Status']) + u"« in klosterStammblatt " + str(uid) + u". Verwende: " + str(bearbeitungsstatus)
		
		if not personallistenstatusDict.has_key(row['Personallisten']):
			personallistenstatusDict[row['Personallisten']] = {
				'uid': len(personallistenstatusDict),
				'name': row['Personallisten']
			}
		personallistenstatus = personallistenstatusDict[row['Personallisten']]['uid']
	
		r = {
			'uid': uid,
			'kloster_id': uid,
			'kloster': row['Klostername'],
			'patrozinium': row['Patrozinium'],
			'bemerkung': row['Bemerkungen'],
			'band_uid': row['GermaniaSacraBandNr'],
			'band_seite': row['GSBandSeite'],
			'text_gs_band': row['TextGSBand'],
			'crdate': crdate,
			'cruser_id': cruser_id,
			'bearbeitungsstatus_uid': bearbeitungsstatus,
			'personallistenstatus_uid': personallistenstatus
		}
		klosterDict[uid] = r
	
		addGNDURLToDoc(row, 'GND', r, r['kloster'], kloster_has_urlDict)
		addWikipediaURLToDoc(row, 'Wikipedia', r, kloster_has_urlDict)

	else:
		print u"FEHLER: klosterStammblatt Datensatz ohne Klosternummer:"
		pprint.pprint(row)




# Orden
tabelle = readPrefix + 'Orden'
query = "SELECT * from " + tabelle
cursor.execute(query)

orden = []
ordenstypDict = {}
orden_has_urlDict = {}
for values in cursor:
	row = dict(zip(cursor.column_names, values))
	graphik = None
	if row['Grafikdatei']:
		graphik = row['Grafikdatei'].split('.png')[0]
	r = {
		'uid': row['ID_Ordo'],
		'orden': row['Ordensbezeichnung'],
		'ordo': row['Ordo'],
		'symbol': row['Symbol'],
		'graphik': graphik
	}

	ordenstyp = row['Geschlecht']
	if not ordenstyp:
		ordenstyp = 'unbekannt'
	if not ordenstypDict.has_key(ordenstyp):
		r2 = {
			'uid': len(ordenstypDict) + 1,
			'ordenstyp': ordenstyp
		}
		ordenstypDict[r2['ordenstyp']] = r2
	r['ordenstyp_uid'] = ordenstypDict[ordenstyp]['uid']
	
	addGNDURLToDoc(row, 'GND_Orden', r, r['orden'], orden_has_urlDict)
	addWikipediaURLToDoc(row, 'Wikipedia_Orden', r, orden_has_urlDict)
	
	orden += [r]


# Kloster Orden
tabelle = readPrefix + 'KlosterOrden'
query = "SELECT * from " + tabelle
cursor.execute(query)
klosterstatusDict = {}

kloster_orden = []
for values in cursor:
	row = dict(zip(cursor.column_names, values))
	kloster_uid = row['Klosternummer']
	orden_uid = row[u'Ordenszugehörigkeit']
	
	if kloster_uid and orden_uid:
		if row['Klosterstatus'] == None or row['Klosterstatus'] == '':
			row['Klosterstatus'] = u'keine Angabe'
		
		if not klosterstatusDict.has_key(row['Klosterstatus']):
			klosterstatusDict[row['Klosterstatus']] = {
				'uid': len(klosterstatusDict),
				'status': row['Klosterstatus']
			}
		klosterstatus_uid = klosterstatusDict[row['Klosterstatus']]['uid']
	
		r = {
			'uid': row['ID_KlosterOrden'],
			'kloster_uid': kloster_uid,
			'orden_uid': orden_uid,
			'klosterstatus_uid': klosterstatus_uid,
			'bemerkung': row['interne_Anmerkungen'],
			'crdate': klosterDict[kloster_uid]['crdate'],
			'cruser_id': klosterDict[kloster_uid]['cruser_id']
		}
	
		r2 = {
			'uid': len(zeitraum) + 1,
			'von_von': row[u'Ordenszugehörigkeit_von_von'],
			'von_bis': row[u'Ordenszugehörigkeitvon__bis'],
			'von_verbal': row[u'OrdenszugehörigkeitVerbal_von'],
			'bis_von': row[u'Ordenszugehörigkeit_bis_von'],
			'bis_bis': row[u'Ordenzugehörigkeit_bis_bis'],
			'bis_verbal': row[u'OrdenszugehörigkeitVerbal_bis'],
			'crdate': klosterDict[kloster_uid]['crdate'],
			'cruser_id': klosterDict[kloster_uid]['cruser_id']
		}
		zeitraum += [r2]
		r['zeitraum_uid'] = r2['uid']
		
		kloster_orden += [r]
		
	else:
		if not kloster_uid:
			print u"FEHLER: Klosternummer fehlt in klosterOrden ID " + str(row['ID_KlosterOrden']) + u": Datensatz verwerfen"
		elif not orden_uid:
			print "FEHLER: orden_uid fehlt in klosterOrden ID " + str(row['ID_KlosterOrden']) + u": Datensatz verwerfen"
		pprint.pprint(row)


# Land
tabelle = readPrefix + 'Bundesländer'
query = "SELECT * from " + tabelle
cursor.execute(query)

land = []
for values in cursor:
	row = dict(zip(cursor.column_names, values))
	r = {
		'uid': row['ID_Bundesland'],
		'land': row['Land'],
		'ist_in_deutschland': row['Deutschland']
	}
	land += [r]



# Ort
tabelle = readPrefix + 'alleOrte'
query = "SELECT * from " + tabelle
cursor.execute(query)

ort = []
ort_has_urlDict = {}
for values in cursor:
	row = dict(zip(cursor.column_names, values))
	uid = row['ID']
	bistum_uid = row['ID_Bistum']
	if not (bistum_uid == None or bistumDict.has_key(bistum_uid)):
		print u"FEHLER: Feld »ID_Bistum« hat ungültigen Wert »" + str(bistum_uid) + u"« in alleOrte " + str(uid) + ". Verwende: 1"
		bistum_uid = 1
	
	if row['Laenge']:
		row['Laenge'] = row['Laenge'].strip().replace(unichr(8206), '')
	
	r = {
		'uid': uid,
		'ort': row['Ort'],
		'gemeinde': row['Gemeinde'],
		'kreis': row['Kreis'],
		'land_uid': row['Land'],
		'wuestung': row[u'Wüstung'],
		'breite': row['Breite'],
		'laenge': row['Laenge'],
        'bistum_uid': bistum_uid
	}
	ort += [r]

	url = row['GeoNameId']
	if url:
		myURL = 'http://geonames.org/' + str(url)
		URLRelation = makeURLData(myURL, r['ort'] + ' [' + str(url) + ']', 'Geonames', uid)
		if URLRelation:
			key = str(URLRelation['uid_local']) + '-' + str(URLRelation['uid_foreign'])
			ort_has_urlDict[key] = URLRelation



# Kloster Standort
tabelle = readPrefix + 'KlosterStandort'
query = "SELECT * from " + tabelle + " ORDER BY Klosternummer"
cursor.execute(query)

kloster_standort = []
literaturDict = {}
kloster_has_literatur = []
bibitemDict = {}
for values in cursor:
	row = dict(zip(cursor.column_names, values))
	standort_uid = row['ID_Kloster']
	kloster_uid = row['Klosternummer']
	ort_uid = row['ID_alleOrte']

	if row['Laenge']:
		row['Laenge'] = row['Laenge'].strip().replace(unichr(8206), '')

	if ort_uid and kloster_uid:
		r = {
			'uid': standort_uid,
			'kloster_uid': kloster_uid,
			'ort_uid': ort_uid,
			'gruender': row['Gruender'],
			'bemerkung': row['interne_Anmerkungen'],
			'breite': row['Breite'],
			'laenge': row['Laenge'],
			'bemerkung_standort': row['BemerkungenStandort'],
			'temp_literatur_alt': row['Literaturnachweise'],
			'crdate': klosterDict[kloster_uid]['crdate'],
			'cruser_id': klosterDict[kloster_uid]['cruser_id']
		}
		
		r2 = {
			'uid': len(zeitraum) + 1,
			'von_von': row['Standort_von_von'],
			'von_bis': row['Standort_Datum_von_bis'],
			'von_verbal': row['Standort_von_Verbal'],
			'bis_von': row['Standort_Datum_bis_von'],
			'bis_bis': row['Standort_Datum_bis_bis'],
			'bis_verbal': row['Standort_bis_Verbal'],
			'crdate': klosterDict[kloster_uid]['crdate'],
			'cruser_id': klosterDict[kloster_uid]['cruser_id']		
		}
		zeitraum += [r2]
		r['zeitraum_uid'] = r2['uid']
		kloster_standort += [r]
	
		lit = row['Literaturnachweise']
		if lit:
			lit = lit.strip(u'- −').replace(u' − ', u' - ').replace(u' — ', u' - ').replace('\r\n', ' - ').replace(u'—', ' - ').replace(u' – ', ' - ').replace(r', S[^.]', ', S.').replace(r',S.', ', S.').split(' - ')
			for litItem in lit:
				parts = litItem.strip().rsplit(', S.')
				buch = parts[0].strip()
				seite = None
				if len(parts) > 1:
					seite = 'S. ' + parts[1].strip(' .')
			
				if not bibitemDict.has_key(buch):
					r3 = {
						'uid': len(bibitemDict) + 1,
						'bibitem': buch
					}
					bibitemDict[buch] = r3
					# print u"INFO: neues Buch »" + buch + u"«"
				
				
				beschreibung = seite
				if citekeyDict.has_key(buch):
					citekey = citekeyDict[buch]['citekey']
					if citekey and citekeyDict[buch]['detail'] and citekeyDict[buch]['detail'] != u'#N/A':
						if beschreibung and citekeyDict[buch]['detail'].find(beschreibung) == -1:
							beschreibung = citekeyDict[buch]['detail'] + ', ' + beschreibung
							print u"INFO: " + str(kloster_uid) + u" Zwei Beschreibungsfelder für: »" + citekey + u"« zusammenfügen: " + beschreibung
						else:
							beschreibung = citekeyDict[buch]['detail']
				
					literaturKey = str(kloster_uid) + u"-" + citekey + u"-" + unicode(beschreibung)
					if literaturDict.has_key(literaturKey):
						print u"INFO: " + str(kloster_uid) + u" Doppelter Literaturverweis »" + literaturKey + u"«: auslassen"
					else:
						literatur_uid = len(literaturDict) + 1
						r4 = {
							'uid': literatur_uid,
							'citekey': citekey,
							'beschreibung': beschreibung,
							'crdate': klosterDict[kloster_uid]['crdate'],
							'cruser_id': klosterDict[kloster_uid]['cruser_id']
						}
						literaturDict[literaturKey] = r4
				
						kloster_has_literatur += [{
							'uid_local': kloster_uid,
							'uid_foreign': literatur_uid
						}]
				else:
					print u"FEHLER: " + str(kloster_uid) + u" Kein citekey für Buch »" + buch + u"« gefunden: auslassen"

	else:
		if not ort_uid:
			print u"FEHLER: Feld »ID_alleOrte« leer in KlosterStandort " + str(standort_uid) + ": verwerfen"
		if not kloster_uid:
			print u"FEHLER: Feld »Klosternummer« leer in KlosterStandort " + str(standort_uid) + ": verwerfen"




# Schema einrichten
f = open('schema.sql')
schema = f.read()
f.close()
schema = re.sub(r'`mydb`.`(.*)`', r'`' + writePrefix + r'domain_model_\1`' , schema)

typo3Felder = """		
		tstamp           INT(11) UNSIGNED DEFAULT '0'    NOT NULL,
		crdate           INT(11) UNSIGNED DEFAULT '0'    NOT NULL,
		cruser_id        INT(11) UNSIGNED DEFAULT '0'    NOT NULL,
		deleted          TINYINT(4) UNSIGNED DEFAULT '0' NOT NULL,
		hidden           TINYINT(4) UNSIGNED DEFAULT '0' NOT NULL,
		starttime        INT(11) UNSIGNED DEFAULT '0'    NOT NULL,
		endtime          INT(11) UNSIGNED DEFAULT '0'    NOT NULL,

		t3ver_oid        INT(11) DEFAULT '0'             NOT NULL,
		t3ver_id         INT(11) DEFAULT '0'             NOT NULL,
		t3ver_wsid       INT(11) DEFAULT '0'             NOT NULL,
		t3ver_label      VARCHAR(255) DEFAULT ''         NOT NULL,
		t3ver_state      TINYINT(4) DEFAULT '0'          NOT NULL,
		t3ver_stage      INT(11) DEFAULT '0'             NOT NULL,
		t3ver_count      INT(11) DEFAULT '0'             NOT NULL,
		t3ver_tstamp     INT(11) DEFAULT '0'             NOT NULL,
		t3ver_move_id    INT(11) DEFAULT '0'             NOT NULL,

		t3_origuid       INT(11) DEFAULT '0'             NOT NULL,
		sys_language_uid INT(11) DEFAULT '0'             NOT NULL,
		l10n_parent      INT(11) DEFAULT '0'             NOT NULL,
		l10n_diffsource  MEDIUMBLOB,
		
		pid              INT(11) DEFAULT '0'             NOT NULL,

		PRIMARY KEY (`uid`)"""

schema = schema.replace('PRIMARY KEY (`uid`)', typo3Felder)
schema = re.sub(r'DROP .*`' + writePrefix + r'domain_model_([a-z_]+)_has_([a-z_]+)\`.*\n\n.*' + writePrefix + r'domain_model_\1_has_\2\`',
	r'DROP TABLE IF EXISTS `' + writePrefix + r'\1_\2_mm`;\n\n CREATE TABLE IF NOT EXISTS `' + writePrefix + r'\1_\2_mm`',
	schema)
#print schema
for result in cursor.execute(schema, multi=True):
	1
	#print result

db.commit()


# Daten in Datenbank einspielen

url = urlDict.values()
addRecordsToTable(url, 'url')

addRecordsToTable(zeitraum, 'zeitraum')

bistum = bistumDict.values()
addRecordsToTable(bistum, 'bistum')
bistum_has_url = bistum_has_urlDict.values()
addRecordsToTable(bistum_has_url, 'bistum_url_mm')

addRecordsToTable(band, 'band')
band_has_url = band_has_urlDict.values()
addRecordsToTable(band_has_url, 'band_url_mm')

bearbeitungsstatus = []
for status in bearbeitungsstatusDict:
	bearbeitungsstatus += [{'uid': bearbeitungsstatusDict[status], 'name': status}]
addRecordsToTable(bearbeitungsstatus, 'bearbeitungsstatus')
personallistenstatus = personallistenstatusDict.values()
addRecordsToTable(personallistenstatus, 'personallistenstatus')

kloster = klosterDict.values()
addRecordsToTable(kloster, 'kloster')
kloster_has_url = kloster_has_urlDict.values()
addRecordsToTable(kloster_has_url, 'kloster_url_mm')

ordenstyp = ordenstypDict.values()
addRecordsToTable(ordenstyp, 'ordenstyp')
klosterstatus = klosterstatusDict.values()
addRecordsToTable(klosterstatus, 'klosterstatus')
addRecordsToTable(orden, 'orden')
addRecordsToTable(kloster_orden, 'kloster_orden')
orden_has_url = orden_has_urlDict.values()
addRecordsToTable(orden_has_url, 'orden_url_mm')

addRecordsToTable(land, 'land')
addRecordsToTable(ort, 'ort')
ort_has_url = ort_has_urlDict.values()
addRecordsToTable(ort_has_url, 'ort_url_mm')

literatur = literaturDict.values()
addRecordsToTable(literatur, 'literatur')
addRecordsToTable(kloster_standort, 'kloster_standort')
addRecordsToTable(kloster_has_literatur, 'kloster_literatur_mm')



cursor.close()
db.close()
