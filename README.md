# Development Team Project: Suspect Sources System for the Dutch National Cyber Security Centre


## Table of Contents
1. [Project Introduction](#introduction)
2. [Setup](#setup)
3. [File Structure](#file-structure)
4. [Database Structure](#database-structure)
5. [User Roles and Use Cases](#user-roles-and-use-cases)
6. [Security](#security)
7. [Email Notification](#email-notification)
8. [Testing](#testing)
9. [Reference List](#reference-list)


## Project Introduction
This project serves as the Development Team Project: Coding Output assignment for the Secure Software Development Module of University of Essex Online - March 2021. The assignment focuses on the second deliverable: a practical development of a previously proposed design.

In total, the submitted code for the Development Team Project assignment aims to implement two major parts:

1.	The NCSC Suspect Sources Core System and Database
2.	Prototype of a Command-Line Interface to Access the System

The National Cyber Security Centre (NCSC) is the Netherlands' consolidated data hub and cyber security knowledge centre. NCSC's objective is to strengthen Dutch society's digital resilience, resulting in a better, broader, and stable digital world. The NCSC provides expert insight into cyber-security innovations, threats, and risks (Government of the Netherlands, N.D.).

One of NCSC's main tasks is to continuously monitor all suspect sources on the internet and alert public authorities and organisations of new threats (Government of the Netherlands, N.D.).

The System that will be developed for the Dutch NCSC will allow authorised employees to search, amend and create entries for the suspect sources database. These can then be accessed and utilised by other staff members to assist in the work they do. It is assumed that the System will be used by three groups of users, each with its own set of access permissions and controls: Specialists, Administrators and External Authorities.


## Setup
### Prerequisites
The project has been coded in python 3.6.9, and it is recommended to use the same version when executing the code on your end.

![Python Version](https://i.imgur.com/8wrOuZU.png)
 
Also, before running the python project, you will need to install a few external libraries:
* Argon2 v1.3 for password hashing via the "argon2-cffi" python lib
* Fernet symmetric encryption to encrypt and decrypt database credentials and content via .bin file
* Psycopg2 as a Python Connector to the PostgreSQL database
* Stdiomask, validator_collection and secrets for the interface inputs and validations

You can use the following pip commands to install the libraries directly or follow the requirements.txt file:
```
pip3 install argon2-cffi
pip3 install cryptography
pip3 install stdiomask
pip3 install psycopg2
pip3 install validator_collection
pip3 install secrets
```

### Database Setup
For the System's database, PostgreSQL v12.6 was used. We have added a "setup" folder that includes setup scripts for all of the database tables and some sample data for Users and Sources.

![PostgreSQL Version](https://i.imgur.com/DT0eLjb.png)
 
For the default users, you can use the following username/password combinations to authenticate once added to the DB:
* Role Administrator: `s.leavitt` / `ZTBJs36*eyzh^msx`
* Role Specialist: `r.newton` / `F44aF#rhVgs9hAH8`
* Role External Authority: `r.crow` / `3S2PkFEn*#twx*g4`

The Administrator account can then be used to create new users in the System to test all use cases and scenarios.

### Database Credential Encryption
To ensure that the CLI can connect to your database, you will need to set up a DB access and include the corresponding encrypted credentials in the "config" folder. The encryption can be done in the following way:
1.	Generate database user with sufficient privileges (exact privileges will be explained in the chapter "Security")
2.	Format the credentials in the following format: `{database_host}:{default_database}:{username}:{password}` (for reference see the "psql_clear_credentials.txt" file in the 'setup' folder)
3.	Generate an own Fernet master key (via "fernet_key_gen.py" in "setup") or use the one currently saved in the "config" folder ("key.bin" in "config")
4.	Run the cleartext file through Fernet encryption using the script "credential_encryption.py" in the "setup" folder and save the output as a binary file
5.	Rename the output to "credentials.bin" and move it into the "config" folder
6.	All done! The CLI should now be able to connect to the DB using your "credentials.bin" file


## File Structure
### Folder Structure
The project includes the main Python modules and requirements file inside the root folder. In addition, there are three subfolders: 'config', 'setup' and 'policies'.

**Config:**
Config includes three binary files used for the code execution and one HTML file used to send formatted email notifications to users. In an actual deployment, this folder would need to enforce strict access controls to protect the sensitive files inside of it:
1.	**banner.bin**: file that contains the initial lines to be printed when the interface is executed.
2.	**credentials.bin**: file that includes the encrypted PostgreSQL credentials (encrypted via Fernet).
3.	**key.bin**: file that contains the key for the Fernet encryption and which is used to decrypt the credentials when the code is executed.
4.	**email_body.html**: file contains the email template used to communicate to the users.

**Setup:**
Setup includes files to understand the initial setup of the project. In an actual deployment, this folder would not exist. In total, the folder includes three files:
1.	**credential_encryption.py**: the python script used to encrypt the clear credentials initially and outputs the credentials.bin file as seen in the 'config' folder.
2.	**fernet_key_gen.py**: the python script used to generate a new fernet master key and outputs the key.bin file as seen in the 'config' folder.
3.	**psql_clear_credentials.txt**: displays the PostgreSQL credentials prior to being encrypted (format: "host:database:user:password").
4.	**sql_table_creation**: includes all of the SQL setup scripts for the database tables and some sample data for the users and sources table.

**Policies:**
Policies includes files that demonstrate the System's compliance to the law and the agreement terms for user to access the System. In total, the folder contains two files:
1.	**privacy_policy.bin**: file that includes the System's privacy policy statements to comply with legal obligations.
2.	**terms_conditions.bin**: file containing the sets of rules and guidelines that users must agree to and follow to use and access the System.

### Python Modules
In total, the Suspect Sources system project includes a total of eight python modules:
1.	**main.py**: executes the NCSC Suspect Sources System prototype interface.
2.	**interface.py**: main user interface contained as a class that provides handler functions to call the other modules and prompts dialogues and user inputs.
3.	**dbconnection.py**: module that decrypts the PostgreSQL credentials and establishes the primary connection to the DB.
4.	**authentication.py**: module that handles the login operations, as well as the password hashing functionality.
5.	**operations.py**: module that holds the main portions of the specialist and authority user role operations. Includes source creation, search, modification, as well as the change password functionality.
6.	**admin_operations.py**: module that handles the main portion of the administration user role operations. Includes user creation, modification, deactivation as well as the unlock functionality.
7.	**notification.py**: module that handles the email notification templates and content. It is called by the other modules whenever a notification needs to be triggered.
8.	**eventlog.py**: module that handles the log creation of the System to ensure traceability and accountability for users and their actions.

For the execution of the Command-Line Interface, please run either `python main.py` or `python3 main.py` (depending on your Python installation).


## Database Structure
The project uses three main databases for the implementation:
1.	**Authentication**: contains the user information for authentication.
2.	**Data**: contains the suspect source information.
3.	**Eventlog**: contains the system logs and traces of all user actions.

### Authentication
The Authentication database contains the 'users' table.

When registering a new user, a new data row is inserted into the 'users' table containing the user's id, first_name, last_name, dob, user_role, username, password as an Argon2 hash, last_login, status and email.

Once a user is registered, an automatic email is sent to the user containing the desired username and the hashed password. When logging into the Suspect Sources system for the first time, the user will be prompted to change his/her password, which will then be hashed and saved/updated into the 'users' table to enhance the security of the account.

When logging into an already existing account, the user needs to input a username and password. Once done, the entered username is compared against all entries in the table. If it exists, the entered password is hashed, and the hash itself is compared against the saved entry. If the hash and the username line up with the existing data, the user is successfully authenticated in the System and can continue.

The user_role attribute denotes the role for that specific user. In total, this attribute can have one of three values:
```
1 = Administrator
2 = Specialist
3 = External Authority
```

The status attribute denotes the current status of that specific user. In total, this attribute can have one of three values:
```
1 = Active
2 = Deactivated (soft-deleted)
3 = Locked (due to failed authentication attempts)
```

!['authentication.users' Columns and Attribute Types](https://i.imgur.com/SWP5kCQ.png)

*Figure 1: 'authentication.users' Columns and Attribute Types*

!['authentication.users' Sample Data](https://i.imgur.com/XEVuCpU.png)

*Figure 2: 'authentication.users' Sample Data*


### Data
The 'sources' table contains the details of suspect sources inside of the System. New entries can be created by the Specialist user role from within the CLI.

When creating a new source, a new data row is inserted into the 'sources' table containing the source's id, name, url, threat_level, description, creation_date and modified_date.

If a new source is added to the System, an email notification is triggered to all users in the System with the role of an external authority.

When searching for sources in the System, the entered data is queried against the appropriate attributes of the 'sources' table, and the details are displayed back to the user. If a user actions a modification, the applicable data row is updated on this database.

!['data.sources' Columns and Attribute Types](https://i.imgur.com/8brslyw.png)

*Figure 3: 'data.sources' Columns and Attribute Types*

!['data.sources' Sample Data](https://i.imgur.com/SnMic84.png)

*Figure 4: 'data.sources' Sample Data*


### Eventlog
The eventlog database serves as the log database that stores all traces of user actions on the System. The three main tables of the eventlog are: 'authlogs', 'operationlogs' and 'adminlogs'.

The table 'authlogs' stores logs for authentication actions of existing accounts, such as successful login, change of password, locked account due to failed attempts, and unsuccessful login attempts for users with the status "deactivated" and "locked". For all actions, the data includes the date and time when the action was conducted, what operation it is (successful login, modified password, locked account or unsuccessful login) and who actioned it (user id).

!['eventlog.authlogs' Sample Data](https://i.imgur.com/bXpmpoz.png)

*Figure 5: 'eventlog.authlogs' Sample Data*

The table 'operationlogs' stores all traces for actions on the source data. For all events the data includes when the action was conducted, what action it is (creation/modification/view), what source was effected (source id) and who actioned it (user id). For modify actions, it includes the record that was modified, the old value before the change and the new value after the change.

!['eventlog.operationlogs'](https://i.imgur.com/jR1lGLM.png)

*Figure 6: 'eventlog.operationlogs' Sample Data*

The table 'adminlogs' stores all traces of administrator actions on user data. For all events, the data includes when the action was conducted, what action it is (creation/modification/unlock/deactivate), what user is affected (user id), and who actioned it (admin id). For modify actions, the logs include the attribute that was modified, the old value before the change and the new value after the change.

!['eventlog.adminlogs' Sample Data](https://i.imgur.com/SfTDnmh.png)

*Figure 7: 'eventlog.adminlogs' Sample Data*


## User Roles and Use Cases
As highlighted in the chapter "Background", it is assumed that the System will be used by three groups of users, each with its own set of access permissions and controls. Each user role has a different CLI view and operations he/she can conduct.

**Administrators** can: 
* Create New Users
* Modify Existing Users
* Deactivate Existing Users (soft delete)
* Unlock Existing Users (if locked due to failed login attempts)

**Specialists** can:
* Search for Existing Suspect Sources
* Modify Existing Suspect Sources
* Create New Suspect Sources
* Change their Password

**External Authorities** can:
* Search for Existing Suspect Sources
* Change their Password

The "Administrator" role is responsible for User Management. Administrators can create new users, as well as modify, deactivate and unlock existing users. When creating a new user, the administrator will need to input the user's first and last name, the date of birth, the email address, and the user's role (administrator, specialist, authority). The System then automatically generates a username (format: first letter of first name + `.` + full last name + running number if existent already) and a 12-character password including special characters, letters and numbers. The login information is then sent to the user's email address directly.

The "Specialist" role is reserved for internal employees of the NCSC. Specialists are responsible for the data maintenance of the Suspect Sources System. The role can create new source data, search for existing data, and modify the data. When creating a new Suspect Source record in the System, an email notification is triggered to all External Authority users in the System to notify them of a newly identified source. The Authorities can then login to view details and a description of the added threat.

The "Authority" role is reserved for external entities that need access to the Suspect Sources system. These would include public authorities and organisations that need to be kept informed about any new threats that are identified. Authorities are limited to only being able to view existing sources on the database. The user role does not have rights to modify existing data or create new records.


## Security
### Cryptography
Within the System, two types of encryptions are being utilised:
* **Fernet's** symmetric encryption for encrypting and decrypting database credentials, as well as SMTP credentials
* **Argon2** for password hashing


Fernet enables encryption of files and messages so that they cannot be manipulated or read without access to the master key. Fernet is an implementation of symmetric (also known as "secret key") authenticated cryptography. Fernet is built on top of several standard cryptographic primitives. Specifically, it uses AES with a 128-bit key for encryption and HMAC using SHA256 for authentication (Gaynor, 2020). Within the System, Fernet is used to encrypt and decrypt the database and SMTP credentials within the "config" folder. Furthermore, it provides the possibility of encoding data within the database if required in the full implementation.

For the System's password hashing, Argon2 is utilised. Argon2 is a password-hashing function that summarises the state of the art design of memory-hard functions. The algorithm has a modern ASIC-resistant and GPU-resistant secure key derivation function. Thus, if configured correctly, it provides a higher degree of cracking resistance than other algorithms, such as PBKDF2, Bcrypt and Scrypt (Nakov, 2018).


### SQL Injection
SQL injection attacks are a big point for security concerns and are still regarded as the most critical web application security risk according to the OWASP Top Ten list (OWASP, 2020). The same is valid for this python project as well. The CLI is asking for user inputs, which can be manipulated to execute such injections if no security measures are taken.

All the malicious user would have to do, for instance, is to escape the actual username select query and insert an attack in its place, e.g.:

The statement below passes the username from the client directly to the database without performing any check or validation. Doing so opens the System up to be exploited.
```
# BAD EXAMPLES. DON'T DO THIS!
cursor.execute("SELECT status FROM users WHERE username = " + username + ";") 
```

The above statements should be converted to the below statement where the username is passed as a named parameter. Now, the database will use the specified type and value of username when executing the query, offering protection from Python SQL injection.
```
# SAFE EXAMPLES. DO THIS!
cursor.execute("SELECT status FROM users WHERE username = %{val}s;", {'val': username})
```


### Database Security
For the PostgreSQL database insert, update, and read operations, a database user is required. For this project, the user 'client' was created, which is used for all interface operations. Before executing any operations, the python code needs to authenticate with the database. Instead of adding the PostgreSQL username and password into the code as plain text, we have opted to encrypt the credentials and store them as a binary file in the 'config' folder for security purposes (using Fernet to encrypt). The encryption script and clear text credentials prior to encryption can be viewed in the 'setup' folder. When running the project, the 'dbconnection' module will attempt to decrypt the credentials binary file using the 'credentials.bin' file stored in the same 'config' folder. Only if that is successful, the interface will operate (register, login, create, modify, view). In an actual deployment, you would limit the 'config' folder access controls so that only the code can access the folder and read the 'credentials.bin' and 'key.bin' files, not the user himself. This would make it difficult for the user to obtain the actual credentials and connect to the database directly.


### Principle of Least Privilege
Another layer of security is provided by the application of the least privilege principle. The user 'client' is only granted privileges that are vital for the interface operations. These are mainly select (for login and view), insert (for registration and create) and update (for modify) rights for the specific data tables. This ensures that in case of a breach or SQL injection attack using this user, the data that may be affected is limited. A complete list of granted privileges for the user can be seen here:
```
GRANT SELECT, INSERT, UPDATE ON users TO client;
GRANT SELECT, USAGE, UPDATE ON users_id_seq TO client;
GRANT SELECT, INSERT, UPDATE ON sources TO client;
GRANT SELECT, USAGE, UPDATE ON sources_id_seq TO client;
GRANT INSERT ON authlogs, adminlogs, operationlogs TO client;
GRANT SELECT, USAGE ON adminlogs_id_seq, authlogs_id_seq, operationlogs_id_seq TO client;
```


## Email Notification
Throughout the System, we are using three email notifications to be sent out to the users. The emails are sent via an external SMTP (Gmail in the case of this implementation) and can be configured in the "notification.py" module. The three types of notifications that are sent out are:
- A ***Registration Email*** that is sent to new users when an Administrator signs them up and contains the auto-generated username and password
- A ***Source Creation Notification*** that is sent to all Authority Users (User Role = 3) whenever a Specialist creates a new source
- A ***Changed Password Confirmation*** whenever a password of a user is changed from within the CLI

![Registration Email](https://i.imgur.com/0GjvNMC.png)

*Figure 8: Registration Email*

![Suspect Source Notification](https://i.imgur.com/sPNAANu.png)

*Figure 9: Suspect Source Notification*

![Changed Password Confirmation](https://i.imgur.com/6v7sOSq.png)

*Figure 10: Changed Password Confirmation*


## Testing
There are three levels of testing employed within the System:
- **Unit Testing**
- **Continuous Review**
- **Functional Testing**

Unit testing is a type of software testing where units or components of the software are tested individually. In the Suspect Sources system, this would mean the outputs of the various functions are tested to confirm that they fulfill expectations in terms of typing and values. Ideally, for the complete system implementation, a framework such as "unittest" or "Robot" could be used to create automated test cases that verify the outputs on-demand. For instance, whenever a major code update is pushed, the unit tests could then be run before merging the code to confirm that previous functions are not affected by the update.

In the case of the prototype implementation, we have instead opted to go with print-based unit tests due to the tight timeline. While developing and adjusting code, print statements were used to verify the outputs of functions and ensure that the individual units of the System are working as expected.

Continuous Source Code review is done to ensure the structure, style, complexity, syntax, and security aspect of the source code as a whole is guaranteed. This can be done with the help of static code analysis tools called Linters. For this project, we decided to go with two different Linters to cover all bases:

**Pylint** for checking the syntax, complexity, styling and referencing of the code basis.

**Bandit** for checking security due to its capability of flagging vulnerabilities and their severeness.

By following the Pylint feedback, we raised the final score of the code basis to 9.96/10. The only part that couldn't conform to the standards was the notification module. Some features of the notification module included the HTML styling of the notification emails, which exceeded the line limit of 100 characters.

![Pylint Final Score for Source Code](https://i.imgur.com/UlYX8nk.png)

*Figure 11: Pylint Final Score for Source Code*

Bandit initially flagged a remaining possible SQL injection vector that could have been exploited if overlooked. We ensured that all users inputs were escaped before being passed to the SQL query; however, at one point, the search attribute in a query was still created via a string-based construction. After adjusting this part of the code, the next Bandit run confirmed that our code basis was now issue-free.

![Bandit's Final Run with No Issues Found](https://i.imgur.com/eEOJpOl.png)

*Figure 12: Bandit's Final Run with No Issues Found.*

The last type of testing was done before submitting the final project. Functional Testing ensures that all end-to-end use cases and user scenarios that will be done via the System are included and working. First, we established a Functional Test Plan containing a full checklist of test cases for the individual roles and the System in general. We then proceeded with manually testing each of the test scenarios to ensure that the System as a whole is working as per the use-case specifications. The complete Functional Test Plan can be found below. Doing so gave certainty that all use cases the System set out to cater towards were fulfilled.

The full end-to-end Functional Test Plan can be found here: [Functional Test Plan](https://marziohr.github.io/SSD_Project/Functional%20Test%20Plan.pdf)


## Reference List

Gaynor, A. (2020) Fernet Documentation. Available from: https://cryptography.io/en/latest/fernet/ [Accessed 17 April 2021].

Government of the Netherlands (N.D.) Fighting Cybercrime in the Netherlands. Government of the Netherlands. Available from: https://www.government.nl/topics/cybercrime/fighting-cybercrime-in-the-netherlands [Accessed 17 April 2021].

Nakov, S. (2018) Practical Cryptography for Developers. Available from: https://cryptobook.nakov.com/mac-and-key-derivation/argon2 [Accessed 17 April 2021].

OWASP (2020) OWASP Top Ten. Available from: https://owasp.org/www-project-top-ten/ [Accessed 10 April 2020].