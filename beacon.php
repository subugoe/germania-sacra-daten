<?php
setlocale(LC_ALL, 'de_DE.utf8');

$sqlServer = '127.0.0.1';
$sqlUsername = 'root';
$sqlPassword = '';
$sqlDatabase = 'personen';

$sql = mysql_connect($sqlServer, $sqlUsername, $sqlPassword);
mysql_set_charset('utf8', $sql);

header("Content-Type: text/plain; charset=utf-8");


if ($sql) {
	if (mysql_select_db($sqlDatabase)) {
		$beacon = "#FORMAT: BEACON
#VERSION: 0.1
#PREFIX: http://d-nb.info/gnd/
#TARGET: http://personendatenbank.germania-sacra.de/index/gnd/{ID}
#FEED: http://personendatenbank.germania-sacra.de/beacon.txt
#NAME: Germania Sacra Personendatenbank
#DESCRIPTION: 
#INSTITUTION: Germania Sacra, Akademie der Wissenschaften zu Göttingen
#CONTACT: bkroege@gwdg.de\n";

		date_default_timezone_set('CET');
		$date = new DateTime();
		$beacon .= "#TIMESTAMP:" . $date->format('c') . "\n";

		$query = "SELECT `persons`.`gndnummer`
					FROM items, persons
					WHERE ((`items`.`status` = 'online')
					AND (`items`.`art` = 'Person')
					AND (`persons`.`gndnummer` <> '')
					AND (`items`.`deleted` = '0')
					AND (`persons`.`deleted` = '0') 
					AND (`items`.`id` =`persons`.`item_id`))
				";
		
		$sql_result = mysql_query($query, $sql);
		
		while ($row = mysql_fetch_array($sql_result, MYSQL_ASSOC)) {
			$beacon .= $row['gndnummer'] . "\n";
		}
		
		$beaconPath = dirname(__FILE__) . '/beacon.txt';
		if (file_put_contents($beaconPath, $beacon)) {
			echo('Beacon Datei nach beacon.txt geschrieben.');
		}
		else {
			echo('Beacon Datei konnte nicht nach beacon.txt geschrieben werden.');
		}
	else {
		echo "Kein Zugriff auf Datenbank »" . $sqlDatabase . "«.\n";
	}
	mysql_close($sql);
}
else {
	echo "Keine Verbindung zum MySQL Server »" . $sqlServer . "«.\n";
}
?>