New user creation:

INSERT INTO users (FIRST_NAME, LAST_NAME, DOB, USER_ROLE, USERNAME, PASSWORD, LAST_LOGIN, STATUS, EMAIL)	
 VALUES ('Russel', 'Crow', '1996-12-02', 3, 'r.crow', '$argon2id$v=19$m=102400,t=2,p=8$VmCtEoAhcer6EJ2ujdMSZA$IhRKHBiKJnkCeP3PbQirpw', null, 1, 'sshiwantha+1@gmail.com'),
	('Robin', 'Newton', '1970-01-01', 2, 'r.newton', '$argon2id$v=19$m=102400,t=2,p=8$ep556/VaRNg+uKW5PR9EOw$QlZOkzjg8Tlq2dAk6PbxpA', null, 1, 'sshiwantha+12@gmail.com'),
	('Shannon', 'Leavitt', '1970-01-21', 1, 's.leavitt', '$argon2id$v=19$m=102400,t=2,p=8$W8xxDHZKQoD4aP908DwUww$2a5lGoR0mpFXvZXaMaeLSg', null, 1, 'sshiwantha+124@gmail.com');
    
 
Sample data sources:

INSERT INTO sources (NAME, URL, THREAT_LEVEL, DESCRIPTION, CREATION_DATE, MODIFIED_DATE)
 VALUES ('WordPress_Malware', 'http://www.plattan.ru', 1, 'Wordpress website attack', '2020-04-12', '2020-04-12'),
	('DDos_Attack', 'http://www.player-codec.biz', 4, 'Denial-of-service (DDoS) attacks', '2020-04-12', '2020-04-12'),
	('XXS_Attack', 'http://www.plusscan5.com', 2, 'Cross-site scripting', '2020-04-12', '2020-04-12'),
	('MitM_Attack', 'http://www.ranbanda.ku', 3, 'Man-in-the-middle', '2020-04-12', '2020-04-12'),
	('Password_Sniff', 'http://www.newnw.uk', 4, 'Brute-force and dictionary attack', '2020-04-12', '2020-04-12'),
	('SQL_injection_attack', 'http://www.sltatck.lk', 4, 'Uses malicious SQL code for backend DB manipulation to access information', '2020-04-12', '2020-04-12'),
	('Capcom ransomware attack', 'http://www.capc.com', 4, 'Hackers gained access via vulnerable VPN', '2020-04-12', '2020-04-12'),
	('uXSS Attack DDGO', 'http://www.duckduckgo.com', 4, 'The vulnerability was discovered in DuckDuckGo Privacy Essentials', '2020-04-12', '2020-04-12'),
	('Cisco routers_RCE', 'http://tools.cisco.com/security/center/content', 4, 'The authentication bypass and system command injection vulnerabilities', '2020-04-12', '2020-04-12'),
    ('WebStresser', 'http://webstresser.org/', 1, 'Worlds biggest marketplace for purchasing Denial of Service attacks. The administrators of the DDoS marketplace were arrested on 24 April 2018 as a result of Operation Power Off, a complex investigation led by the Dutch Police and the UK’s National Crime Agency with the support of Europol and a dozen law enforcement agencies from around the world.', '2017-01-01', '2018-05-01');