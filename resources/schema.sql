DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    email VARCHAR NOT NULL,
    is_admin BOOLEAN DEFAULT 'false' NOT NULL
);

INSERT INTO users (id, name, email, is_admin) VALUES ('1e33cf0b-5421-48bc-848c-0aeb3557a843', 'Admin Person','admin@gmail.com', true);
INSERT INTO users (id, name, email, is_admin) VALUES ('881b04c0-a960-46c9-a184-e7568decdb95', 'John Prozsiac','john.prozsiac@gmail.com', false);
