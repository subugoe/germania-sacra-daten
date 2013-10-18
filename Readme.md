# Germania Sacra Daten
Dateien und Skripte zur Bearbeitung der Germania Sacra (Kloster)-Daten


## Ziel
Die Germania Sacra Klosterdaten liegen in einer MS Access Datenbank vor. Ziel ist es, sie auf der TYPO3 Website der AdW im Web verfüg- und bearbeitbar zu machen. Schritte dazu:

* Export des Dumps aus MS Access
* Einlesen des Dumps in MySQL und:
	* Korrektur der bekannten Fehler im Dump
	* Verbesserung der Normalisierung
	* Anpassung an die Tabellenformate von TYPO3
* Erstellung eines Solr Index aus den Daten
	* dabei: Anreicherung mit Daten aus der Personendatenbank
* Darstellung der Solr Dokumente durch TYPO3
	* dabei: Anreicherung mit Literaturdaten


## Weitere Informationen
* zu Konversion und Indexierung der Daten: [klosterdatenbank_neu](klosterdatenbank_neu)
* zur Integration der Personendaten in den Index: [Personendatenbank](Personendatenbank)


## Unterordner
* [Bistumsgrenzen](Bistumsgrenzen): Geodaten mit den Bistumsgrenzen in verschiedenen Dateiformaten
* HelvetiaSacra: alte FileMaker Datenbank zu Schweizer Klöstern (submodule, nicht öffentlich)
* [Karten Wikipedia](Karten Wikipedia): Skript zum Laden von Kloster Geodaten aus dem Wikimedia Toolserver
* Klosterdatenbank: SQL Dump aus MS Access und Beschreibung des Datenmodells (nicht öffentlich)
* [klosterdatenbank_neu](klosterdatenbank_neu): Skripte für Konversion und Indexierung der Daten (mit eigenen Readme)
* [Klostersymbole](Klostersymbole): SVG Graphiken mit Symbolen für die verschiedenen Orden
* [Personendatenbank](Personendatenbank): Dateien für den Export der Personendatenbank (mit eigenem Readme)
* [solr](solr): Konfiguration für den Solr Index der Klosterdatenbank