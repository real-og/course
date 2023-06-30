CREATE USER 'english_app' IDENTIFIED BY 'english_pass';
GRANT ALL PRIVILEGES ON english.* TO 'english_app';

CREATE TABLE IF NOT EXISTS roles
(
    id serial primary key NOT NULL,
    name varchar(21) NOT NULL
);

INSERT INTO roles (id, name)
VALUES (1, 'admin'),
       (2, 'moderator'),
       (3, 'user');

CREATE TABLE IF NOT EXISTS users
(
    id serial primary key NOT NULL,
    name varchar(51),
    email varchar(51) NOT NULL,
    password varchar(111) NOT NULL,
    joinDate timestamp default CURRENT_TIMESTAMP(1),
    age int,
    isActive boolean NOT NULL default true,
    role int default 3,
    FOREIGN KEY (role) REFERENCES roles (id) ON DELETE SET NULL
);

CREATE TABLE words
(
    id serial primary key NOT NULL,
    word varchar(21) NOT NULL,
    translate varchar(111)
);
CREATE UNIQUE INDEX idx_unique_word ON words (word);

CREATE TABLE songs
(
    id serial primary key NOT NULL,
    name varchar(41) NOT NULL,
    author varchar(41) NOT NULL default 'Undefined',
    album varchar(41) NOT NULL default 'Single'
);

CREATE TABLE user_word
(
    id serial primary key NOT NULL,
    idWord int NOT NULL,
    idUSER int NOT NULL,
    isKnown boolean,
    FOREIGN KEY (idWord) REFERENCES words (id) ON DELETE CASCADE,
    FOREIGN KEY (idUser) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT unique_pair UNIQUE (idWord, idUser)
);

CREATE TABLE song_user
(
    id serial primary key NOT NULL,
    idSong int NOT NULL,
    idUSER int NOT NULL,
    isKnown boolean,
    startDate timestamp default NOW(),
    FOREIGN KEY (idSong) REFERENCES songs (id) ON DELETE CASCADE,
    FOREIGN KEY (idUser) REFERENCES users (id) ON DELETE CASCADE
);


-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "course_user";