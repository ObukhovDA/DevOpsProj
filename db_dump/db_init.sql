CREATE DATABASE IF NOT EXISTS `devops` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `devops`;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `alembic_version` (`version_num`) VALUES
('ef2c890c1fc0');


CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `text` text NOT NULL,
  `rating` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `images` (
  `id` varchar(250) NOT NULL,
  `file_name` varchar(250) NOT NULL,
  `MIME` varchar(250) NOT NULL,
  `MD5` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `price` int(11) NOT NULL,
  `image_id` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `roles` (`id`, `title`, `description`) VALUES
(1, 'Админинстратор', 'Админ'),
(2, 'Модератор', 'Модер'),
(3, 'Пользователь', 'Юзер');


CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `login` varchar(100) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `login`, `password_hash`, `last_name`, `first_name`, `middle_name`, `role_id`) VALUES
(1, 'admin', 'pbkdf2:sha256:600000$DaCXvH9lPMs7Qo42$4b403a8cd3c2ff3ff6f9a4109128710b1e1981ce5478314fcec12c6efb989d79', 'admin', 'admin', NULL, 1),
(2, 'moder', 'pbkdf2:sha256:600000$dUj4mcYkA8F7TcV3$9d3975af800ee06770aaa589934663e92089c7b0c54c8c5ed665d369ba1bf051', 'moder', 'moder', NULL, 2),
(3, 'user1', 'pbkdf2:sha256:600000$9K1MaNm0aN7ZXBWi$1311dea15f2dbbd8874aac025468b094e9332e24ea28fe76fcefdb4b10d065c9', 'user1', 'user1', NULL, 3),
(4, 'user2', 'pbkdf2:sha256:600000$m5ID6a6kanpEyPi8$59b324fe3c4ff52f343525e10042182e976dd698daedc961bab6b366fe079478', 'user2', 'user2', NULL, 3);

ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);


ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_comments_item_id_items` (`item_id`),
  ADD KEY `fk_comments_user_id_users` (`user_id`);


ALTER TABLE `images`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `items`
  ADD PRIMARY KEY (`id`);
  
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);
  
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_users_login` (`login`),
  ADD KEY `fk_users_role_id_roles` (`role_id`);


ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

ALTER TABLE `items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;


ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;


ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;


ALTER TABLE `comments`
  ADD CONSTRAINT `fk_comments_item_id_items` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`),
  ADD CONSTRAINT `fk_comments_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);


ALTER TABLE `users`
  ADD CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
COMMIT;

