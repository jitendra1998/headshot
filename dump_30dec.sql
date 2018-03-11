-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: quizycash
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

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
-- Table structure for table `Session`
--

DROP TABLE IF EXISTS `Session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_info` varchar(255) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `game_room_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `expired_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_session__game_room_id` (`game_room_id`),
  KEY `idx_session__user_id` (`user_id`),
  CONSTRAINT `fk_session__game_room_id` FOREIGN KEY (`game_room_id`) REFERENCES `game_room` (`id`),
  CONSTRAINT `fk_session__user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Session`
--

LOCK TABLES `Session` WRITE;
/*!40000 ALTER TABLE `Session` DISABLE KEYS */;
/*!40000 ALTER TABLE `Session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `betting_round`
--

DROP TABLE IF EXISTS `betting_round`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `betting_round` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `betting_no` mediumint(9) DEFAULT '0',
  `question` mediumint(9) DEFAULT '0',
  `hint` mediumint(9) DEFAULT '0',
  `active_players` bigint(20) DEFAULT '0',
  `player_id` int(11) DEFAULT NULL,
  `game_room` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_betting_round__game_room` (`game_room`),
  KEY `idx_betting_round__player_id` (`player_id`),
  CONSTRAINT `fk_betting_round__game_room` FOREIGN KEY (`game_room`) REFERENCES `game_room` (`id`),
  CONSTRAINT `fk_betting_round__player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `betting_round`
--

LOCK TABLES `betting_round` WRITE;
/*!40000 ALTER TABLE `betting_round` DISABLE KEYS */;
/*!40000 ALTER TABLE `betting_round` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_admin`
--

DROP TABLE IF EXISTS `client_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client_admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_user_name` varchar(255) NOT NULL,
  `admin_password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_admin`
--

LOCK TABLES `client_admin` WRITE;
/*!40000 ALTER TABLE `client_admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `client_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_room`
--

DROP TABLE IF EXISTS `game_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_room` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_room_name` varchar(255) DEFAULT NULL,
  `game_category` varchar(50) DEFAULT NULL,
  `max_players` mediumint(9) DEFAULT '0',
  `game_theme` varchar(50) DEFAULT NULL,
  `min_buy_in` mediumint(9) DEFAULT '0',
  `max_buy_in` mediumint(9) DEFAULT '0',
  `game_status` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `big_blind` mediumint(9) DEFAULT '0',
  `small_blind` mediumint(9) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_room`
--

LOCK TABLES `game_room` WRITE;
/*!40000 ALTER TABLE `game_room` DISABLE KEYS */;
INSERT INTO `game_room` VALUES
(0,'game1','soccer-world-cup',10,'sports',1,10,1,'2017-08-03 15:36:45',NULL,NULL,2,1),
            (1,'game1','soccer-world-cup',10,'sports',3,30,1,'2017-08-03 15:36:45',NULL,NULL,6,3),
            (2,'game2','chemistry',10,'science',2,20,1,'2017-09-13 21:40:05',NULL,NULL,4,2),
            (3,'game3','social_sciences',10,'social_sciences',4,20,1,'2017-09-20 08:19:32',NULL,NULL,8,4),
            (4,'game4','sciences',10,'sciences',2,20,1,'2017-09-13 21:40:05',NULL,NULL,4,2),
            (5,'game5','soccer-world-cup',10,'sports',2,30,1,'2017-09-20 08:19:32',NULL,NULL,4,2),
            (6,'game6','football',10,'science',5,50,1,'2017-09-13 21:40:05',NULL,NULL,10,5),
            (7,'game7','europe-capitals',10,'other',1,10,1,'2017-09-20 08:19:32',NULL,NULL,2,1),
            (8,'game8','pop-art',10,'other',2,20,1,'2017-08-03 15:36:45',NULL,NULL,4,2),
            (9,'game9','world-capitals',10,'other',1,10,1,'2017-09-13 21:40:05',NULL,NULL,2,1),
            (10,'game10','astronomy',10,'other',3,30,1,'2017-09-20 08:19:32',NULL,NULL,6,3);
/*!40000 ALTER TABLE `game_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_statistics`
--

DROP TABLE IF EXISTS `game_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_statistics`
--

LOCK TABLES `game_statistics` WRITE;
/*!40000 ALTER TABLE `game_statistics` DISABLE KEYS */;
/*!40000 ALTER TABLE `game_statistics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `live_game_play`
--

DROP TABLE IF EXISTS `live_game_play`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_game_play` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) DEFAULT '0',
  `pot_amount` double DEFAULT '0',
  `player_action` varchar(50) NOT NULL,
  `buy_in` double DEFAULT '0',
  `joined_at` datetime DEFAULT NULL,
  `left_at` datetime DEFAULT NULL,
  `game_room_id` int(11) NOT NULL,
  `betting_round_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_live_game_play__betting_round_id` (`betting_round_id`),
  KEY `idx_live_game_play__game_room_id` (`game_room_id`),
  CONSTRAINT `fk_live_game_play__betting_round_id` FOREIGN KEY (`betting_round_id`) REFERENCES `betting_round` (`id`),
  CONSTRAINT `fk_live_game_play__game_room_id` FOREIGN KEY (`game_room_id`) REFERENCES `game_room` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `live_game_play`
--

LOCK TABLES `live_game_play` WRITE;
/*!40000 ALTER TABLE `live_game_play` DISABLE KEYS */;
/*!40000 ALTER TABLE `live_game_play` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `player`
--

DROP TABLE IF EXISTS `player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_action` varchar(255) NOT NULL,
  `balance` varchar(255) DEFAULT '0',
  `is_dealer` tinyint(1) DEFAULT '0',
  `user_id` int(11) NOT NULL,
  `has_turn` tinyint(1) DEFAULT '0',
  `game_room` int(11) NOT NULL,
  `is_active` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_player__game_room` (`game_room`),
  KEY `idx_player__user_id` (`user_id`),
  CONSTRAINT `fk_player__game_room` FOREIGN KEY (`game_room`) REFERENCES `game_room` (`id`),
  CONSTRAINT `fk_player__user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player`
--

LOCK TABLES `player` WRITE;
/*!40000 ALTER TABLE `player` DISABLE KEYS */;
/*!40000 ALTER TABLE `player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `virtual_money` double DEFAULT '0',
  `user_availability` tinyint(1) DEFAULT '0',
  `gender` varchar(20) DEFAULT NULL,
  `date_of_birth` varchar(12) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'java_guy','java_guy',1000000,0,'male','1997-05-02','java','guy',NULL,'2017-09-06 06:12:55',NULL,NULL,'java_guy@gmail.com','India'),(2,'pratik','pratik',1000000,0,'male','1997-02-02','Pratik','Salunkhe',NULL,'2017-09-06 06:14:06',NULL,NULL,'pratik.sal13@gmail.com','India'),(3,'python','python',9999000,0,'male','1998-02-02','python','program',NULL,'2017-09-06 06:22:57',NULL,NULL,'python@gmail.com','India'),(4,'ruby','ruby',10000000,0,'male','1998-02-02','ruby','program',NULL,'2017-09-06 06:23:42',NULL,NULL,'ruby@gmail.com','India'),(5,'a','12345',9995386.01,0,'male','1925-02-05','avinash','goje',NULL,'2017-09-06 06:34:38',NULL,NULL,'a@gmail.com','ind'),(6,'b','12345',999997708,0,'male','1998-05-05','type','script',NULL,'2017-09-06 06:37:25',NULL,NULL,'b@gmail.com','india'),(7,'c','12345',10003209,0,'male','1995-05-05','avina','goj',NULL,'2017-09-07 09:24:14',NULL,NULL,'c@gmail.com','India'),(8,'d','12345',100000000,0,'male','1998-05-03','pen','pen',NULL,'2017-09-07 09:24:36',NULL,NULL,'d@gmail.com','india'),(9,'lalala','12345',100000000,0,'male','1995-02-02','lala','lala',NULL,'2017-09-07 12:48:51',NULL,NULL,'lalala@lala.com','lalala'),(10,'Shellzcrypt','123400000',100,0,'female','2011-11-11','Shilpa','K',NULL,'2017-09-08 15:00:20',NULL,NULL,'shilpa@myraatechnologies.com','India'),(11,'abc@gmail.com','12345',100000000,0,'male','1995-06-03','abc','xyz',NULL,'2017-09-08 15:06:43',NULL,NULL,'abc@gmail.com','ind'),(12,'lala','lala',12353620,0,'male','1995-06-12','lala','lala',NULL,'2017-09-20 13:17:31',NULL,NULL,'lala@email.com','india'),(13,'poly','poly',991000,0,'male','2014-05-04','asd','as',NULL,'2017-09-20 13:18:40',NULL,NULL,'poly@gmail.com','ind'),(14,'rhishikesh','12345',100000000,0,'male','1993-04-05','rhishi','mhatre',NULL,'2017-09-20 13:24:41',NULL,NULL,'rhishikesh@gmail.com','India'),(15,'kriti','K.n1202.',10000020,0,'male','2017-09-07','kriti','nidhi',NULL,'2017-09-20 13:29:00',NULL,NULL,'kritinidhi1202@gmail.com','India'),(16,'MyraaTron','123',10000000,0,'male','2011-11-11','Myraa','Tron',NULL,'2017-09-20 13:31:05',NULL,NULL,'my@my.com','India');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_statistics`
--

DROP TABLE IF EXISTS `user_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `games_played` mediumint(9) DEFAULT '0',
  `games_won` mediumint(9) DEFAULT '0',
  `no_of_folds` mediumint(9) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_statistics`
--

LOCK TABLES `user_statistics` WRITE;
/*!40000 ALTER TABLE `user_statistics` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_statistics` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-30  7:27:31
