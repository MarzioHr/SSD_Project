# Development Team Project - Dutch National Cyber Security Centre Suspect Sources System


## Table of Contents
1. [Introduction](#introduction)
2. [Background](#background)
3. [Proposed System](#proposed_system)
4. [Simple User Interface](#simple_user_interface)
5. [Prerequisites](#prerequisites)
6. [PostgreSQL Database](#postgresql_database)
7. [PostgreSQL Connection in Python Code and Security Measures](#postgresql-connection-in-python-code-and-security-measures)
8. [Python Modules](#python-modules)
9. [Folder Structure](#folder-structure)
12.[Reference List](#reference-list)

### Introduction
This project serves as the Development Team Project: Coding Output assignment for Secure Software Development March 2021. The assignment focuses on the second deliverable, a practical development of your design from Unit 3. 

In total, the submitted code for the Development Team Project: Coding Output assignment aims to implement two major parts:
1.	The NCSC Suspect Sources System
2. 	Demo Implementation with a Simple User Interface


### Background
The National Cyber Security Centre (NCSC) is the Netherlands' consolidated data hub and cyber security knowledge centre. NCSC's objective is to strengthen Dutch society's digital resilience, resulting in a better, broader, and stable digital world. The NCSC provides expert insight into cyber-security innovations, threats, and risks (Government of the Netherlands, N.D.).

### Proposed System
One of NCSC's main tasks is to continuously monitor all suspect sources on the internet and to alert public organisations of new threats (Government of the Netherlands, N.D.).

The system that will be developed for the Dutch NCSC will allow authorised employees to search, amend and create entries for the suspect sources database. These can then be accessed and utilised by other staff members to assist in the work they do. 

The system will need to adhere to the domain-specific requirements mentioned above. It is assumed that the system will be used by three groups of users, each with their own set of access permissions and controls: Specialists, Administrators and External Authorities. 

### Simple User Interface
The project furthermore includes a simple user interface for three groups of users namely, Administrators, Specialists and External Authorities. 

The interface has individual menu for each user as follows:

1. **Administrators** will be able to:

	o Create new user
	o Modify user
	o Desactivate user
	o Unlock user

2. **Specialists** will be able to:

	o Create source 
	o View/Modify source

3. **External Authorities** will be able to:

	o View source
    
### Prerequisites
Prior to running the python project, you will need to install a few external libraries:
- PostgreSQL Database v1.2.2 to conform to open-source requirements via python lib [http://github.com/python-postgres/fe]
- Pylint v2.7.4 to check for syntax errors and enforce PEP-8 styling via the python lib [https://github.com/PyCQA/pylint/]
- Fernet symmetric encryption to encrypt and decrypt database credentials and content via .bin file [https://cryptography.io/en/latest/fernet.html] 
- Argon2 v1.3 for password hashing via the “argon2-cffi” python lib [https://github.com/hynek/argon2-cffi]


You can use the following pip commands to install the libraries directly:
```
pip3 install py-postgresql
```
```
pip3 install pylint
```
```
pip3 install cryptography
```
```
pip3 install argon2-cffi
```

This project has been coded in python 2.7.17 and it is recommended to use the same version when executing the code.

![Python Version](https://i.imgur.com/jmGiZfX.png)


### PostgreSQL Database 
The project uses three main databases for the implementation:

1. **Authentication**
2. **Data**
3. **Eventlog**

**Authentication:**
Authentication contains the 'users' table. 

When registering a new user, a new data row is inserted into the 'users' table containing the user's id, first_name, last_name, dob, user_role, desired username, password as an Argon2 hash, last_login, status and email.

Once an user is registed, an automatic email is sent to the user containing the desired username and the hashed password. 

When logging into the Suspect Sources system for the first time, the user will be prompted to change his/her password which will be eventually be updated as hash into the 'users' table, to enhance the security of the account.

When logging into an already existing account, the user needs to input a username and password. Once done, the entered username are compared against all entries in the table. If it exists, the entered password is hashed and the hash itself is compared against the saved entry. If the hash, the username and email address are line up with the existing data, the user is successfully authenticated in the system and can continue.

*'authentication.users' table columns:*
![users table columns](https://i.imgur.com/TFdbCMP.png)

*'authentication.users' table sample data:*
![users data table](https://i.imgur.com/hRUVYut.png)


**Data:**
The 'sources' table contains the details of the sources created from the system by the Specialist users. 

When creating a new source, a new data row is inserted into the 'sources' table containing the source's id, name, url, threat_level, descritption, creation_date and modified_date.

When searching for sources in the system, the entered data is queried against the appropriate attributes of the 'sources' table and the details are displayed back to the user. If a user actions an modify, the appropriate data row is updated on this database.

*'data.sources' table columns:*
![sources table columns](image url from imgur to be placed)

*'data.sources' table sample data:*
![sources data table](image url from imgur to be placed)


**Eventlog:**
The eventlog database serves as the log database that stores all traces of user actions on the system. The three main tables of the eventlog are: AuthLogs, OperationLogs and AdminLogs. 

* AuthLogs
The table 'AuthLogs' stores logs for authentications actions for existing accounts as successful login, modified password, locked account and unsuccessful login by user from their respective interface. For all actions, the data includes the when the action was conducted, what operation it is (successful login, modified password, locked account or unsuccessful login) and who actioned it (user id). 

*'eventlog.authlog' table columns:*
![authlog table columns](image url from imgur to be placed)

*'eventlog.authlog' table sample data:*
![authlog data table](image url from imgur to be placed)

* OperationLogs
The table 'OperationLogs' stores all traces for actions on sources. For all actions the data includes when the action was conducted, what action it is (modify/view), who actioned it (user id). For modify actions it includes the record that was modified, the old value prior to the change and the new value after the change.

*'eventlog.operationlog' table columns:*
![operationlog table columns](image url from imgur to be placed)

*'eventlog.operationlog' table sample data:*
![operationlog data table](image url from imgur to be placed)

* AdminLogs
The table 'AdminLogs' stores all traces for actions on users. For all actions, the data includes when the action was conducted, what action it is (modify/unlock/desactivate), who actioned it (user id), and what attribute was effected (e.g. 'status'). For modify actions it includes the record that was modified, the old value prior to the change and the new value after the change.

*'eventlog.adminlog' table columns:*
![adminlog table columns](image url from imgur to be placed)

*'eventlog.adminlog' table sample data:*
![adminlog data table](image url from imgur to be placed)

### PostgreSQL Connection in Python Code and Security Measures
For the PostgreSQL database insert, update, and read operations, a database user is required. For this project, the user 'client'@'localhost' was created which is used for all interface operations. Prior to executing any operations, the python code needs to authenticate with the database. Instead of adding the PostgreSQL username and password into the code as plain text, we have opted to encrypt the credentials and store them as a binary file in the 'config' folder for security purposes (using Fernet to encrypt). The encryption script and clear text credentials prior to encryption can be viewed in the 'setup' folder. When running the project, the 'dbconnection' module will attempt to decrypt the credentials binary file using the credentials.bin file stored in the same 'config' folder. Only if that is successful, the interface will be able to operate (register, login,create, modify, view, search). In an actual deployment, you would be able to limit the 'config' folder access controls, so that only the code is able to access the folder and read the 'credentials.bin' and 'key.bin' files, not the user himself. This would make it difficult for the user to obtain the actual credentials and connect to the database directly.

Another layer of security is provided by the application of the least privilege principle. The user 'client'@'localhost' is only granted privileges that are vital for the interface operations. These are mainly select (for search and login), insert (for registration and create) and update (for modify) rights for the specific data tables. This ensures that in case of a breach or SQL injection attack using this user, the data that may be effected is limited. A full list of granted privileges for the user can be seen here:

!['client'@'localhost' privileges](image url from imgur to be placed)

SQL injection attacks are a big point for security concerns and are still regarded as the most critical web application security risk according to the OWASP Top Ten list (OWASP, 2020). The same is valid for this python project as well. The staff interface is asking for user inputs, which - if no security measures are taken - can be manipulated to execute such injections. All the malicious user would have to do, for instance, is to escape the actual username select query and insert an attack in its place, e.g.:

The statement below passes username from the client directly to the database, without performing any sort of check or validation. This sort of code is ripe for inviting Python SQL injection. 
```
# BAD EXAMPLES. DON'T DO THIS!
cursor.execute("SELECT status FROM users WHERE username = '" + username + '"); 
```
The above statements should be converted to the below statement  where username is passed as a named parameter. Now, the database will use the specified type and value of username when executing the query, offering protection from Python SQL injection.
```
# SAFE EXAMPLES. DO THIS!
cursor.execute("SELECT status FROM users WHERE username = %s'", (username, ));
```

### Python Modules
In total, the Suspect Sources system project includes a total of seven python modules:
1. **main.py:** executes Dutch NCSC Suspect Sources System main interface

2. **interface.py:** main user interface that includes handler functions to call the other modules

3. **dbconnection.py:** module that decrypts the PostgreSQL credentials and establishes the primary connection to the db

4. **authentication.py:** module that handles the login and registration operations, as well as the password hashing functionality

5. **operations.py:** module that handles the main portions of the create, search, view and modify operations, as well as sanitization of inputs 

6. **admin_operations.py:** module that handles the all the administration events of the project

7. **notifications.py:** module that handles all the events of the project which require to be notified by emails

For the execution of the actual program (user interface), please run ```python3 main.py```.

### Folder Structure
The python modules are all located on the root folder of the project. Furthermore, the project includes three additional folders: 'config', 'setup' and 'pycache'.

**Config:**

Config includes five binary files that are used for the code execution. In an actual deployment, this folder would need to enforce strict access controls to protect the sensitive files inside of it:
1. **banner.bin:** file that contains the initial lines to be printed when the interface is executed

2. **credentials.bin:** file that contains the encrypted PostgreSQL credentials (encrypted via Fernet)

3. **key.bin:** file that contains the key for the Fernet encryption and which is used to decrypt the credentials when the code is executed

4. **privacy_policy.bin:** file that contains the system's privacy policy statements in order to comply with legal obligations 

5. **terms_conditions.bin:** file that contains the sets of rules and guidelines that users must agree to and follow in order to use and access the system

**Setup:**

Setup includes files to understand the initial setup of the project. In an actual deployment, this folder would not exist. In total, the folder includes three files:

1. **credential_encryption.py:** the python script used to initially encrypt the clear credentials and outputs the credentials.bin file as seen in the 'config' folder

2. **fernet_key_gen.py:** the python script used to generate a fresh fernet key and outing it in the key.bin file as seen in the 'config' folder

3. **psql_clear_credentials.txt:** displays the PostgreSQL credentials prior to being encrypted (format: "host:database:password:user")












### Reference List

Baum, D., Dietrich, J., Anslow, C. and Müller, R. (2018) Visualizing Design Erosion: How Big Balls of Mud are Made. 2018 IEEE Working Conference on Software Visualization (VISSOFT): 122-126. Available from: https://ieeexplore.ieee.org/abstract/document/8530139 [Accessed 23 March 2021]. 

Government of the Netherlands (N.D.) Fighting Cybercrime in the Netherlands. Government of the Netherlands. Available from: https://www.government.nl/topics/cybercrime/fighting-cybercrime-in-the-netherlands [Accessed 15 March 2021].

Hillenius, G. (2013)' Open Source Only' at Dutch Police Internet Forensics. European Union. Available from: https://joinup.ec.europa.eu/collection/open-source-observatory-osor/news/open-source-only-dutch-p [Accessed 15 March 2021].

Hijazi, H., Alqrainy, S., Muaidi, H. & Khdour, T. (2014) Identifying Causality Relation between Software Projects Risk Factors. International Journal of Software Engineering and Its Applications 8(2): 51-58.

Kalske, M., Mäkitalo, N.  & Mikkonen, T. (2018). Challenges When Moving from Monolith to Microservice Architecture. Available from https://www.researchgate.net/publication/323312732_Challenges_When_Moving_from_Monolith_to_Microservice_Architecture  [Accessed 21 March 2021].

OWASP (2017) OWASP Top 10 – 2017: The Ten Most Critical Web Application Security Risks. Available from: https://owasp.org/www-pdf-archive/OWASP_Top_10-2017_%28en%29.pdf.pdf [Accessed 20 March 2021].

OWASP (2018) Proactive Controls. Available from: https://owasp.org/www-project-proactive-controls/ [Accessed 23 March 2021]. 

Politie (2019) Privacy Statement. Available from https://www.politie.nl/algemeen/privacy.html?sid=228463d3-72e3-4434-8947-933a8e3d3756 [Accessed 20 March 2021].

Spiekermann, S. (2012). The Challenges of Privacy by Design. Communications of The ACM – CACM 55 (7): 38-40. DOI: 10.1145/2209249.2209263.