Eventlog DB:

CREATE TABLE AuthLogs(
   id SERIAL PRIMARY KEY     		NOT NULL, 
   datetime       VARCHAR(255)    	NOT NULL,
   operation      VARCHAR(255)      NOT NULL,
   user_id 		  INT				NOT NULL
);


    CREATE TABLE OperationLogs(
   id SERIAL PRIMARY KEY     			NOT NULL, 
   datetime       		VARCHAR(255)    NOT NULL,
   operation      		VARCHAR(255)    NOT NULL,
   user_id 		 		INT				NOT NULL,
   source_id 	  		INT				NOT NULL,
   modified_attribute	VARCHAR(255),
   old_value			VARCHAR(500),
   new_value			VARCHAR(500)
);


CREATE TABLE AdminLogs(
   id SERIAL PRIMARY KEY     			NOT NULL, 
   datetime       		VARCHAR(255)    NOT NULL,
   operation      		VARCHAR(255)    NOT NULL,
   admin_id 		 	INT				NOT NULL,
   user_id 	  			INT				NOT NULL,
   modified_attribute	VARCHAR(255),	
   old_value			VARCHAR(255),	
   new_value			VARCHAR(255)
);
