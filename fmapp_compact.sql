/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bookings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `url` varchar(1000) DEFAULT NULL,
  `logged` datetime DEFAULT NULL,
  `owner_id` varchar(25) DEFAULT NULL,
  `zone` varchar(200) DEFAULT NULL,
  `approved_date` datetime DEFAULT NULL,
  `approved_by` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
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
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `complexes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `complex_name` varchar(1000) NOT NULL,
  `complex_mgr` varchar(1000) NOT NULL,
  `complex_type` varchar(1000) NOT NULL,
  `firewall_type` varchar(1000) NOT NULL,
  `location` varchar(1000) NOT NULL,
  `environment` varchar(1000) NOT NULL,
  `updated` varchar(1000) NOT NULL,
  `active` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
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
INSERT INTO `dashboard` VALUES (1,'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datesofinterest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doi_name` varchar(1000) NOT NULL,
  `doi_priority` int(11) NOT NULL,
  `doi_comment` varchar(2000) DEFAULT NULL,
  `doi_start_dt` datetime NOT NULL,
  `doi_end_dt` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `datesofinterest` VALUES (1,'Christmas Holiday',83,'test','2020-02-08 15:15:00','2020-02-15 15:45:00');
INSERT INTO `datesofinterest` VALUES (8,'Easter Holiday',83,'Easter Holiday','2020-03-26 00:00:00','2020-04-18 00:00:00');
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
INSERT INTO `fortimanagers` VALUES (1,'TESTFM','192.168.1.200',0,NULL,NULL,'adminuser','gAAAAABdZ-BcyTP3ZFK1D126rxjaTGLSDGQQgTZDN4tyIQqvdUeliHdocdVLsDXcUgZsKqR1hQdGArHnSfxrG9jLHdPDhtkNkA==',NULL,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `parameters` VALUES (1,'Locations','Locations',0,0,0,1);
INSERT INTO `parameters` VALUES (2,'Firewall Managers','Firewall Managers',0,0,0,0);
INSERT INTO `parameters` VALUES (3,'Hours','Hours',0,0,0,1);
INSERT INTO `parameters` VALUES (4,'Minutes','Minutes',0,0,0,1);
INSERT INTO `parameters` VALUES (29,'Hour 00','00',3,0,0,0);
INSERT INTO `parameters` VALUES (30,'Hour 01','01',3,0,0,0);
INSERT INTO `parameters` VALUES (31,'Hour 02','02',3,0,0,0);
INSERT INTO `parameters` VALUES (32,'Hour 03','03',3,0,0,0);
INSERT INTO `parameters` VALUES (33,'Hour 04','04',3,0,0,0);
INSERT INTO `parameters` VALUES (34,'Hour 05','05',3,0,0,0);
INSERT INTO `parameters` VALUES (35,'Hour 06','06',3,0,0,0);
INSERT INTO `parameters` VALUES (36,'Hour 07','07',3,0,0,0);
INSERT INTO `parameters` VALUES (37,'Hour 08','08',3,0,0,0);
INSERT INTO `parameters` VALUES (38,'Hour 09','09',3,0,0,0);
INSERT INTO `parameters` VALUES (39,'Hour 10','10',3,0,0,0);
INSERT INTO `parameters` VALUES (40,'Hour 11','11',3,0,0,0);
INSERT INTO `parameters` VALUES (41,'Hour 12','12',3,0,0,0);
INSERT INTO `parameters` VALUES (42,'Hour 13','13',3,0,0,0);
INSERT INTO `parameters` VALUES (43,'Hour 14','14',3,0,0,0);
INSERT INTO `parameters` VALUES (44,'Hour 15','15',3,0,0,0);
INSERT INTO `parameters` VALUES (45,'Hour 16','16',3,0,0,0);
INSERT INTO `parameters` VALUES (46,'Hour 17','17',3,0,0,0);
INSERT INTO `parameters` VALUES (47,'Hour 18','18',3,0,0,0);
INSERT INTO `parameters` VALUES (48,'Hour 19','19',3,0,0,0);
INSERT INTO `parameters` VALUES (49,'Hour 20','20',3,0,0,0);
INSERT INTO `parameters` VALUES (50,'Hour 21','21',3,0,0,0);
INSERT INTO `parameters` VALUES (51,'Hour 22','22',3,0,0,0);
INSERT INTO `parameters` VALUES (52,'Hour 23','23',3,0,0,0);
INSERT INTO `parameters` VALUES (53,'Minute 00','00',4,0,0,0);
INSERT INTO `parameters` VALUES (54,'Minute 15','15',4,0,0,0);
INSERT INTO `parameters` VALUES (55,'Minute 30','30',4,0,0,0);
INSERT INTO `parameters` VALUES (56,'Minute 45','45',4,0,0,0);
INSERT INTO `parameters` VALUES (57,'Minute 59','59',4,0,0,0);
INSERT INTO `parameters` VALUES (61,'United Kingdom','GBR',1,0,0,0);
INSERT INTO `parameters` VALUES (63,'Vendors','Vendors',0,0,0,1);
INSERT INTO `parameters` VALUES (64,'Vendor-name1','Vendor-name1',63,0,0,0);
INSERT INTO `parameters` VALUES (65,'Vendor-name2','Vendor-name2',63,0,0,0);
INSERT INTO `parameters` VALUES (66,'Active Options','Active Options',0,0,0,1);
INSERT INTO `parameters` VALUES (67,'Active','1',66,0,0,0);
INSERT INTO `parameters` VALUES (68,'Not Active','0',66,0,0,0);
INSERT INTO `parameters` VALUES (69,'India','IND',1,0,0,0);
INSERT INTO `parameters` VALUES (70,'Main-Organisation','Main-Organisation',63,0,0,0);
INSERT INTO `parameters` VALUES (71,'Search Categories','Search Categories',0,0,0,1);
INSERT INTO `parameters` VALUES (72,'Parameters','{\r\n\'name\' : \'Parameters\',\r\n\'id\' : 2,\r\n\'query\' : \'parameter.param_name.like(\"%{}%\")\'\r\n}',71,0,0,1);
INSERT INTO `parameters` VALUES (73,'Users','{ \r\n\'name\' : \'Users\',\r\n\'id\' : 3,\r\n\'query\' : \'users.forename.like(\"%{}%\") | users.surname.like(\"%{}%\")\' \r\n}',71,0,0,1);
INSERT INTO `parameters` VALUES (74,'Everything','{ \r\n\'name\' : \'Everything\', \r\n\'id\' : 1, \r\n\'query\' : \'\' \r\n}',71,0,0,1);
INSERT INTO `parameters` VALUES (75,'Log File Options','Log File Options',0,0,0,1);
INSERT INTO `parameters` VALUES (76,'Application Log','LOG_FILE',75,0,0,1);
INSERT INTO `parameters` VALUES (77,'Database Log','DB_LOG_FILE',75,0,0,1);
INSERT INTO `parameters` VALUES (78,'Log Entries','Log Entries',0,0,0,1);
INSERT INTO `parameters` VALUES (79,'Show 10 Records','10',78,0,0,1);
INSERT INTO `parameters` VALUES (80,'Show 50 Records','50',78,0,0,1);
INSERT INTO `parameters` VALUES (81,'Show All Records','99999',78,0,0,1);
INSERT INTO `parameters` VALUES (82,'Priority','Priority',0,0,0,1);
INSERT INTO `parameters` VALUES (83,'High','High',82,0,0,1);
INSERT INTO `parameters` VALUES (84,'Medium','Medium',82,0,0,1);
INSERT INTO `parameters` VALUES (85,'Low','Low',82,0,0,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `roles` VALUES (1,'Standard User Access',0,'CHANGES','2019-08-28 11:44:03',1);
INSERT INTO `roles` VALUES (2,'Administrator User Access',1,'CHANGES,ADMIN','2019-08-28 11:44:03',1);
INSERT INTO `roles` VALUES (6,'New User',0,'','2020-01-08 17:08:55',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `users` VALUES (1,'philip','Philip','Troon','User account for Philip Troon','$2b$12$pyyaZQRkxyVdz8SXVmrRCepr6UXs38rin1uk/Nqtqd9Q3WUuojF0i','philiptroon@gmail.com',2,70,'2019-08-28 11:46:08','2020-01-06 15:34:08','2020-01-06 15:34:08','philip',0);
INSERT INTO `users` VALUES (2,'bob','Bob','Smith','User account for Bob Smith','$2b$12$SjOFE3rvjz4Jpn4MUa5T9uS3TeoAXcgNhhRJOa0xiu2sQh0ux7pAK','bob@somewhere.com',6,64,'2019-08-28 11:46:08','2020-01-08 17:20:47','2020-01-08 17:20:47','philip',0);
INSERT INTO `users` VALUES (3,'frank','Frank','Black','User account for Frank Black test 123','$2b$12$W7l0QbKXrOLKh2.7IDYI3.eP7gAsIzbJ730HJ0bgyd8.FGmrr4Je6','frank@somewhere.com',2,65,'2019-08-28 11:46:08','2020-01-12 17:11:44','2020-01-12 17:11:44','frank',0);
INSERT INTO `users` VALUES (4,'evan','Evan','Troon','Account for Evan','$2b$12$fRYijfQhLPT1wH9/akayhu/1F9l1IgozFbXG4uMk0p5H2u66/tUVy','evan@someone.com',1,70,'2019-09-02 15:14:53','2020-01-06 15:34:20','2020-01-06 15:34:20','philip',1);
INSERT INTO `users` VALUES (6,'dylan','Dylan','Troon','Dylan Troon','$2b$12$kyttQmBiV7Gxn4NdG1gh1eOwfzfp8LEy5.PUhMLcUyWlVd8F9DSku','dylan@somewhere.com',1,65,'2019-09-02 16:50:50','2020-01-07 13:49:47','2020-01-07 13:49:47','philip',1);
