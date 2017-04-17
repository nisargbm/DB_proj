-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: localhost    Database: document_tracking
-- ------------------------------------------------------
-- Server version	5.7.17-0ubuntu0.16.04.2

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
-- Table structure for table `Document`
--

DROP TABLE IF EXISTS `Document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Document` (
  `sr_no` int(11) NOT NULL AUTO_INCREMENT,
  `doc_id` int(11) NOT NULL,
  `Date_of_receipt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `sender` varchar(255) NOT NULL,
  `receiver` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`sr_no`),
  KEY `doc_id` (`doc_id`),
  CONSTRAINT `Document_ibfk_1` FOREIGN KEY (`doc_id`) REFERENCES `Document_details` (`doc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Document`
--

LOCK TABLES `Document` WRITE;
/*!40000 ALTER TABLE `Document` DISABLE KEYS */;
INSERT INTO `Document` VALUES (1,1,'2017-04-11 15:44:33','HEMANG','NISARG'),(2,1,'2017-04-11 15:37:51','NISARG','HEMANG'),(3,1,'2017-04-11 15:44:33','HEMANG','NISARG'),(4,1,'2017-04-11 15:44:47','HEMANG','HEMANG'),(5,2,'2017-04-16 12:56:02','NISARG','HEMANG'),(6,2,'2017-04-16 12:56:55','HEMANG','NISARG'),(7,3,'2017-04-17 10:14:48','NISARG','HEMANG'),(8,4,'2017-04-17 10:15:22','NISARG','HEMANG'),(9,5,'2017-04-17 10:15:43','NISARG','HEMANG');
/*!40000 ALTER TABLE `Document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Document_details`
--

DROP TABLE IF EXISTS `Document_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Document_details` (
  `doc_id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(255) NOT NULL,
  `number_of_documents` int(11) NOT NULL,
  `organisation` varchar(255) NOT NULL,
  `details` varchar(255) DEFAULT NULL,
  `move_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`doc_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Document_details`
--

LOCK TABLES `Document_details` WRITE;
/*!40000 ALTER TABLE `Document_details` DISABLE KEYS */;
INSERT INTO `Document_details` VALUES (1,'vjti pointer',2,'vjti','vjti pointer request','2017-04-11 21:07:30'),(2,'subject',2,'Vjti','details','2017-04-16 18:26:02'),(3,'abcde',1,'abcde','ancde','2017-04-17 15:44:47'),(4,'ksaj',1,'olweanhohnre','lnearnoli','2017-04-17 15:45:21'),(5,'abcde',1,'abcde','abcde','2017-04-17 15:45:43');
/*!40000 ALTER TABLE `Document_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Inward`
--

DROP TABLE IF EXISTS `Inward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Inward` (
  `inward_id` int(11) NOT NULL AUTO_INCREMENT,
  `place_of_receiving` varchar(255) NOT NULL,
  `doc_id` int(11) NOT NULL,
  PRIMARY KEY (`inward_id`),
  KEY `doc_id` (`doc_id`),
  CONSTRAINT `Inward_ibfk_1` FOREIGN KEY (`doc_id`) REFERENCES `Document_details` (`doc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Inward`
--

LOCK TABLES `Inward` WRITE;
/*!40000 ALTER TABLE `Inward` DISABLE KEYS */;
/*!40000 ALTER TABLE `Inward` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Mobile`
--

DROP TABLE IF EXISTS `Mobile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Mobile` (
  `mobile_no` int(11) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  UNIQUE KEY `mobile_no` (`mobile_no`),
  KEY `fr2` (`user_id`),
  CONSTRAINT `fr2` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Mobile`
--

LOCK TABLES `Mobile` WRITE;
/*!40000 ALTER TABLE `Mobile` DISABLE KEYS */;
/*!40000 ALTER TABLE `Mobile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Name`
--

DROP TABLE IF EXISTS `Name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Name` (
  `First_name` varchar(255) NOT NULL,
  `Middle_name` varchar(255) NOT NULL,
  `Last_name` varchar(255) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  KEY `fr1` (`user_id`),
  CONSTRAINT `fr1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Name`
--

LOCK TABLES `Name` WRITE;
/*!40000 ALTER TABLE `Name` DISABLE KEYS */;
/*!40000 ALTER TABLE `Name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Outward`
--

DROP TABLE IF EXISTS `Outward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Outward` (
  `outward_id` int(11) NOT NULL AUTO_INCREMENT,
  `sending_place` varchar(255) NOT NULL,
  `to_whom_addressed` varchar(255) NOT NULL,
  `doc_id` int(11) NOT NULL,
  PRIMARY KEY (`outward_id`),
  KEY `doc_id` (`doc_id`),
  CONSTRAINT `Outward_ibfk_1` FOREIGN KEY (`doc_id`) REFERENCES `Document_details` (`doc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Outward`
--

LOCK TABLES `Outward` WRITE;
/*!40000 ALTER TABLE `Outward` DISABLE KEYS */;
/*!40000 ALTER TABLE `Outward` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Postal_charges`
--

DROP TABLE IF EXISTS `Postal_charges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Postal_charges` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `type_of_post` varchar(50) DEFAULT NULL,
  `estimated_cost` int(11) NOT NULL,
  `outward_id` int(11) NOT NULL,
  PRIMARY KEY (`post_id`),
  KEY `outward_id` (`outward_id`),
  CONSTRAINT `Postal_charges_ibfk_1` FOREIGN KEY (`outward_id`) REFERENCES `Outward` (`outward_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Postal_charges`
--

LOCK TABLES `Postal_charges` WRITE;
/*!40000 ALTER TABLE `Postal_charges` DISABLE KEYS */;
/*!40000 ALTER TABLE `Postal_charges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Process`
--

DROP TABLE IF EXISTS `Process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Process` (
  `movement_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comment` varchar(255) DEFAULT 'No Comments',
  `user_id` varchar(255) NOT NULL,
  `doc_id` int(11) NOT NULL,
  `status` varchar(50) DEFAULT 'PENDING',
  KEY `user_id` (`user_id`),
  KEY `doc_id` (`doc_id`),
  CONSTRAINT `Process_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`),
  CONSTRAINT `Process_ibfk_2` FOREIGN KEY (`doc_id`) REFERENCES `Document_details` (`doc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Process`
--

LOCK TABLES `Process` WRITE;
/*!40000 ALTER TABLE `Process` DISABLE KEYS */;
INSERT INTO `Process` VALUES ('2017-04-11 21:07:30','No Comments','HEMANG',1,'CREATED'),('2017-04-11 21:07:30','cool','NISARG',1,'ACCEPTED'),('2017-04-11 21:07:51','this is accepted','HEMANG',1,'REJECTED'),('2017-04-11 21:14:32','No Comments','NISARG',1,'PENDING'),('2017-04-11 21:14:47','','HEMANG',1,'REJECTED'),('2017-04-16 18:26:02','No Comments','NISARG',2,'CREATED'),('2017-04-16 18:26:02','Valid document.','HEMANG',2,'ACCEPTED'),('2017-04-16 18:26:55','No Comments','NISARG',2,'PENDING'),('2017-04-17 15:44:48','No Comments','NISARG',3,'CREATED'),('2017-04-17 15:44:48','No Comments','HEMANG',3,'PENDING'),('2017-04-17 15:45:21','No Comments','NISARG',4,'CREATED'),('2017-04-17 15:45:22','No Comments','HEMANG',4,'PENDING'),('2017-04-17 15:45:43','No Comments','NISARG',5,'CREATED'),('2017-04-17 15:45:43','No Comments','HEMANG',5,'PENDING');
/*!40000 ALTER TABLE `Process` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `user_id` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email_id` varchar(255) NOT NULL,
  `department` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email_id` (`email_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES ('HEMANG','$5$rounds=535000$H7BhaXD2PqUojAFw$AjV4/aLozMSgp.MTVueP7tPhUCUWfIXtuZdwtv8MIR8','hemang@gmail.com','ELEX'),('NISARG','$5$rounds=535000$YsQjqrmn8OzWP7cW$8N10ZlxHl.nddz87cDKqJIp0wK9S37OmoCD2dnAalQA','nisarg@gmail.com','CSIT');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-17 15:49:28
