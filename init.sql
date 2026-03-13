-- ======================================
-- MemeHub Database Initialization
-- ======================================

DROP DATABASE IF EXISTS meme_site;

CREATE DATABASE meme_site
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE meme_site;

-- ======================================
-- 用户表
-- ======================================

CREATE TABLE users (
    uid INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    user_status VARCHAR(20) DEFAULT 'user',
    is_banned BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ======================================
-- 梗图表
-- ======================================

CREATE TABLE memes (
    pid INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    image_base64 LONGTEXT NOT NULL,
    uploader_uid INT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_meme_user
    FOREIGN KEY (uploader_uid)
    REFERENCES users(uid)
    ON DELETE CASCADE
);

-- ======================================
-- 评分表
-- ======================================

CREATE TABLE ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uid INT NOT NULL,
    pid INT NOT NULL,
    rating FLOAT NOT NULL,

    UNIQUE(uid,pid),

    CONSTRAINT fk_rating_user
    FOREIGN KEY (uid)
    REFERENCES users(uid)
    ON DELETE CASCADE,

    CONSTRAINT fk_rating_meme
    FOREIGN KEY (pid)
    REFERENCES memes(pid)
    ON DELETE CASCADE
);

-- ======================================
-- 评论表
-- ======================================

CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uid INT NOT NULL,
    pid INT NOT NULL,
    content VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_comment_user
    FOREIGN KEY (uid)
    REFERENCES users(uid)
    ON DELETE CASCADE,

    CONSTRAINT fk_comment_meme
    FOREIGN KEY (pid)
    REFERENCES memes(pid)
    ON DELETE CASCADE
);

-- ======================================
-- 收藏表
-- ======================================

CREATE TABLE favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uid INT NOT NULL,
    pid INT NOT NULL,

    UNIQUE(uid,pid),

    CONSTRAINT fk_fav_user
    FOREIGN KEY (uid)
    REFERENCES users(uid)
    ON DELETE CASCADE,

    CONSTRAINT fk_fav_meme
    FOREIGN KEY (pid)
    REFERENCES memes(pid)
    ON DELETE CASCADE
);

-- ======================================
-- 索引优化
-- ======================================

CREATE INDEX idx_meme_pid ON memes(pid);
CREATE INDEX idx_meme_user ON memes(uploader_uid);
CREATE INDEX idx_comment_pid ON comments(pid);
CREATE INDEX idx_rating_pid ON ratings(pid);

-- 搜索优化（标题 + 描述）
ALTER TABLE memes ADD FULLTEXT(title,description);

-- ======================================
-- 默认管理员账号（可选）
-- username: admin
-- password: admin123
-- ======================================

INSERT INTO users (
    username,
    password,
    email,
    user_status
) VALUES (
    'admin',
    'admin123',
    'admin@example.com',
    'admin'
);