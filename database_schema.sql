DROP DATABASE IF EXISTS quizycash;
CREATE DATABASE quizycash;
USE quizycash;
CREATE TABLE `client_admin` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `admin_user_name` VARCHAR(255) NOT NULL,
  `admin_password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME,
  `deleted_at` DATETIME,
  `updated_at` DATETIME
);

CREATE TABLE `game_room` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `game_room_name` VARCHAR(255) DEFAULT NULL,
  `game_category` VARCHAR(50) DEFAULT NULL,
  `max_players` MEDIUMINT DEFAULT 0,
  `game_theme` VARCHAR(50) DEFAULT NULL,
  `min_buy_in` MEDIUMINT DEFAULT 0,
  `max_buy_in` MEDIUMINT DEFAULT 0,
  `game_status` BOOLEAN DEFAULT 0,
  `created_at` DATETIME DEFAULT NULL,
  `updated_at` DATETIME DEFAULT NULL,
  `deleted_at` DATETIME DEFAULT NULL,
  `big_blind` MEDIUMINT DEFAULT 0,
  `small_blind` MEDIUMINT DEFAULT 0
);

CREATE TABLE `game_statistics` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT
);

CREATE TABLE `user` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `user_name` VARCHAR(255) DEFAULT NULL,
  `password` VARCHAR(255) DEFAULT NULL,
  `virtual_money` DOUBLE DEFAULT 0,
  `user_availability` BOOLEAN DEFAULT 0,
  `gender` VARCHAR(20) DEFAULT NULL,
  `date_of_birth` DATE DEFAULT NULL,
  `first_name` VARCHAR(50) DEFAULT NULL,
  `last_name` VARCHAR(50) DEFAULT NULL,
  `profile_image` VARCHAR(255) DEFAULT NULL,
  `created_at` DATETIME DEFAULT NULL,
  `updated_at` DATETIME DEFAULT NULL,
  `deleted_at` DATETIME DEFAULT NULL,
  `email` VARCHAR(50) DEFAULT NULL,
  `country` VARCHAR(50) DEFAULT NULL
);

CREATE TABLE `Session` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `session_info` VARCHAR(255) NOT NULL,
  `user_id` INTEGER,
  `game_room_id` INTEGER NOT NULL,
  `created_at` DATETIME DEFAULT NULL,
  `updated_at` DATETIME DEFAULT NULL,
  `expired_at` DATETIME DEFAULT NULL
);

CREATE INDEX `idx_session__game_room_id` ON `Session` (`game_room_id`);

CREATE INDEX `idx_session__user_id` ON `Session` (`user_id`);

ALTER TABLE `Session` ADD CONSTRAINT `fk_session__game_room_id` FOREIGN KEY (`game_room_id`) REFERENCES `game_room` (`id`);

ALTER TABLE `Session` ADD CONSTRAINT `fk_session__user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

CREATE TABLE `player` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `player_action` VARCHAR(255) NOT NULL,
  `balance` VARCHAR(255) DEFAULT 0,
  `is_dealer` BOOLEAN DEFAULT 0,
  `user_id` INTEGER NOT NULL,
  `has_turn` BOOLEAN DEFAULT 0,
  `game_room` INTEGER NOT NULL,
  `is_active` BOOLEAN DEFAULT 0,
  `created_at` DATETIME DEFAULT NULL,
  `updated_at` DATETIME DEFAULT NULL,
  `deleted_at` DATETIME DEFAULT NULL
);

CREATE INDEX `idx_player__game_room` ON `player` (`game_room`);

CREATE INDEX `idx_player__user_id` ON `player` (`user_id`);

ALTER TABLE `player` ADD CONSTRAINT `fk_player__game_room` FOREIGN KEY (`game_room`) REFERENCES `game_room` (`id`);

ALTER TABLE `player` ADD CONSTRAINT `fk_player__user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

CREATE TABLE `betting_round` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `betting_no` MEDIUMINT DEFAULT 0,
  `question` MEDIUMINT DEFAULT 0,
  `hint` MEDIUMINT DEFAULT 0,
  `active_players` BIGINT DEFAULT 0,
  `player_id` INTEGER,
  `game_room` INTEGER NOT NULL
);

CREATE INDEX `idx_betting_round__game_room` ON `betting_round` (`game_room`);

CREATE INDEX `idx_betting_round__player_id` ON `betting_round` (`player_id`);

ALTER TABLE `betting_round` ADD CONSTRAINT `fk_betting_round__game_room` FOREIGN KEY (`game_room`) REFERENCES `game_room` (`id`);

ALTER TABLE `betting_round` ADD CONSTRAINT `fk_betting_round__player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`);

CREATE TABLE `live_game_play` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `user_id` BIGINT DEFAULT 0,
  `pot_amount` DOUBLE DEFAULT 0,
  `player_action` VARCHAR(50) NOT NULL,
  `buy_in` DOUBLE DEFAULT 0,
  `joined_at` DATETIME DEFAULT NULL,
  `left_at` DATETIME DEFAULT NULL,
  `game_room_id` INTEGER NOT NULL,
  `betting_round_id` INTEGER
);

CREATE INDEX `idx_live_game_play__betting_round_id` ON `live_game_play` (`betting_round_id`);

CREATE INDEX `idx_live_game_play__game_room_id` ON `live_game_play` (`game_room_id`);

ALTER TABLE `live_game_play` ADD CONSTRAINT `fk_live_game_play__betting_round_id` FOREIGN KEY (`betting_round_id`) REFERENCES `betting_round` (`id`);

ALTER TABLE `live_game_play` ADD CONSTRAINT `fk_live_game_play__game_room_id` FOREIGN KEY (`game_room_id`) REFERENCES `game_room` (`id`);

CREATE TABLE `user_statistics` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `games_played` MEDIUMINT DEFAULT 0,
  `games_won` MEDIUMINT DEFAULT 0,
  `no_of_folds` MEDIUMINT DEFAULT 0
)
