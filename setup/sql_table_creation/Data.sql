Data DB:

CREATE TABLE sources(
   id SERIAL PRIMARY 	KEY     	NOT NULL, 
   name           	VARCHAR(255)  	NOT NULL,
   url            	VARCHAR(255)  	NOT NULL,
   threat_level	  	INT				NOT	NULL,
   description		VARCHAR(500) 	NOT	NULL,
   creation_date	DATE			NOT	NULL,
   modified_date	DATE			NOT	NULL
);