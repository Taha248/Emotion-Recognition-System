/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 10.4.6-MariaDB : Database - emotion_recognition
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`emotion_recognition` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `emotion_recognition`;

/*Table structure for table `samples` */

DROP TABLE IF EXISTS `samples`;

CREATE TABLE `samples` (
  `sampleID` varchar(10) NOT NULL,
  `age` int(10) NOT NULL,
  `gender` enum('M','F') NOT NULL,
  `duration` int(10) NOT NULL,
  `emotion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `samples` */

insert  into `samples`(`sampleID`,`age`,`gender`,`duration`,`emotion`) values 
('0001',20,'M',20,'Sad'),
('0002',22,'M',20,'Sad'),
('0003',4,'M',20,'Surprised'),
('0004',51,'F',20,'Surprised');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
