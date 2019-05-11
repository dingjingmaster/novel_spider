-- novel spider 表创建

-- 信息表
CREATE TABLE IF NOT EXISTS `novel_info` (
    `nid` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,                   -- id 自增
    `name` VARCHAR(300) DEFAULT NULL,
    `author` VARCHAR(300) DEFAULT NULL,
    `category` VARCHAR(300) DEFAULT NULL,
    `describe` TEXT DEFAULT NULL,
    `complete` TINYINT DEFAULT 0,                                       -- 0:不确定; 1. 连载; 2:完结
    `book_url` VARCHAR(300) NOT NULL UNIQUE,
    `img_url` TEXT DEFAULT NULL,
    `img_content` MEDIUMBLOB DEFAULT NULL,
    `chapter_base_url` TEXT NOT NULL,
    `create_time` TIMESTAMP NOT NULL,
    `update_time` TIMESTAMP NOT NULL,
    `hot` TINYINT DEFAULT 0,                                            -- 是否好书
    `cp` TINYINT DEFAULT 0,                                             -- 0:版权书 1:非版权书
    `lock` TINYINT DEFAULT 0                                            -- 0:未上锁；1:上锁 上锁条件：完结+信息确认没问题
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- 章节内容表
CREATE TABLE IF NOT EXISTS `novel_chapter` (
    `cid` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,                   -- id 自增
    `nid` BIGINT UNSIGNED NOT NULL,
    `index` INT UNSIGNED NOT NULL,                                      -- 章节序
    `chapter_url` VARCHAR(300) NOT NULL UNIQUE,                         -- 章节url
    `name` VARCHAR(300) DEFAULT NULL,
    `content` MEDIUMTEXT DEFAULT NULL,
    `update_time` TIMESTAMP NOT NULL,
    `lock` TINYINT DEFAULT 0                                            -- 0:未上锁；1:上锁
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
