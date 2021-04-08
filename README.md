# Development Team Project - Dutch National Cyber Security Centre Suspect Sources System


## Table of Contents
1. [Introduction](#introduction)
2. [Background](#background)
3. [Proposed System](#proposed_system)
4. [Simple User Interface](#simple_user_interface)
5. [Prerequisites](#prerequisites)


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

