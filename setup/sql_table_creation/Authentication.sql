Authentication DB:


CREATE TABLE users(
	id SERIAL PRIMARY 	KEY 			NOT NULL,
	first_name		VARCHAR(255) 		NOT NULL,
	last_name		VARCHAR(255) 		NOT NULL,
	dob        		DATE				NOT NULL,
	user_role		INT					NOT NULL,
	username		VARCHAR(255) UNIQUE	NOT NULL,
	password		VARCHAR(255)		NOT NULL,
	last_login		DATE,
	status			INT					NOT NULL,
	email			VARCHAR(255) UNIQUE	NOT NULL
);