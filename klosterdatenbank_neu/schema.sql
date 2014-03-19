SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `mydb` ;
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`ordenstyp`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`ordenstyp` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`ordenstyp` (
  `uid` INT NOT NULL ,
  `ordenstyp` VARCHAR(255) NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`orden`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`orden` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`orden` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `orden` VARCHAR(255) NULL ,
  `ordo` VARCHAR(45) NULL ,
  `symbol` VARCHAR(45) NULL ,
  `graphik` VARCHAR(45) NULL ,
  `ordenstyp_uid` INT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) ,
  INDEX `fk_orden_ordenstyp_idx` (`ordenstyp_uid` ASC) ,
  CONSTRAINT `fk_orden_ordenstyp`
    FOREIGN KEY (`ordenstyp_uid` )
    REFERENCES `mydb`.`ordenstyp` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`land`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`land` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`land` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `land` VARCHAR(255) NULL ,
  `ist_in_deutschland` TINYINT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ort`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`ort` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`ort` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `ort` VARCHAR(255) NULL ,
  `gemeinde` VARCHAR(255) NULL ,
  `kreis` VARCHAR(255) NULL ,
  `land_uid` INT NULL ,
  `wuestung` TINYINT NULL ,
  `breite` FLOAT NULL ,
  `laenge` FLOAT NULL ,
  `bistum_uid` INT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) ,
  INDEX `fk_ort_bundesland1_idx` (`land_uid` ASC) ,
  INDEX `fk_ort_bistum1_idx` (`bistum_uid` ASC) ,
  CONSTRAINT `fk_ort_bundesland1`
    FOREIGN KEY (`land_uid` )
    REFERENCES `mydb`.`land` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ort_bistum1`
    FOREIGN KEY (`bistum_uid` )
    REFERENCES `mydb`.`bistum` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`bistum`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`bistum` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`bistum` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `bistum` VARCHAR(255) NULL ,
  `kirchenprovinz` VARCHAR(255) NULL ,
  `bemerkung` TEXT NULL ,
  `ist_erzbistum` TINYINT NULL ,
  `shapefile` VARCHAR(255) NULL ,
  `ort_uid` INT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) ,
  INDEX `fk_bistum_ort1_idx` (`ort_uid` ASC) ,
  CONSTRAINT `fk_bistum_ort1`
    FOREIGN KEY (`ort_uid` )
    REFERENCES `mydb`.`ort` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`band`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`band` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`band` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `nummer` VARCHAR(255) NULL ,
  `sortierung` INT NOT NULL ,
  `titel` TEXT NULL ,
  `kurztitel` TEXT NULL ,
  `bistum_uid` INT NOT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) ,
  INDEX `fk_band_bistum1_idx` (`bistum_uid` ASC) ,
  CONSTRAINT `fk_band_bistum1`
    FOREIGN KEY (`bistum_uid` )
    REFERENCES `mydb`.`bistum` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`personallistenstatus`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`personallistenstatus` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`personallistenstatus` (
  `uid` INT NOT NULL ,
  `name` VARCHAR(255) NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`bearbeitungsstatus`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`bearbeitungsstatus` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`bearbeitungsstatus` (
  `uid` INT NOT NULL ,
  `name` VARCHAR(45) NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`kloster`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`kloster` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`kloster` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `kloster_id` INT NOT NULL ,
  `kloster` VARCHAR(255) NULL ,
  `patrozinium` VARCHAR(255) NULL ,
  `bemerkung` TEXT NULL ,
  `band_uid` INT NULL ,
  `band_seite` VARCHAR(45) NULL ,
  `text_gs_band` TEXT NULL ,
  `bearbeitungsstatus_uid` INT NOT NULL ,
  `personallistenstatus_uid` INT NOT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) ,
  INDEX `fk_kloster_band1_idx` (`band_uid` ASC) ,
  UNIQUE INDEX `kloster_id_UNIQUE` (`kloster_id` ASC) ,
  INDEX `fk_kloster_personallistenstatus1_idx` (`personallistenstatus_uid` ASC) ,
  INDEX `fk_kloster_bearbeitungsstatus1_idx` (`bearbeitungsstatus_uid` ASC) ,
  CONSTRAINT `fk_kloster_band1`
    FOREIGN KEY (`band_uid` )
    REFERENCES `mydb`.`band` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kloster_personallistenstatus1`
    FOREIGN KEY (`personallistenstatus_uid` )
    REFERENCES `mydb`.`personallistenstatus` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kloster_bearbeitungsstatus1`
    FOREIGN KEY (`bearbeitungsstatus_uid` )
    REFERENCES `mydb`.`bearbeitungsstatus` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`zeitraum`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`zeitraum` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`zeitraum` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `von_von` INT NULL ,
  `von_bis` INT NULL ,
  `von_verbal` VARCHAR(255) NULL ,
  `bis_von` INT NULL ,
  `bis_bis` INT NULL ,
  `bis_verbal` VARCHAR(255) NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`klosterstatus`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`klosterstatus` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`klosterstatus` (
  `uid` INT NOT NULL ,
  `status` VARCHAR(255) NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`kloster_orden`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`kloster_orden` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`kloster_orden` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `kloster_uid` INT NOT NULL ,
  `orden_uid` INT NOT NULL ,
  `klosterstatus_uid` INT NOT NULL ,
  `zeitraum_uid` INT NOT NULL ,
  `bemerkung` TEXT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) ,
  INDEX `fk_kloster_orden_orden1_idx` (`orden_uid` ASC) ,
  INDEX `fk_kloster_orden_kloster2_idx` (`kloster_uid` ASC) ,
  INDEX `fk_kloster_orden_zeitraum1_idx` (`zeitraum_uid` ASC) ,
  INDEX `fk_kloster_orden_klosterstatus1_idx` (`klosterstatus_uid` ASC) ,
  CONSTRAINT `fk_kloster_orden_orden1`
    FOREIGN KEY (`orden_uid` )
    REFERENCES `mydb`.`orden` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kloster_orden_kloster2`
    FOREIGN KEY (`kloster_uid` )
    REFERENCES `mydb`.`kloster` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kloster_orden_zeitraum1`
    FOREIGN KEY (`zeitraum_uid` )
    REFERENCES `mydb`.`zeitraum` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kloster_orden_klosterstatus1`
    FOREIGN KEY (`klosterstatus_uid` )
    REFERENCES `mydb`.`klosterstatus` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`url_typ`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`url_typ` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`url_typ` (
  `uid` INT NOT NULL ,
  `name` VARCHAR(255) NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`url`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`url` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`url` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `url` TEXT NULL ,
  `bemerkung` TEXT NULL ,
  `url_typ_uid` INT NOT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) ,
  INDEX `fk_url_url_typ1_idx` (`url_typ_uid` ASC) ,
  CONSTRAINT `fk_url_url_typ1`
    FOREIGN KEY (`url_typ_uid` )
    REFERENCES `mydb`.`url_typ` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`band_has_url`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`band_has_url` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`band_has_url` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_band_has_url_url1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_band_has_url_band1_idx` (`uid_local` ASC) ,
  CONSTRAINT `fk_band_has_url_band1`
    FOREIGN KEY (`uid_local` )
    REFERENCES `mydb`.`band` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_band_has_url_url1`
    FOREIGN KEY (`uid_foreign` )
    REFERENCES `mydb`.`url` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`kloster_has_url`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`kloster_has_url` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`kloster_has_url` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_kloster_has_url_url1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_kloster_has_url_kloster1_idx` (`uid_local` ASC) ,
  CONSTRAINT `fk_kloster_has_url_kloster1`
    FOREIGN KEY (`uid_local` )
    REFERENCES `mydb`.`kloster` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kloster_has_url_url1`
    FOREIGN KEY (`uid_foreign` )
    REFERENCES `mydb`.`url` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`kloster_standort`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`kloster_standort` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`kloster_standort` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `kloster_uid` INT NOT NULL ,
  `ort_uid` INT NOT NULL ,
  `zeitraum_uid` INT NOT NULL ,
  `gruender` TEXT NULL ,
  `bemerkung` TEXT NULL ,
  `breite` FLOAT NULL ,
  `laenge` FLOAT NULL ,
  `bemerkung_standort` TEXT NULL ,
  `temp_literatur_alt` TEXT NULL ,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) ,
  INDEX `fk_kloster_standort_kloster1_idx` (`kloster_uid` ASC) ,
  INDEX `fk_kloster_standort_ort1_idx` (`ort_uid` ASC) ,
  INDEX `fk_kloster_standort_zeitraum1_idx` (`zeitraum_uid` ASC) ,
  CONSTRAINT `fk_kloster_standort_kloster1`
    FOREIGN KEY (`kloster_uid` )
    REFERENCES `mydb`.`kloster` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kloster_standort_ort1`
    FOREIGN KEY (`ort_uid` )
    REFERENCES `mydb`.`ort` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kloster_standort_zeitraum1`
    FOREIGN KEY (`zeitraum_uid` )
    REFERENCES `mydb`.`zeitraum` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ort_has_url`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`ort_has_url` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`ort_has_url` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_ort_has_url_url1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_ort_has_url_ort1_idx` (`uid_local` ASC) ,
  CONSTRAINT `fk_ort_has_url_ort1`
    FOREIGN KEY (`uid_local` )
    REFERENCES `mydb`.`ort` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ort_has_url_url1`
    FOREIGN KEY (`uid_foreign` )
    REFERENCES `mydb`.`url` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`literatur`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`literatur` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`literatur` (
  `uid` INT NOT NULL AUTO_INCREMENT ,
  `citekey` VARCHAR(255) NULL ,
  `beschreibung` TEXT NULL ,
  `titel` TEXT NULL,
  PRIMARY KEY (`uid`) ,
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`bibitem`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`bibitem` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`bibitem` (
  `uid` INT NOT NULL ,
  `bibitem` TEXT NULL ,
  PRIMARY KEY (`uid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`orden_has_url`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`orden_has_url` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`orden_has_url` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_orden_has_url_url1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_orden_has_url_orden1_idx` (`uid_local` ASC) ,
  CONSTRAINT `fk_orden_has_url_orden1`
    FOREIGN KEY (`uid_local` )
    REFERENCES `mydb`.`orden` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orden_has_url_url1`
    FOREIGN KEY (`uid_foreign` )
    REFERENCES `mydb`.`url` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`bistum_has_url`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`bistum_has_url` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`bistum_has_url` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_bistum_has_url_url1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_bistum_has_url_bistum1_idx` (`uid_local` ASC) ,
  CONSTRAINT `fk_bistum_has_url_bistum1`
    FOREIGN KEY (`uid_local` )
    REFERENCES `mydb`.`bistum` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bistum_has_url_url1`
    FOREIGN KEY (`uid_foreign` )
    REFERENCES `mydb`.`url` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`kloster_has_literatur`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`kloster_has_literatur` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`kloster_has_literatur` (
  `uid_local` INT NOT NULL ,
  `uid_foreign` INT NOT NULL ,
  PRIMARY KEY (`uid_local`, `uid_foreign`) ,
  INDEX `fk_kloster_has_literatur_literatur1_idx` (`uid_foreign` ASC) ,
  INDEX `fk_kloster_has_literatur_kloster1_idx` (`uid_local` ASC) ,
  CONSTRAINT `fk_kloster_has_literatur_kloster1`
    FOREIGN KEY (`uid_local` )
    REFERENCES `mydb`.`kloster` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kloster_has_literatur_literatur1`
    FOREIGN KEY (`uid_foreign` )
    REFERENCES `mydb`.`literatur` (`uid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
