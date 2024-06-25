CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`, `server_id`) REFERENCES `users` (`user_id`, `server_id`)
);

CREATE TABLE IF NOT EXISTS `users` (
    `user_id` varchar(20) NOT NULL,
    `server_id` varchar(20) NOT NULL,
    `points` INTEGER NOT NULL,
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`, `server_id`)
);

CREATE TABLE IF NOT EXISTS `bets` (
    `bet_id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user1_id` varchar(20) NOT NULL,
    `user1_server_id` varchar(20) NOT NULL,
    `user2_id` varchar(20) NOT NULL,
    `user2_server_id` varchar(20) NOT NULL,
    `wager` TEXT NOT NULL,
    `points` INTEGER NOT NULL,
    `user1_confirm` BOOLEAN DEFAULT 0,
    `user2_confirm` BOOLEAN DEFAULT 0,
    `winner_id` varchar(20) DEFAULT NULL,
    `winner_server_id` varchar(20) DEFAULT NULL,
    FOREIGN KEY (`user1_id`, `user1_server_id`) REFERENCES `users` (`user_id`, `server_id`),
    FOREIGN KEY (`user2_id`, `user2_server_id`) REFERENCES `users` (`user_id`, `server_id`),
    FOREIGN KEY (`winner_id`, `winner_server_id`) REFERENCES `users` (`user_id`, `server_id`)
);
