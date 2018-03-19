/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50638
Source Host           : localhost:3306
Source Database       : zhihu

Target Server Type    : MYSQL
Target Server Version : 50638
File Encoding         : 65001

Date: 2018-03-19 00:24:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ip_list
-- ----------------------------
DROP TABLE IF EXISTS `ip_list`;
CREATE TABLE `ip_list` (
  `ip` varchar(50) NOT NULL,
  `port` varchar(20) NOT NULL,
  `speed` float DEFAULT NULL,
  `proxy_type` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
