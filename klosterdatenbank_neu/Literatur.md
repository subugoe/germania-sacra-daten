# Anpassung / Hinzufügen von Literatureinträgen

Bis zur fertigen Eingabeapplikation der Daten müssen die Literaturdaten an mehreren Stellen gepflegt werden.

## Anzeige der Daten im ADW Portal

Für die Anzeige der Daten im ADW Portal ist die BibTeX Datei maßgebend. Diese wird von angemeldeten Benutzer hochgeladen und enthält neben den CiteKeys weitere Informationen zur Literatur.
Damit die korrekten Datensätze angezeigt werden müssen die beim Import auseinandergetrennten Citekeys aus der Access Datenbank ein Äquivalent in der BibTeX Datei besitzen.

Diese Äquivalente werden über die CSV Datei GS-citekeys.csv hergestellt. Aufgebaut ist die Datei nach dem Spaltenschema

"uid","titel","citekey","detail","kommentar","bib Datei","Klosternr"

Die letzte Spalte (Klosternr) findet beim Importvorgang keine Berücksichtigung.

## Literaturimport aus Access

Bei der Konvertierung der Daten aus dem Ursprungsschema in das normalisierte Schema werden die Äquivalente der Daten aus dem Access und der CSV überprüft.
Ist im convert.log ein Eintrag zu finden wie

"FEHLER: 860 Kein citekey für Buch Streich 2011 gefunden: auslassen"

Existiert dieser Eintrag nicht in der CSV Datei und muss dort entsprechend ergänzt werden. Evtl. handelt es sich auch um eine andere Schreibweise, so dass die Daten in der CSV oder im Access angepasst werden müssen.
Zusätzlich müssen fehlende Einträge auch in der BibTeX Datei hinzugefügt werden. Dabei muss der CiteKey mit dem im Access / CSV übereinstimmen.
