/*
Navicat MySQL Data Transfer

Source Server         : 本地mysql
Source Server Version : 50635
Source Host           : localhost:3306
Source Database       : leodb

Target Server Type    : MYSQL
Target Server Version : 50635
File Encoding         : 65001

Date: 2018-11-27 17:39:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `wterror`
-- ----------------------------
DROP TABLE IF EXISTS `wterror`;
CREATE TABLE `wterror` (
  `id` varchar(36) COLLATE utf8_bin NOT NULL,
  `watcher_id` varchar(36) COLLATE utf8_bin DEFAULT NULL,
  `creat_time` datetime DEFAULT NULL,
  `updata_time` datetime DEFAULT NULL,
  `work_for` varchar(1024) COLLATE utf8_bin DEFAULT NULL,
  `erro_type` varchar(5) COLLATE utf8_bin DEFAULT NULL,
  `log_type` varchar(1) COLLATE utf8_bin DEFAULT NULL,
  `del_type` varchar(1) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `watcher_id` (`watcher_id`),
  CONSTRAINT `wterror_ibfk_1` FOREIGN KEY (`watcher_id`) REFERENCES `watcher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of wterror
-- ----------------------------
INSERT INTO `wterror` VALUES ('29a655a1-f212-11e8-bf0c-f44d307d3586', 'af_138C', '2018-11-27 15:00:45', '2018-11-27 15:00:45', '均不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29b6f770-f212-11e8-b0cb-f44d307d3586', 'af_220C', '2018-11-27 15:00:45', '2018-11-27 15:00:45', '服务器不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29bbb25e-f212-11e8-9670-f44d307d3586', 'af_016C', '2018-11-27 15:00:45', '2018-11-27 15:00:45', '单IP设备，设备异常', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29c79940-f212-11e8-a3f5-f44d307d3586', 'af_044C', '2018-11-27 15:00:45', '2018-11-27 15:00:45', '均不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29cc542e-f212-11e8-aad5-f44d307d3586', 'af_424C', '2018-11-27 15:00:45', '2018-11-27 15:00:45', '均不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29cec52e-f212-11e8-a338-f44d307d3586', 'af_238C', '2018-11-27 15:00:45', '2018-11-27 15:00:45', '设备不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29d5f121-f212-11e8-b3e4-f44d307d3586', 'af_291C', '2018-11-27 15:00:46', '2018-11-27 15:00:46', '均不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29d83b0f-f212-11e8-9168-f44d307d3586', 'af_292C', '2018-11-27 15:00:46', '2018-11-27 15:00:46', '均不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29df6700-f212-11e8-9c80-f44d307d3586', 'af_324C', '2018-11-27 15:00:46', '2018-11-27 15:00:46', '均不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29e421f0-f212-11e8-813e-f44d307d3586', 'af_202C', '2018-11-27 15:00:46', '2018-11-27 15:00:46', '设备不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29e903f0-f212-11e8-89ff-f44d307d3586', 'af_411C', '2018-11-27 15:00:46', '2018-11-27 15:00:46', '设备不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29edbede-f212-11e8-91c0-f44d307d3586', 'af_183C', '2018-11-27 15:00:46', '2018-11-27 15:00:46', '设备不在线', '0', '0', '0');
INSERT INTO `wterror` VALUES ('29f279cf-f212-11e8-b7a3-f44d307d3586', 'af_207C', '2018-11-27 15:00:46', '2018-11-27 15:00:46', '均不在线', '0', '0', '0');
