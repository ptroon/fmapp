-- MySQL dump 10.13  Distrib 5.5.62, for Linux (x86_64)
--
-- Host: localhost    Database: fmapp
-- ------------------------------------------------------
-- Server version	5.5.62

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
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bookings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot_id` int(11) DEFAULT NULL,
  `title` varchar(32) NOT NULL,
  `start_dt` datetime NOT NULL,
  `end_dt` datetime NOT NULL,
  `ticket` varchar(20) NOT NULL,
  `stakeholder_id` varchar(20) DEFAULT NULL,
  `budget` varchar(20) DEFAULT NULL,
  `project` varchar(100) DEFAULT NULL,
  `description` varchar(4000) NOT NULL,
  `owner_id` varchar(25) DEFAULT NULL,
  `complex` int(11) NOT NULL,
  `cluster` int(11) NOT NULL,
  `approval_required` int(11) DEFAULT NULL,
  `approved_date` datetime DEFAULT NULL,
  `approved_by` varchar(25) DEFAULT NULL,
  `change_ref` varchar(20) DEFAULT NULL,
  `change_subref` varchar(20) DEFAULT NULL,
  `logged` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `change_profiles`
--

DROP TABLE IF EXISTS `change_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `change_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `change_name` varchar(256) DEFAULT NULL,
  `change_desc` text,
  `master_record` varchar(32) DEFAULT NULL,
  `task_record` varchar(32) DEFAULT NULL,
  `sbid` varchar(9) DEFAULT NULL,
  `budget_code` varchar(32) DEFAULT NULL,
  `target_date` datetime DEFAULT NULL,
  `change_raiser` int(11) DEFAULT NULL,
  `change_checker` int(11) DEFAULT NULL,
  `change_approver` int(11) DEFAULT NULL,
  `change_implementer` int(11) DEFAULT NULL,
  `change_raised` datetime DEFAULT NULL,
  `change_checked` datetime DEFAULT NULL,
  `change_approved` datetime DEFAULT NULL,
  `change_implemented` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `change_profiles`
--

LOCK TABLES `change_profiles` WRITE;
/*!40000 ALTER TABLE `change_profiles` DISABLE KEYS */;
/*!40000 ALTER TABLE `change_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complexes`
--

DROP TABLE IF EXISTS `complexes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `complexes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `complex_name` varchar(1000) NOT NULL,
  `complex_manager` int(11) NOT NULL,
  `complex_fw_inner_1` varchar(1000) DEFAULT NULL,
  `complex_fw_inner_2` varchar(1000) DEFAULT NULL,
  `complex_fw_outer_1` varchar(1000) DEFAULT NULL,
  `complex_fw_outer_2` varchar(1000) DEFAULT NULL,
  `complex_fw_location_1` varchar(1000) DEFAULT NULL,
  `complex_fw_location_2` varchar(1000) DEFAULT NULL,
  `complex_fw_type` int(11) NOT NULL,
  `complex_serial` varchar(1000) DEFAULT NULL,
  `complex_license` varchar(1000) DEFAULT NULL,
  `complex_push_start` varchar(5) DEFAULT NULL,
  `complex_push_end` varchar(5) DEFAULT NULL,
  `complex_push_days` varchar(7) DEFAULT NULL,
  `complex_category` varchar(1000) DEFAULT NULL,
  `complex_hardware` varchar(1000) DEFAULT NULL,
  `complex_fw_inner_name_1` varchar(1000) DEFAULT NULL,
  `complex_fw_inner_name_2` varchar(1000) DEFAULT NULL,
  `complex_location_1` varchar(1000) DEFAULT NULL,
  `complex_fw_outer_name_1` varchar(1000) DEFAULT NULL,
  `complex_fw_outer_name_2` varchar(1000) DEFAULT NULL,
  `complex_location_2` varchar(1000) DEFAULT NULL,
  `complex_location_all` varchar(1000) DEFAULT NULL,
  `complex_area` int(11) NOT NULL,
  `complex_fw_info1` varchar(1000) DEFAULT NULL,
  `complex_fw_info2` varchar(1000) DEFAULT NULL,
  `complex_fw_inner_info1` varchar(1000) DEFAULT NULL,
  `complex_fw_inner_info2` varchar(1000) DEFAULT NULL,
  `complex_fw_outer_info1` varchar(1000) DEFAULT NULL,
  `complex_fw_outer_info2` varchar(1000) DEFAULT NULL,
  `complex_type` int(11) NOT NULL,
  `complex_info_1` varchar(1000) DEFAULT NULL,
  `complex_country` int(11) NOT NULL,
  `complex_restricted` int(11) DEFAULT NULL,
  `complex_restrict_start` varchar(5) DEFAULT NULL,
  `complex_restrict_end` varchar(5) DEFAULT NULL,
  `complex_allow_slot_day` varchar(7) DEFAULT NULL,
  `complex_allow_slot_start` varchar(5) DEFAULT NULL,
  `complex_allow_slot_end` varchar(5) DEFAULT NULL,
  `complex_push_day_extra` varchar(7) DEFAULT NULL,
  `complex_change_info` varchar(2000) DEFAULT NULL,
  `complex_environment` int(11) DEFAULT NULL,
  `complex_updated` datetime DEFAULT NULL,
  `complex_active` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complexes`
--

LOCK TABLES `complexes` WRITE;
/*!40000 ALTER TABLE `complexes` DISABLE KEYS */;
INSERT INTO `complexes` VALUES (1,'Made Up CheckPoint',87,'asd','asd','asd','asd','asd','asd',91,'asd','asd','02:00','04:00','NYNNNNN','asd','asd','','','','','','','',69,'','','','','','',108,'',69,107,'0','0','0','02:00','04:00','NNNNNYY','',95,'2020-01-27 09:01:00',67),(2,'Made Up Fortigate',86,'test','test','test','test','test','test',91,'test','test','02:00','04:00','YYYYYYN','test','test','','','','','','','',61,'','','','','','',103,'',61,107,'06/02','07/02','0','04:00','06:00','YYYYYYY','',94,'2020-02-03 16:40:39',67);
/*!40000 ALTER TABLE `complexes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard`
--

DROP TABLE IF EXISTS `dashboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fm_text` text,
  `fg_text` text,
  `user_text` text,
  `log_text` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard`
--

LOCK TABLES `dashboard` WRITE;
/*!40000 ALTER TABLE `dashboard` DISABLE KEYS */;
INSERT INTO `dashboard` VALUES (1,'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');
/*!40000 ALTER TABLE `dashboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datesofinterest`
--

DROP TABLE IF EXISTS `datesofinterest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datesofinterest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doi_name` varchar(1000) NOT NULL,
  `doi_priority` int(11) NOT NULL,
  `doi_comment` varchar(2000) DEFAULT NULL,
  `doi_start_dt` datetime NOT NULL,
  `doi_end_dt` datetime NOT NULL,
  `doi_regions` varchar(100) DEFAULT NULL,
  `doi_locked` int(11) DEFAULT NULL,
  `doi_hap` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datesofinterest`
--

LOCK TABLES `datesofinterest` WRITE;
/*!40000 ALTER TABLE `datesofinterest` DISABLE KEYS */;
INSERT INTO `datesofinterest` VALUES (1,'Change Freeze (Critical)',83,'Change Freeze (Critical) that is very important','2020-02-22 00:00:00','2020-02-28 23:45:00','GBR,IND',107,106),(8,'Easter Holiday',83,'Easter Holiday','2020-04-10 00:00:00','2020-04-13 23:45:00','GBR,IND',107,106),(9,'May Day',83,'May Day Holiday','2020-05-08 00:00:00','2020-05-08 23:45:00','GBR,IND',106,106),(10,'Late May Holiday',83,'Late May Holiday','2020-05-25 00:00:00','2020-05-25 23:45:00','GBR,IND',106,106),(11,'Christmas Day',83,'Christmas Day','2020-12-25 00:00:00','2020-12-25 23:45:00','GBR,IND',107,106),(12,'Boxing Day',83,'Boxing Day','2020-12-26 00:00:00','2020-12-26 23:45:00','GBR,IND',107,106),(13,'Boxing Day Holiday',83,'Boxing Day Holiday','2020-12-28 00:00:00','2020-12-28 23:45:00','GBR,IND',106,106),(15,'Summer Change Freeze',83,'Summer Change Freeze','2020-07-23 00:00:00','2020-07-25 23:45:00','GBR,IND',107,106),(16,'Important Thing that is a long name',83,'Important Thing','2020-02-23 00:00:00','2020-02-24 23:45:00','GBR,IND',106,106),(18,'Test Feb',83,'Test Feb','2020-02-20 00:00:00','2020-02-26 23:45:00','GBR,IND',106,106),(19,'Change Freeze RED',83,'','2020-04-14 00:00:00','2020-04-14 23:45:00','GBR,IND',106,106);
/*!40000 ALTER TABLE `datesofinterest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fortimanagers`
--

DROP TABLE IF EXISTS `fortimanagers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fortimanagers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_name` varchar(128) NOT NULL,
  `ip` varchar(32) NOT NULL,
  `adom_mode` int(11) DEFAULT NULL,
  `serial` varchar(32) DEFAULT NULL,
  `version` varchar(64) DEFAULT NULL,
  `username` varchar(64) NOT NULL,
  `_password` varchar(128) NOT NULL,
  `sync_time` datetime DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fortimanagers`
--

LOCK TABLES `fortimanagers` WRITE;
/*!40000 ALTER TABLE `fortimanagers` DISABLE KEYS */;
INSERT INTO `fortimanagers` VALUES (1,'TESTFM','192.168.1.200',0,NULL,NULL,'adminuser','gAAAAABdZ-BcyTP3ZFK1D126rxjaTGLSDGQQgTZDN4tyIQqvdUeliHdocdVLsDXcUgZsKqR1hQdGArHnSfxrG9jLHdPDhtkNkA==',NULL,0);
/*!40000 ALTER TABLE `fortimanagers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_name` varchar(1000) NOT NULL,
  `job_type` int(11) NOT NULL,
  `job_start` datetime NOT NULL,
  `job_complete` datetime DEFAULT NULL,
  `job_content` varchar(4000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parameters`
--

DROP TABLE IF EXISTS `parameters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parameters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `param_name` varchar(1000) NOT NULL,
  `param_value` varchar(2000) NOT NULL,
  `param_group` int(11) DEFAULT NULL,
  `param_parent` int(11) DEFAULT NULL,
  `param_disabled` int(11) DEFAULT NULL,
  `param_critical` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameters`
--

LOCK TABLES `parameters` WRITE;
/*!40000 ALTER TABLE `parameters` DISABLE KEYS */;
INSERT INTO `parameters` VALUES (1,'Locations','Locations',0,0,0,1),(2,'Firewall Managers','Firewall Managers',0,0,0,1),(3,'Hours','Hours',0,0,0,1),(4,'Minutes','Minutes',0,0,0,1),(29,'Hour 00','00',3,0,0,0),(30,'Hour 01','01',3,0,0,0),(31,'Hour 02','02',3,0,0,0),(32,'Hour 03','03',3,0,0,0),(33,'Hour 04','04',3,0,0,0),(34,'Hour 05','05',3,0,0,0),(35,'Hour 06','06',3,0,0,0),(36,'Hour 07','07',3,0,0,0),(37,'Hour 08','08',3,0,0,0),(38,'Hour 09','09',3,0,0,0),(39,'Hour 10','10',3,0,0,0),(40,'Hour 11','11',3,0,0,0),(41,'Hour 12','12',3,0,0,0),(42,'Hour 13','13',3,0,0,0),(43,'Hour 14','14',3,0,0,0),(44,'Hour 15','15',3,0,0,0),(45,'Hour 16','16',3,0,0,0),(46,'Hour 17','17',3,0,0,0),(47,'Hour 18','18',3,0,0,0),(48,'Hour 19','19',3,0,0,0),(49,'Hour 20','20',3,0,0,0),(50,'Hour 21','21',3,0,0,0),(51,'Hour 22','22',3,0,0,0),(52,'Hour 23','23',3,0,0,0),(53,'Minute 00','00',4,0,0,0),(54,'Minute 15','15',4,0,0,0),(55,'Minute 30','30',4,0,0,0),(56,'Minute 45','45',4,0,0,0),(57,'Minute 59','59',4,0,0,0),(61,'United Kingdom','GBR',1,0,0,1),(63,'Vendors','Vendors',0,0,0,1),(64,'Vendor-name1','Vendor-name1',63,0,0,0),(65,'Vendor-name2','Vendor-name2',63,0,0,0),(66,'Active Options','Active Options',0,0,0,1),(67,'Active','1',66,0,0,1),(68,'Not Active','0',66,0,0,1),(69,'India','IND',1,0,0,1),(70,'Main-Organisation','Main-Organisation',63,0,0,0),(71,'Search Categories','Search Categories',0,0,0,1),(72,'Parameters','{\r\n\'name\' : \'Parameters\',\r\n\'id\' : 2,\r\n\'query\' : \'parameter.param_name.like(\"%{}%\")\'\r\n}',71,0,0,1),(73,'Users','{ \r\n\'name\' : \'Users\',\r\n\'id\' : 3,\r\n\'query\' : \'users.forename.like(\"%{}%\") | users.surname.like(\"%{}%\")\' \r\n}',71,0,0,1),(74,'Everything','{ \r\n\'name\' : \'Everything\', \r\n\'id\' : 1, \r\n\'query\' : \'\' \r\n}',71,0,0,1),(75,'Log File Options','Log File Options',0,0,0,1),(76,'Application Log','LOG_FILE',75,0,0,1),(77,'Database Log','DB_LOG_FILE',75,0,0,1),(78,'Log Entries','Log Entries',0,0,0,1),(79,'Show 10 Records','10',78,0,0,1),(80,'Show 100 Records','100',78,0,0,1),(81,'Show All Records','99999',78,0,0,1),(82,'Priority','Priority',0,0,0,1),(83,'High','High',82,0,0,1),(84,'Medium','Medium',82,0,0,1),(85,'Low','Low',82,0,0,1),(86,'FortiManager','Fortigate FortiManager',2,0,0,0),(87,'CheckPoint CMA','CheckPoint CMA',2,0,0,0),(88,'Juniper','Juniper',2,0,0,0),(89,'Firewall Type','Firewall Type',0,0,0,1),(90,'Single Layer','Single Layer',89,0,0,1),(91,'Dual Layer','Dual Layer',89,0,0,1),(92,'Environments','Environments',0,0,0,0),(93,'Test','Test',92,0,0,0),(94,'Production','Production',92,0,0,0),(95,'FTE','FTE',92,0,0,0),(96,'NFTE','NFTE',92,0,0,0),(97,'Cluster Type','Cluster Type',0,0,0,0),(98,'Inner','Inner',97,0,0,0),(99,'Outer','Outer',97,0,0,0),(100,'Complex Type','Complex Type',0,0,0,1),(101,'Fortigate','Fortigate',100,0,0,1),(102,'Juniper','Juniper',100,0,0,0),(103,'Cisco','Cisco',100,0,0,0),(104,'F5','F5',100,0,0,0),(105,'Yes/No Answers','Yes or No for answering options as a select list',0,0,0,1),(106,'Yes','1',105,0,0,1),(107,'No','0',105,0,0,1),(108,'CheckPoint','CheckPoint',100,0,0,0),(109,'Booking Parameters','Core booking parameters that define rules for how many bookings can be achieved ',0,0,0,1),(110,'Total Changes Per Complex Per Day','3',109,0,0,1),(111,'Different Complexes Per Day','8',109,0,0,1),(112,'Total Changes Per Day','16',109,0,0,1),(113,'Help Content','Covers the usage of the system',0,0,0,1),(114,'1. Logging in & Registration','To register, click on the link called \"Register for access to secFBA\".  Fill in the fields as required and press Register to submit the request.  Once the request is received, the team managing user requests will approve the access to allow you to login and start booking changes',113,0,0,1);
/*!40000 ALTER TABLE `parameters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(100) NOT NULL,
  `role_admin` int(11) NOT NULL,
  `role_app_sections` varchar(200) DEFAULT NULL,
  `created_date` datetime NOT NULL,
  `enabled` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Standard User Access',0,'LOGIN','2020-01-29 19:35:33',1),(2,'Administrator User Access',1,'LOGIN','2020-01-29 19:37:55',1),(6,'No Login',0,'','2020-01-29 19:59:20',1);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` varchar(25) NOT NULL,
  `forename` varchar(100) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `comment` varchar(2000) DEFAULT NULL,
  `_password` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` int(11) DEFAULT NULL,
  `vendor` int(11) DEFAULT NULL,
  `created_date` datetime NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `last_modified` datetime DEFAULT NULL,
  `modified_by` varchar(100) DEFAULT NULL,
  `enabled` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_id` (`login_id`),
  KEY `role` (`role`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'philip','Philip','Troon','User account for Philip Troon','$2b$12$pyyaZQRkxyVdz8SXVmrRCepr6UXs38rin1uk/Nqtqd9Q3WUuojF0i','philiptroon@gmail.com',2,70,'2019-08-28 11:46:08','2020-01-06 15:34:08','2020-01-30 08:56:35','philip',0),(2,'bob','Bob','Smith','User account for Bob Smith 123','$2b$12$S1dmklX6EOC.5JeHQ8imiO3Wa6hZcNBb7zgZHbuqUWyxmMWv3WjrS','bob@somewhere.com',1,64,'2019-08-28 11:46:08',NULL,'2020-01-30 01:26:17','philip',0),(3,'frank','Frank','Black','User account for Frank Black test 987654321','$2b$12$nbRhfcVg5W70EbAxHek.3OABSd5twyY9Ezmr5Cr4LRXOgTNZsLYSe','frank@somewhere.com',2,65,'2019-08-28 11:46:08',NULL,'2020-01-30 09:05:57','frank',0),(4,'evan','Evan','Troon','Account for Evan Troon','$2b$12$fRYijfQhLPT1wH9/akayhu/1F9l1IgozFbXG4uMk0p5H2u66/tUVy','evan@someone.com',1,70,'2019-09-02 15:14:53',NULL,'2020-01-28 16:52:21','philip',1),(6,'dylan','Dylan','Troon','Dylan Troon TEST12399','$2b$12$kyttQmBiV7Gxn4NdG1gh1eOwfzfp8LEy5.PUhMLcUyWlVd8F9DSku','dylan@somewhere.com',1,65,'2019-09-02 16:50:50',NULL,'2020-01-26 19:12:30','philip',1),(8,'philip2','Philip','Troon','Test account','$2b$12$Hpbh0Dfjr9dtIcXAngUGKedF9XdsPlZWtQ0a.iZg0J0zdzAepBKru','philiptroon@gmail.com',1,65,'2020-01-29 19:28:53',NULL,'2020-01-30 09:04:24','philip2',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-04  9:57:19
