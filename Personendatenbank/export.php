#!/usr/bin/env php -f
# Skript zum Export der relevanten Personendaten aus der Personendatenbank
# zur Anreicherung des Indexed der Klosterdatenbank.
# 
# Exportiert werden Daten zu Ämtern, die mit einer Klosternummer versehen sind.
# Die Daten sind ein JSON Objekt der Form:
# {
#	KLOSTERNUMMER: [
#		{ PERSONENINFORMATIONEN }, 
#		…
#	],
#	…
# }
# das in die Datei »export.json« geschrieben wird.
#
# 2013 Sven-S. Porst, SUB Göttingen (porst@sub.uni-goettingen.de)
#
<?php
	$sqlServer = '127.0.0.1';
	$sqlUsername = 'root';
	$sqlDatabase = 'personen';
	
	$sql = mysql_connect($sqlServer, $sqlUsername);
	
	function improveYear ($yearString) {
		$matches = array();
		
		if (preg_match('/([0-9]{3,4})/', $yearString, $matches)) {
			$result = (int)$matches[1];
		}
		else if (preg_match('/Mitte ([0-9]+)\. J/', $yearString, $matches)) {
			$result = ((int)$matches[1]) * 100 - 50;
		}
		else if (preg_match('/Ende ([0-9]+)\. J/', $yearString, $matches)) {
			$result = ((int)$matches[1]) * 100;
		}
		else if (preg_match('/2. Hälfte ([0-9]+)\. J/', $yearString, $matches)) {
			$result = ((int)$matches[1]) * 100 - 25;
		}
		else if (preg_match('/1. Hälfte ([0-9]+)\. J/', $yearString, $matches)) {
			$result = ((int)$matches[1]) * 100 - 75;
		}
		else if (preg_match('/Anfang ([0-9]+)\. J/', $yearString, $matches)) {
			$result = ((int)$matches[1]) * 100 - 100;
		}
		else if (preg_match('/([0-9]+)\. J/', $yearString, $matches)) {
			$result = ((int)$matches[1]) * 100 - 50;
		}
		else {
			$result = 0;
		}

		return $result;		
	}


	function klosterinfocompare ($a, $b) {
		$aString = $a['person_bezeichnung'] . '-' . str_pad($a['person_von'], 4, '0') . '-' . str_pad($a['person_bis'], 4, '0') . '-' . $a['person_vorname'];
		$bString = $b['person_bezeichnung'] . '-' . str_pad($b['person_von'], 4, '0') . '-' . str_pad($b['person_bis'], 4, '0') . '-' . $b['person_vorname'];
		return strcmp($aString, $bString);
	}


	if ($sql) {
		if (mysql_select_db($sqlDatabase)) {
			$query = '
			SELECT
				vorname, vornamenvarianten, familienname, familiennamenvarianten, titel, namenspraefix, namenszusatz, persons.item_id AS person_id, gsonummer, gndnummer,
				offices.id AS office_id, bezeichnung, klosterid, von, bis, anmerkung
			FROM
				persons, offices
			WHERE
				offices.person_id = persons.id AND
				offices.klosterid != ""
			ORDER BY
				klosterid	
			';
			$sql_result = mysql_query($query, $sql);

			if ($sql_result) {
				$results = array();
	
				while ($row = mysql_fetch_array($sql_result, MYSQL_ASSOC)) {
					$personeninfo = Array('person_vorname' => $row['vorname']);
					$namensteile = Array();
					if ($row["titel"]) { $namensteile[] = $row["titel"]; }
					if ($row["vorname"]) { $namensteile[] = $row["vorname"]; }
					if ($row["namenspraefix"]) { $namensteile[] = $row["namenspraefix"]; }
					if ($row["familienname"]) { $namensteile[] = $row["familienname"]; }
					if ($row["namenszusatz"]) { $namensteile[] = $row["namenszusatz"]; }
					$personeninfo['person_name'] = implode(' ', $namensteile);
		
					$namensalternativenteile = Array();
					if ($row["vornamenvarianten"]) { $namensalternativenteile[] = $row["vornamenvarianten"]; }
					if ($row["familiennamenvarianten"]) { $namensalternativenteile[] = $row["familiennamenvarianten"]; }
					$personeninfo['person_namensalternativen'] = implode('; ', $namensalternativenteile);
		
					// $personeninfo['person_id'] = $row['person_id'];
					$GSOs = array_filter(array_unique(explode('; ', $row['gsonummer'])));
					if (count($GSOs) > 0) {
						$personeninfo['person_gso'] = $GSOs[0];
					}
					else {
						$personeninfo['person_gso'] = '';
					}
					$GNDs = array_filter(array_unique(explode('; ', $row['gndnummer'])));
					if (count($GNDs) > 0) {
						$personeninfo['person_gnd'] = $GNDs[0];
					}
					else {
						$personeninfo['person_gnd'] = '';
					}
		
					// $personeninfo['person_office_id'] = $row['office_id'];
					$personeninfo['person_bezeichnung'] = $row['bezeichnung'];
					$personeninfo['person_anmerkung'] = $row['anmerkung'];

					$personeninfo['person_von_verbal'] = $row['von'];
					$personeninfo['person_von'] = improveYear($row['von']);
					$personeninfo['person_bis_verbal'] = $row['bis'];
					$personeninfo['person_bis'] = improveYear($row['bis']);

					if (!array_key_exists($row['klosterid'], $results)) {
						$results[$row['klosterid']] = array();
					}
					
					$results[$row['klosterid']][] = $personeninfo;
				}
		
				foreach ($results as &$result) {
					usort($result, 'klosterinfocompare');
				}
	
				$json = json_encode($results);
				$jsonPath = dirname(__FILE__) . '/export.json';
				file_put_contents($jsonPath, $json);
			}
			else {
				echo "Keine Ergebnisse für die SQL Abfrage.";
			}
		}
		else {
			echo "Kein Zugriff auf Datenbank »" . $sqlDatabase . "«.";
		}
		mysql_close($sql);
	}
	else {
		echo "Keine Verbindung zum SQL Server »" . $sqlServer . "«.";
	}
?>