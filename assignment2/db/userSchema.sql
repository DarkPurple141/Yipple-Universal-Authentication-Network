CREATE TABLE users(
	uid SERIAL PRIMARY KEY,
	username TEXT NOT NULL UNIQUE,
	passhash TEXT NOT NULL
);

CREATE TABLE creds(
	 uid INTEGER,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    email TEXT NOT NULL,
    phonenum TEXT NOT NULL,
    funds INTEGER
);

INSERT INTO users (username, passhash) VALUES ('admin', 'alice');
INSERT INTO users (username, passhash) VALUES ('Bobby\" DROP TABLES;--', '\" OR \"1\"=\"1\"');

INSERT INTO creds (uid, name, address, email, phonenum, funds) VALUES ('1', 'Alice Administrator', 'Omnipotent', 'alice@alice.com', '+313 373 8483', 31333337);
INSERT INTO creds (uid, name, address, email, phonenum, funds) VALUES ('2', 'Bob Bandit', 'Nowhere', 'bob@bob.com', '-123 456 7890', 1337);
