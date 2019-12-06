-- MySQL dump 10.13  Distrib 5.7.28, for Linux (x86_64)
--
-- Host: localhost    Database: fmapp
-- ------------------------------------------------------
-- Server version       5.7.28-0ubuntu0.19.04.2

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Standard User Access',0,'CHANGES','2019-08-28 11:44:03',NULL),(2,'Administrator User Access',1,'CHANGES,ADMIN','2019-08-28 11:44:03',NULL);
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
  `created_date` datetime NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `last_modified` datetime DEFAULT NULL,
  `modified_by` varchar(100) DEFAULT NULL,
  `enabled` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_id` (`login_id`),
  KEY `role` (`role`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'philip','Philip','Troon','User account for Philip Troon','$2b$12$pyyaZQRkxyVdz8SXVmrRCepr6UXs38rin1uk/Nqtqd9Q3WUuojF0i','philiptroon@gmail.com',2,'2019-08-28 11:46:08','2019-09-02 11:29:55','2019-09-02 11:29:55','philip',0),(2,'bob','Bob','Smith','User account for Bob Smith','$2b$12$SjOFE3rvjz4Jpn4MUa5T9uS3TeoAXcgNhhRJOa0xiu2sQh0ux7pAK','bob@somewhere.com',1,'2019-08-28 11:46:08','2019-09-02 11:30:13','2019-09-02 11:30:13','philip',0),(3,'frank','Frank','Green','User account for Frank Green XYZsdsdsd','$2b$12$2RDJ3F87MGxqgtTlXs7uOeK6zUufGtA3aTBouKgJcsyczf9oHyC0a','frank@somewhere.com',1,'2019-08-28 11:46:08','2019-09-02 20:55:25','2019-09-02 20:55:25','philip',0),(4,'evan','Evan','Troon','Account for Evan','$2b$12$fRYijfQhLPT1wH9/akayhu/1F9l1IgozFbXG4uMk0p5H2u66/tUVy','evan@someone.com',1,'2019-09-02 15:14:53','2019-09-02 16:12:03','2019-09-02 16:12:03','philip',1),(6,'dylan','Dylan','Troon','Dylan Troon XYZ','$2b$12$kyttQmBiV7Gxn4NdG1gh1eOwfzfp8LEy5.PUhMLcUyWlVd8F9DSku','dylan@somewhere.com',1,'2019-09-02 16:50:50','2019-09-03 09:02:34','2019-09-03 09:02:34','philip',1);
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

-- Dump completed on 2019-12-03 13:04:54

