-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: Gambler
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.16.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `GamblerCreatorInfo`
--

DROP TABLE IF EXISTS `GamblerCreatorInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GamblerCreatorInfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` varchar(255) DEFAULT NULL,
  `gambleid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GamblerInfo`
--

DROP TABLE IF EXISTS `GamblerInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GamblerInfo` (
  `gambleid` int(11) NOT NULL AUTO_INCREMENT,
  `titleid` varchar(255) DEFAULT NULL,
  `conditionOne` text,
  `conditionTwo` text,
  `conditionThree` text,
  `conditionFour` text,
  `conditionFive` text,
  `conditionOneInfo` mediumtext,
  `conditionTwoInfo` mediumtext,
  `conditionThreeInfo` mediumtext,
  `conditionFourInfo` mediumtext,
  `conditionFiveInfo` mediumtext,
  `initgambThresh` int(11) DEFAULT NULL,
  `posgambThresh` int(11) DEFAULT NULL,
  `neggambThresh` int(11) DEFAULT NULL,
  `maxgambThresh` int(11) DEFAULT NULL,
  `mingambThresh` int(11) DEFAULT NULL,
  `gambScenario` text,
  `gambChoosing` text,
  `gambBenefits` text,
  `gambWelcome` text,
  `gambSideeffects` text,
  `gambAgreementA` text,
  `gambAgreementE` text,
  `gambAgreementB` text,
  `inittimeThresh` int(11) DEFAULT NULL,
  `postimetThresh` int(11) DEFAULT NULL,
  `negtimetThresh` int(11) DEFAULT NULL,
  `maxtimetThresh` int(11) DEFAULT NULL,
  `mintimetThresh` int(11) DEFAULT NULL,
  `timetScenario` text,
  `timetChoosing` text,
  `timetBenefits` text,
  `timetSideeffects` text,
  `timetWelcome` text,
  `timetAgreementA` text,
  `timetAgreementE` text,
  `timetAgreementB` text,
  `imageOnename` varchar(60) DEFAULT NULL,
  `imageTwoname` varchar(60) DEFAULT NULL,
  `imageThreename` varchar(60) DEFAULT NULL,
  `imageFourname` varchar(60) DEFAULT NULL,
  `imageFivename` varchar(60) DEFAULT NULL,
  `finalconditionOrderOne` varchar(60) DEFAULT NULL,
  `finalconditionOrderTwo` varchar(60) DEFAULT NULL,
  `finalconditionOrderThree` varchar(60) DEFAULT NULL,
  `finalconditionOrderFour` varchar(60) DEFAULT NULL,
  `finalconditionOrderFive` varchar(60) DEFAULT NULL,
  `conditionSix` text,
  `conditionSeven` text,
  `conditionEight` text,
  `conditionSixInfo` text,
  `conditionSevenInfo` text,
  `conditionEightInfo` text,
  `imageSixname` varchar(60) DEFAULT NULL,
  `imageSevenname` varchar(60) DEFAULT NULL,
  `imageEightname` varchar(60) DEFAULT NULL,
  `mechgamb` varchar(60) DEFAULT NULL,
  `conditionOneAC` varchar(10) DEFAULT NULL,
  `conditionTwoAC` varchar(10) DEFAULT NULL,
  `conditionThreeAC` varchar(10) DEFAULT NULL,
  `conditionFourAC` varchar(10) DEFAULT NULL,
  `conditionFiveAC` varchar(10) DEFAULT NULL,
  `conditionSixAC` varchar(10) DEFAULT NULL,
  `conditionSevenAC` varchar(10) DEFAULT NULL,
  `conditionEightAC` varchar(10) DEFAULT NULL,
  `gambScenarioThree` text,
  `gambScenarioFour` text,
  `gambScenarioFive` text,
  `gambScenarioSix` text,
  `gambScenarioSeven` text,
  `timetScenarioThree` text,
  `timetScenarioFour` text,
  `timetScenarioFive` text,
  `timetScenarioSix` text,
  `timetScenarioSeven` text,
  `otitleid` text,
  `language_id` int(5) DEFAULT '1',
  `language` varchar(10) DEFAULT NULL,
  `SonFHR` int(11) DEFAULT NULL,
  `genranduid` int(11) DEFAULT NULL,
  `disablepatname` int(11) DEFAULT NULL,
  `disablepatgender` int(11) DEFAULT NULL,
  `disablepatage` int(11) DEFAULT NULL,
  `disablepatrace` int(11) DEFAULT NULL,
  PRIMARY KEY (`gambleid`),
  UNIQUE KEY `titleid` (`titleid`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `LangCode`
--

DROP TABLE IF EXISTS `LangCode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LangCode` (
  `language_id` int(5) NOT NULL AUTO_INCREMENT,
  `language` varchar(10) DEFAULT NULL,
  `language_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`language_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `LangUserGenderRaceSystemTranslate`
--

DROP TABLE IF EXISTS `LangUserGenderRaceSystemTranslate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LangUserGenderRaceSystemTranslate` (
  `language_id` int(11) NOT NULL AUTO_INCREMENT,
  `demographics_language` varchar(20) DEFAULT NULL,
  `demographics_country` varchar(20) DEFAULT NULL,
  `demographics_gender` text,
  `demographics_gender_default` varchar(20) DEFAULT NULL,
  `demographics_race` text,
  `demographics_race_default` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`language_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `LangUserSystemTranslate`
--

DROP TABLE IF EXISTS `LangUserSystemTranslate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LangUserSystemTranslate` (
  `language_id` int(5) NOT NULL,
  `Greeting_Text` text,
  `Continue_Button` text,
  `Show_Less_Text` text,
  `Show_More_Text` text,
  `Title_Title_Program` text,
  `Title_Project_Name` text,
  `Title_Status_Text` text,
  `Title_Start_Button` text,
  `SInfo_Icon_Text` text,
  `SInfo_HS_Text` text,
  `SInfo_HSA_Text` text,
  `SInfo_Status_Info` text,
  `SInfo_Information_Text` text,
  `SInfo_Instruction_Text` text,
  `OR_Instruction_Text` text,
  `OR_Video_Instruction_Text` text,
  `OR_Incorrect_Function_Text` text,
  `VAS_Instruction_Text` text,
  `VAS_Alert_Selection_Text` text,
  `VAS_Video_Instruction_Text` text,
  `SG_Video_Instruction_Text` text,
  `SG_HS_Video_Instruction_Text` text,
  `TTO_Video_Instruction_Text` text,
  `TTO_HS_Video_Instruction_Text` text,
  `End_HS_Text` text,
  `End_OR_Text` text,
  `End_VAS_Text` text,
  `End_SG_Text` text,
  `End_TTO_Text` text,
  `End_CSV_Export_Button` text,
  `End_Finish_Button` text,
  `language` varchar(255) DEFAULT NULL,
  `End_Greeting_Text` text,
  `Demo_userid_text` text,
  `Demo_firstname_text` text,
  `Demo_lastname_text` text,
  `Demo_age_text` text,
  `Demo_hld_text` text,
  `Demo_gender_text` text,
  `Demo_race_text` text,
  `Demo_videoinstructions_text` text,
  `Demo_firstname_warn_text` text,
  `Demo_lastname_warn_text` text,
  `Demo_age_warn_text` text,
  `Demo_Information_Text` text,
  `SG_Shake_Button` text,
  `SG_Pill_Text` text,
  `TTO_Month_Text` text,
  `TTO_Year_Text` text,
  PRIMARY KEY (`language_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `LifeTable`
--

DROP TABLE IF EXISTS `LifeTable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LifeTable` (
  `Age` int(11) NOT NULL,
  `Citizen` float DEFAULT NULL,
  `Male` float DEFAULT NULL,
  `Female` float DEFAULT NULL,
  `White` float DEFAULT NULL,
  `WMale` float DEFAULT NULL,
  `WFemale` float DEFAULT NULL,
  `AA` float DEFAULT NULL,
  `AAMale` float DEFAULT NULL,
  `AAFemale` float DEFAULT NULL,
  `WHispanic` float DEFAULT NULL,
  `WHMale` float DEFAULT NULL,
  `WHFemale` float DEFAULT NULL,
  PRIMARY KEY (`Age`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `UserInfo`
--

DROP TABLE IF EXISTS `UserInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserInfo` (
  `uid` int(12) NOT NULL AUTO_INCREMENT,
  `userid` varchar(255) DEFAULT NULL,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `age` int(4) DEFAULT NULL,
  `hld` int(4) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `race` varchar(255) DEFAULT NULL,
  `finalconditionIntensityOne` int(4) DEFAULT NULL,
  `finalconditionIntensityTwo` int(4) DEFAULT NULL,
  `finalconditionIntensityThree` int(4) DEFAULT NULL,
  `finalconditionIntensityFour` int(4) DEFAULT NULL,
  `finalconditionIntensityFive` int(4) DEFAULT NULL,
  `finalconditionTimeTOne` varchar(60) DEFAULT NULL,
  `finalconditionTimeTTwo` varchar(60) DEFAULT NULL,
  `finalconditionTimeTThree` int(4) DEFAULT NULL,
  `finalconditionTimeTFour` int(4) DEFAULT NULL,
  `finalconditionTimeTFive` int(4) DEFAULT NULL,
  `finalconditionGambOne` int(4) DEFAULT NULL,
  `finalconditionGambTwo` int(4) DEFAULT NULL,
  `finalconditionGambThree` int(4) DEFAULT NULL,
  `finalconditionGambFour` int(4) DEFAULT NULL,
  `finalconditionGambFive` int(4) DEFAULT NULL,
  `titleid` varchar(60) DEFAULT NULL,
  `finalconditionOrderOne` int(4) DEFAULT NULL,
  `finalconditionOrderTwo` int(4) DEFAULT NULL,
  `finalconditionOrderThree` int(4) DEFAULT NULL,
  `finalconditionOrderFour` int(4) DEFAULT NULL,
  `finalconditionOrderFive` int(4) DEFAULT NULL,
  `finalconditionOrderSix` int(4) DEFAULT NULL,
  `finalconditionOrderSeven` int(4) DEFAULT NULL,
  `finalconditionOrderEight` int(4) DEFAULT NULL,
  `finalconditionIntensitySix` int(4) DEFAULT NULL,
  `finalconditionIntensitySeven` int(4) DEFAULT NULL,
  `finalconditionIntensityEight` int(4) DEFAULT NULL,
  `finalconditionTimeTSix` int(4) DEFAULT NULL,
  `finalconditionTimeTSeven` int(4) DEFAULT NULL,
  `finalconditionTimeTEight` int(4) DEFAULT NULL,
  `finalconditionGambSix` int(4) DEFAULT NULL,
  `finalconditionGambSeven` int(4) DEFAULT NULL,
  `finalconditionGambEight` int(4) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `UserMetaData`
--

DROP TABLE IF EXISTS `UserMetaData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserMetaData` (
  `entryid` int(30) NOT NULL AUTO_INCREMENT,
  `gambleid` int(11) DEFAULT NULL,
  `titleid` varchar(255) DEFAULT NULL,
  `userid` varchar(255) DEFAULT NULL,
  `currentPage` text,
  `buttonPress` text,
  `totalTime` int(11) DEFAULT NULL,
  `conditionOneTime` double DEFAULT NULL,
  `conditionTwoTime` double DEFAULT NULL,
  `conditionThreeTime` double DEFAULT NULL,
  `conditionFourTime` double DEFAULT NULL,
  `conditionFiveTime` double DEFAULT NULL,
  `conditionSixTime` double DEFAULT NULL,
  `conditionSevenTime` double DEFAULT NULL,
  `conditionEightTime` double DEFAULT NULL,
  `conditionOneVideoTime` double DEFAULT NULL,
  `conditionTwoVideoTime` double DEFAULT NULL,
  `conditionThreeVideoTime` double DEFAULT NULL,
  `conditionFourVideoTime` double DEFAULT NULL,
  `conditionFiveVideoTime` double DEFAULT NULL,
  `conditionSixVideoTime` double DEFAULT NULL,
  `conditionSevenVideoTime` double DEFAULT NULL,
  `conditionEightVideoTime` double DEFAULT NULL,
  PRIMARY KEY (`entryid`)
) ENGINE=InnoDB AUTO_INCREMENT=1558 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-18 16:34:21
