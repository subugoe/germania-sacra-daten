# Konversion der Daten
Das Konversionsskript [convert.py](convert.py) bereitet die Daten aus dem MS Access Dump für das verbesserte Datenschema auf.

Es benötigt:

* einige Python Module, z.B. mysql.connector (siehe die imports am Anfang des Skripts)
* den importierten MS Access SQL Dump in der Datenbank »Klosterdatenbank« in MySQL (host:127.0.0.1, user:root, einstellbar am Anfang des Skripts)
* die Möglichkeit, das Konversionsergebnis in die Tabelle »kloster« des MySQL Servers zu schreiben
* das SQL Schema der Zieldatenbank in [schema.sql](schema.sql)


## Zielschema
Das Zieldatenbankschema wurde mit MySQLWorkbench erstellt. Zugehörige Dateien sind:

* [klosterdatenbank.mwb](klosterdatenbank.mwb) – MySQLWorkbench Datei
* [schema.sql](schema.sql) – SQL Schema, vom Importskript benötigt
* [schema.pdf](schema.pdf) – graphische Darstellung des SQL Schemas

Die TYPO3 spezifischen Felder sind nicht in dem Datenbankschema enthalten. Wegen ihrer großen Zahl und Redundanz fügt das Konversionsskript sie zu den Tabellen hinzu und wandelt dabei die verschiedenen Namenskonventionen für Tabellen ineinander um (Präfix `tx_gs_` und ggf `model_domain`, bzw. Suffix `_mm`).

## Bearbeiter
Das Konversionsskript enthält ein dictionary `bearbeiterDict` der Bearbeiter und bildet die Access IDs auf die IDs der entsprechenden TYPO3 Nutzerkonten ab.

## Bearbeitungsstatus
Das Konversionsskript enthält ein dictionary `bearbeitungsstatusDict` von Bearbeitungsstatus, die den vorkommenden Freitexen im Dump entspricht.

## Änderungsdaten
Das Konversionsskript versucht, die Änderungsdaten – falls vorhanden – aus den Access Datensätzen zu übernehmen. Falls ein Datensatz kein Datum hat, aber zu einem anderen Datensatz gehört, wird dessen Datum genutzt, ansonsten der 1.1.2000.

## Literaturimport
In den Access Daten stehen die Literaturverweise als Freitext. Das Importskript versucht:

* mehrere Einträge im Feld `tblKlosterStandort.Literaturnachweise` zu trennen
* Seiten-/Artikelangaben am Ende des Literaturverweises abzutrennen
* den reinen Literaturverweis in der Datei [GS-citekeys.csv](GS-citekeys.csv) zu finden
	* diese Datei entstand aus Bereinigungsarbeiten bei in der Tabelle [Germania Sacra Literatur](https://docs.google.com/spreadsheet/ccc?key=0Ah9t1ddBuxv8dEluYUg3OHBQUms1Z3ljV29EQmFpUWc&usp=drive_web/)
	* die Datei bildet den Freitext der Bibliographieeinträge auf die entsprechenden citekeys der BibTeX Datei [klosterdatenbankGS.bib] ab (die im TYPO3 System mit in die [bib Extension](https://github.com/subugoe/typo3-bib) importiert wird)

Es gibt also folgende Zusammenhänge:

* Access: Freitext
	* hieraus entsteht durch Magie und Geduld die Google Tabelle
* Google Tabelle: Freitext → citekeys
	* Der Export dieser Tabelle ist in der Datei [GS-citekeys.csv](GS-citekeys.csv)
* BibTeX Datei: citekeys → Literaturangabe
* Klosterdatensätze verweisen auf Datensätze der Tabelle »literatur«. Diese enthalten die citekeys und stellen so die Verbindung zur Bibliographie her
* Die citekeys werden im Index gespeichert und genutzt um die Bibliographiedatensätze für die Anzeige von der bib Extension laden zu lassen


## URLs
Die einfachen URL Felder in den Originaldaten wurden durch ein flexibleres System ersetzt: Datensätze können so mit beliebig vielen URLs verbunden werden. Jede URL ist dabei mit einem `typ` getaggt und kann mit einer `bemerkung` (z.B. Anzeigestring) versehen sein.

## Logging
Das Importskript loggt Problemfälle, die beim Import auftreten können, und allgemeine Informationen zum Datenimport in die Konsole. Das Log liegt als [convert.log](convert.log) vor. Importprobleme sind je nach Schwere mit INFO, WARNUNG oder FEHLER versehen.





# Indexierung der Daten
Das Indexierungsskrip ist [index.py](index.py). Es erzeugt einen [Solr](http://lucene.apache.org/solr/) Index aus den konvertierten MySQL Daten.

Es benötigt:
* einige Python Module, z.B. mysql.connector, python-geohash, json, solrpy (siehe die Imports am Anfang des Skripts)
* Zugriff auf MySQL mit den konvertierten Daten in der Datenbank »kloster« (host:127.0.0.1, user:root, einstellbar am Anfang des Skripts)
* Schreibzugriff auf den Ziel Solr Index (konfiguriert am Ende des Skriptes, es wird in zwei Indexe indexiert)
* die zugehörigen Personendaten als JSON


## Solr Konfiguration
Die zugehörige Solr Konfiguration liegt unter [../solr/conf](../solr/conf). Sie beinhaltet das [Schema](../solr/conf/schema.xml) und die [solrconfig](../solr/conf/solrconfig.xml) mit Einstellungen für Autocomplete/Spellchecker. Sie ist getestet mit Solr 4.5.


## Anreicherung mit Personendaten
Die zu einem Kloster gehörenden Personen werden auf der Seite des Klosters angezeigt. Da sie getrennt in der [Personendatenbank](http://personendatenbank.germania-sacra.de) erfaßt sind, werden sie zunächst von dort geladen. 

Das Indexierungsskript lädt die [JSON Datei](../Personendatenbank/export.json) herunter, erstellt eine [lesbare Version](../Personendatenbank/export-pp.json) von ihr (nutzt das Skript json_pp im Pfad, dieser Schritt ist nicht nötig, aber wegen der besseren Diffbarkeit beim Testen hilfreich) und liest sie dann ein, um dem Indexdokument jedes Klosters seine Personen hinzuzufügen.


## Ausmultiplizieren der Daten
Das Datenmodell von Germania Sacra erfaßt für jedes Kloster sowohl Standorte als auch Ordenszugehörigkeiten mit den jeweiligen Zeiträumen. Es sollen Abfragen und Filter sowohl nach Standort, Orden als auch nach den Zeiträumen möglich und kombinierbar sein.

Mit dem »flachen« Dokumentenmodell von Solr ist dies nicht möglich, da z.B. ein Kloster mit

* 1200-1400 Kanoniker
* 1400-1600 Benediktiner

auch als Ergebnis zu einer Abfrage nach »Benediktinern um 1300« erschiene. Um diese Abfragen trotz der »flachen« Dokumente von Solr zu ermöglichen werden für jedes Kloster mehrere Datensätze erzeug, die sich im Feld »typ« unterscheiden. Es gibt die Werte:

* kloster: Informationen zum Kloster mit allen Standorten und Ordenszugehörigkeiten
* kloster-standort: Informationen zum Kloster mit einem Standort
* kloster-orden: Informationen zum Kloster mit einer Ordenszugehörigkeit
* standort-orden: »Produkt« von kloster-standort und kloster-orden

Zur Produktbildung werden alle Zeiträume der Standort- und Ordenszugehörigkeiten in die größtmöglichen von-bis Bereiche mit einem Standort und Orden zerlegt. Dies macht die Abfragen etwas undurchsichtig: Abfragen finden auf Dokumenten mit typ:standort-orden statt. Die Ergebnisse werden mit `{!join}` auf den zugehörigen Datensatz mit typ:kloster abgebildet (und dadurch wenn nötig dedupliziert). Die Standardabfrage ist also `{!join from=kloster_id to=id}(%s AND typ:standort-orden)`.

Die Facettenbildung nutzt ebenfalls diesen Mechanismus für die Abfrage. Da Solr aber die Zählung der Facetten erst _nach_ dem `{!join}` durchführt, kann die angezeigte Anzahl etwas zu hoch sein, weil auch Ordenszugehörigkeiten aus dem falschen Zeitraum mit im Dokument stehen (ich sehe dafür keine Lösungsmöglichkeit).

Hier würde ein hierarchisches Datenmodell sowohl die Indexerstellung als auch die Abfragen wesentlich vereinfachen. [elasticsearch](http://www.elasticsearch.org/) bietet solche Möglichkeiten. Die SUB will es momentan aber nicht einsetzen.


## Automatische Indexierung
Dieses Skript erstellt den Index vollständig neu. Für den regulären Betrieb, in dem Daten in TYPO3 bearbeitet werden und sofort im Index abfragbar sein sollen ist es nötig, die Konversion granularer auszuführen und nur das neue/geänderte/gelöschte Dokument, sowie die davon abhängigen Dokumente im Index zu aktualisieren. Die Überprüfung der Abhängigkeiten und die Löschfunktion ist in diesem Skript noch nicht vorhanden.

Änderungen an der Personendatenbank werden – da sie vollkommen unabhängig ist – auch nicht automatisch gemerkt. Vermutlich wird es reichen, den Index ab und an mit einer frischen Kopie der Personendaten komplett neu aufzubauen.


## Logging
Das Indexierungsskript loggt Probleme in die Konsole. Das Log liegt als index.log vor und sollte leer sein.
