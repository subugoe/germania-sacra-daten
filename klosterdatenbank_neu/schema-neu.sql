-- phpMyAdmin SQL Dump
-- version 4.1.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 18. Jun 2014 um 16:25
-- Server Version: 5.5.37-0ubuntu0.12.04.1
-- PHP-Version: 5.5.12-2+deb.sury.org~precise+1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `germania`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_band`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_band`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_band` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `bistum` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `nummer` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sortierung` int(11) NOT NULL,
  `titel` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `kurztitel` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`),
  KEY `IDX_BC13F9E62BE54566` (`bistum`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=75 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_bandhasurl`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_bandhasurl`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_bandhasurl` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `band` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  KEY `IDX_885BD41148DFA2EB` (`band`),
  KEY `IDX_885BD411F47645AE` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_bearbeiter`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_bearbeiter`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_bearbeiter` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `bearbeiter` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=12 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_bearbeitungsstatus`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_bearbeitungsstatus`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_bearbeitungsstatus` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=8 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_bibitem`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_bibitem`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_bibitem` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `bibitem` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=250 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_bistum`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_bistum`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_bistum` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `ort` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `bistum` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `kirchenprovinz` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bemerkung` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ist_erzbistum` int(11) DEFAULT NULL,
  `shapefile` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`),
  UNIQUE KEY `UNIQ_62F2479BF6ABFB5E` (`ort`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=76 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_bistumhasurl`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_bistumhasurl`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_bistumhasurl` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `bistum` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  KEY `IDX_79C4421C2BE54566` (`bistum`),
  KEY `IDX_79C4421CF47645AE` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_kloster`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_kloster`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_kloster` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `bearbeitungsstatus` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `bearbeiter` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `personallistenstatus` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `band` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `kloster_id` int(11) DEFAULT NULL,
  `kloster` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `patrozinium` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bemerkung` longtext COLLATE utf8_unicode_ci,
  `band_seite` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `text_gs_band` longtext COLLATE utf8_unicode_ci,
  `bearbeitungsstand` longtext COLLATE utf8_unicode_ci,
  `creationdate` datetime NOT NULL,
  `changeddate` datetime DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`),
  KEY `IDX_3F3F3173F77E4657` (`bearbeitungsstatus`),
  KEY `IDX_3F3F3173E063B86C` (`bearbeiter`),
  KEY `IDX_3F3F3173CC4E7F70` (`personallistenstatus`),
  KEY `IDX_3F3F317348DFA2EB` (`band`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3575 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_klosterhasliteratur`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_klosterhasliteratur`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_klosterhasliteratur` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `kloster` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `literatur` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  KEY `IDX_81316783FC7AA8D0` (`kloster`),
  KEY `IDX_813167836CD7C9B9` (`literatur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_klosterhasurl`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_klosterhasurl`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_klosterhasurl` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `kloster` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  KEY `IDX_150245A4FC7AA8D0` (`kloster`),
  KEY `IDX_150245A4F47645AE` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_klosterorden`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_klosterorden`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_klosterorden` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `kloster` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `orden` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `klosterstatus` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `von_von` int(11) DEFAULT NULL,
  `von_bis` int(11) DEFAULT NULL,
  `von_verbal` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bis_von` int(11) DEFAULT NULL,
  `bis_bis` int(11) DEFAULT NULL,
  `bis_verbal` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bemerkung` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`),
  KEY `IDX_6024429DFC7AA8D0` (`kloster`),
  KEY `IDX_6024429DE128CFD7` (`orden`),
  KEY `IDX_6024429D91356728` (`klosterstatus`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2435 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_klosterstandort`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_klosterstandort`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_klosterstandort` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `kloster` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ort` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `von_von` int(11) DEFAULT NULL,
  `von_bis` int(11) DEFAULT NULL,
  `von_verbal` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bis_von` int(11) DEFAULT NULL,
  `bis_bis` int(11) DEFAULT NULL,
  `bis_verbal` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gruender` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bemerkung` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `breite` double DEFAULT NULL,
  `laenge` double DEFAULT NULL,
  `bemerkung_standort` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `temp_literatur_alt` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`),
  KEY `IDX_FD484853FC7AA8D0` (`kloster`),
  KEY `IDX_FD484853F6ABFB5E` (`ort`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2020 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_klosterstatus`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_klosterstatus`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_klosterstatus` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=13 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_land`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_land`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_land` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `land` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ist_in_deutschland` int(11) DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=79 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_literatur`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_literatur`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_literatur` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `citekey` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `beschreibung` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1891 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_orden`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_orden`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_orden` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `ordenstyp` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `orden` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ordo` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `symbol` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `graphik` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`),
  KEY `IDX_9F6D7F31EEE8F78` (`ordenstyp`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=77 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_ordenhasurl`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_ordenhasurl`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_ordenhasurl` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `orden` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  KEY `IDX_82D92A2E128CFD7` (`orden`),
  KEY `IDX_82D92A2F47645AE` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_ordenstyp`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_ordenstyp`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_ordenstyp` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `ordenstyp` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_ort`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_ort`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_ort` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `land` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bistum` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `ort` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `gemeinde` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `kreis` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `wuestung` int(11) DEFAULT NULL,
  `breite` double DEFAULT NULL,
  `laenge` double DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`),
  KEY `IDX_EE45A748A800D5D8` (`land`),
  KEY `IDX_EE45A7482BE54566` (`bistum`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=46479326 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_orthasurl`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_orthasurl`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_orthasurl` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `ort` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  KEY `IDX_AD307F85F6ABFB5E` (`ort`),
  KEY `IDX_AD307F85F47645AE` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_personallistenstatus`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_personallistenstatus`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_personallistenstatus` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_url`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_url`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_url` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `urltyp` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `bemerkung` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`),
  KEY `IDX_EC9819B8E5CFB5CA` (`urltyp`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=911 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subugoe_germaniasacra_domain_model_urltyp`
--

DROP TABLE IF EXISTS `subugoe_germaniasacra_domain_model_urltyp`;
CREATE TABLE IF NOT EXISTS `subugoe_germaniasacra_domain_model_urltyp` (
  `persistence_object_identifier` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`persistence_object_identifier`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=8 ;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_band`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_band`
  ADD CONSTRAINT `FK_BC13F9E62BE54566` FOREIGN KEY (`bistum`) REFERENCES `subugoe_germaniasacra_domain_model_bistum` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_bandhasurl`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_bandhasurl`
  ADD CONSTRAINT `FK_885BD41148DFA2EB` FOREIGN KEY (`band`) REFERENCES `subugoe_germaniasacra_domain_model_band` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_885BD411F47645AE` FOREIGN KEY (`url`) REFERENCES `subugoe_germaniasacra_domain_model_url` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_bistum`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_bistum`
  ADD CONSTRAINT `FK_62F2479BF6ABFB5E` FOREIGN KEY (`ort`) REFERENCES `subugoe_germaniasacra_domain_model_ort` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_bistumhasurl`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_bistumhasurl`
  ADD CONSTRAINT `FK_79C4421C2BE54566` FOREIGN KEY (`bistum`) REFERENCES `subugoe_germaniasacra_domain_model_bistum` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_79C4421CF47645AE` FOREIGN KEY (`url`) REFERENCES `subugoe_germaniasacra_domain_model_url` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_kloster`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_kloster`
  ADD CONSTRAINT `FK_3F3F317348DFA2EB` FOREIGN KEY (`band`) REFERENCES `subugoe_germaniasacra_domain_model_band` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_3F3F3173CC4E7F70` FOREIGN KEY (`personallistenstatus`) REFERENCES `subugoe_germaniasacra_domain_model_personallistenstatus` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_3F3F3173E063B86C` FOREIGN KEY (`bearbeiter`) REFERENCES `subugoe_germaniasacra_domain_model_bearbeiter` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_3F3F3173F77E4657` FOREIGN KEY (`bearbeitungsstatus`) REFERENCES `subugoe_germaniasacra_domain_model_bearbeitungsstatus` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_klosterhasliteratur`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_klosterhasliteratur`
  ADD CONSTRAINT `FK_813167836CD7C9B9` FOREIGN KEY (`literatur`) REFERENCES `subugoe_germaniasacra_domain_model_literatur` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_81316783FC7AA8D0` FOREIGN KEY (`kloster`) REFERENCES `subugoe_germaniasacra_domain_model_kloster` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_klosterhasurl`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_klosterhasurl`
  ADD CONSTRAINT `FK_150245A4F47645AE` FOREIGN KEY (`url`) REFERENCES `subugoe_germaniasacra_domain_model_url` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_150245A4FC7AA8D0` FOREIGN KEY (`kloster`) REFERENCES `subugoe_germaniasacra_domain_model_kloster` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_klosterorden`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_klosterorden`
  ADD CONSTRAINT `FK_6024429D91356728` FOREIGN KEY (`klosterstatus`) REFERENCES `subugoe_germaniasacra_domain_model_klosterstatus` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_6024429DE128CFD7` FOREIGN KEY (`orden`) REFERENCES `subugoe_germaniasacra_domain_model_orden` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_6024429DFC7AA8D0` FOREIGN KEY (`kloster`) REFERENCES `subugoe_germaniasacra_domain_model_kloster` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_klosterstandort`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_klosterstandort`
  ADD CONSTRAINT `FK_FD484853F6ABFB5E` FOREIGN KEY (`ort`) REFERENCES `subugoe_germaniasacra_domain_model_ort` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_FD484853FC7AA8D0` FOREIGN KEY (`kloster`) REFERENCES `subugoe_germaniasacra_domain_model_kloster` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_orden`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_orden`
  ADD CONSTRAINT `FK_9F6D7F31EEE8F78` FOREIGN KEY (`ordenstyp`) REFERENCES `subugoe_germaniasacra_domain_model_ordenstyp` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_ordenhasurl`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_ordenhasurl`
  ADD CONSTRAINT `FK_82D92A2E128CFD7` FOREIGN KEY (`orden`) REFERENCES `subugoe_germaniasacra_domain_model_orden` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_82D92A2F47645AE` FOREIGN KEY (`url`) REFERENCES `subugoe_germaniasacra_domain_model_url` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_ort`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_ort`
  ADD CONSTRAINT `FK_EE45A7482BE54566` FOREIGN KEY (`bistum`) REFERENCES `subugoe_germaniasacra_domain_model_bistum` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_EE45A748A800D5D8` FOREIGN KEY (`land`) REFERENCES `subugoe_germaniasacra_domain_model_land` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_orthasurl`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_orthasurl`
  ADD CONSTRAINT `FK_AD307F85F47645AE` FOREIGN KEY (`url`) REFERENCES `subugoe_germaniasacra_domain_model_url` (`persistence_object_identifier`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_AD307F85F6ABFB5E` FOREIGN KEY (`ort`) REFERENCES `subugoe_germaniasacra_domain_model_ort` (`persistence_object_identifier`) ON DELETE NO ACTION;

--
-- Constraints der Tabelle `subugoe_germaniasacra_domain_model_url`
--
ALTER TABLE `subugoe_germaniasacra_domain_model_url`
  ADD CONSTRAINT `FK_EC9819B8E5CFB5CA` FOREIGN KEY (`urltyp`) REFERENCES `subugoe_germaniasacra_domain_model_urltyp` (`persistence_object_identifier`) ON DELETE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
