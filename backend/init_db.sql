CREATE DATABASE IF NOT EXISTS meme_club CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE meme_club;

CREATE TABLE IF NOT EXISTS users (
  uid INT PRIMARY KEY AUTO_INCREMENT,
  username_b64 VARCHAR(255) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  email_b64 VARCHAR(255) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  user_status VARCHAR(20) NOT NULL DEFAULT 'user',
  is_banned BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS memes (
  pid INT PRIMARY KEY AUTO_INCREMENT,
  title_b64 VARCHAR(255) NOT NULL,
  description_b64 TEXT NOT NULL,
  image_b64 LONGTEXT NOT NULL,
  review_status VARCHAR(20) NOT NULL DEFAULT 'pending',
  uploader_uid INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_memes_user FOREIGN KEY (uploader_uid) REFERENCES users(uid)
);

CREATE TABLE IF NOT EXISTS comments (
  cid INT PRIMARY KEY AUTO_INCREMENT,
  content_b64 VARCHAR(512) NOT NULL,
  meme_pid INT NOT NULL,
  user_uid INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_comments_meme FOREIGN KEY (meme_pid) REFERENCES memes(pid),
  CONSTRAINT fk_comments_user FOREIGN KEY (user_uid) REFERENCES users(uid)
);

CREATE TABLE IF NOT EXISTS ratings (
  rid INT PRIMARY KEY AUTO_INCREMENT,
  score DECIMAL(2, 1) NOT NULL,
  meme_pid INT NOT NULL,
  user_uid INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_ratings_meme_user UNIQUE (meme_pid, user_uid),
  CONSTRAINT fk_ratings_meme FOREIGN KEY (meme_pid) REFERENCES memes(pid),
  CONSTRAINT fk_ratings_user FOREIGN KEY (user_uid) REFERENCES users(uid)
);

CREATE TABLE IF NOT EXISTS favorites (
  fid INT PRIMARY KEY AUTO_INCREMENT,
  meme_pid INT NOT NULL,
  user_uid INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_favorites_meme_user UNIQUE (meme_pid, user_uid),
  CONSTRAINT fk_favorites_meme FOREIGN KEY (meme_pid) REFERENCES memes(pid),
  CONSTRAINT fk_favorites_user FOREIGN KEY (user_uid) REFERENCES users(uid)
);
