"""Module to define the Interface Class including menu options and user inputs."""

import sys
import stdiomask
from validator_collection import checkers
import authentication as auth
import admin_operations as adops
import operations as ops
import eventlog as log


RED = '\033[91m' # Error Messages
GREEN = '\033[92m' # Success Messages
BLUE = '\033[94m' # MOTD and Menus
WHITE = '\033[97m' # User Input
YELLOW = '\033[93m' # Notices to User
BOLD = '\033[1m'


class Interface: #pylint: disable=too-many-public-methods
    """Class that provides user menus and inputs. Differentiates views depending on user role."""

    def __init__(self):
        # Initialise the interface object when main.py is run.
        self.uid = None
        self.urole = None
        self.first_name = None
        self.username = None

        self.entered_username = None
        self.failed_attempts = 0

        self.motd() # call motd to display


    def motd(self):
        '''
        Display the motd including privacy and data policies. Prompts user to accept the ToS.
        If user agrees, display login prompt. If user disagrees, terminate CLI.
        '''
        with open('config/banner.bin','r') as file:
            motd = file.readlines()
            for line in motd:
                print(BLUE + BOLD + line, end='')
        print(YELLOW+'Terms of Service: '+WHITE+
              'https://marziohr.github.io/SSD_Project/policies/Terms%20and%20Conditions.pdf')
        print(YELLOW+'Privacy Policy: '+WHITE+
              'https://marziohr.github.io/SSD_Project/policies/Privacy%20Policy.pdf\n')
        choice=self.y_n_input("Do you agree with the Terms of Service and Privacy Policy? (y/n): ")
        if choice == 'y':
            self.login()
        else:
            sys.exit()


    def login(self):
        '''
        Asks user to enter username and password. If combination is found,
        logs user in and saves the user id, role and first name.
        If combination is incorrect after third try, user will be locked from logging in again.
        '''
        inpt_username = self.username_input()
        inpt_password = stdiomask.getpass()

        login = auth.existing_user(inpt_username,inpt_password)

        if login is None: # Condition if Username was not found
            print(RED + 'The Username and Password combination you have entered is incorrect.')
            self.login()

        elif login is False: # Condition if entered password was incorrect
            if self.entered_username != inpt_username: # if username differs, reset attempts to 1
                self.entered_username = inpt_username
                self.failed_attempts = 1
                print(RED + 'The Username and Password combination you have entered is incorrect.')
                self.login()
            else: # trigger lock if login for same user is failed 3 times in succession
                if self.failed_attempts < 2:
                    self.failed_attempts += 1
                    print(RED, end='')
                    print('The Username and Password combination you have entered is incorrect.')
                    self.login()
                else:
                    adops.lock_user(adops.fetch_user_info(username=inpt_username)[0])
                    print(RED+'Your account has been locked because it reached ', end='')
                    print('a maximum amount of failed login attempts.')
                    print('Please contact the system administrator team for further assistance.\n')
                    print(WHITE)
                    sys.exit()

        else:
            log.auth_log("Successful Login", login[0]) # log successful login
            self.uid = login[0]
            self.urole = login[2]
            self.first_name = login[1]
            self.username = inpt_username

            last_login = auth.fetch_last_login(self.uid)
            if last_login is None:
                print(GREEN+f'\nAccess Granted! Welcome to the System, {self.first_name}.')
                print(YELLOW+'\nDue to you logging into the system for the first time, ', end='')
                print('please change your own password.')
                while True: # while password is not changed iterate over password change prompt
                    changed_pswd = self.change_password()
                    if changed_pswd:
                        auth.update_last_login(self.uid) # updates last_login date stamp
                        print(YELLOW+'You will now be logged out. ', end='')
                        print('Please login with your new password to use the system.')
                        self.logout()

            else:
                print(GREEN + f'\nAccess Granted! Welcome back, {self.first_name}.')
                auth.update_last_login(self.uid) # updates last_login date stamp
                self.handle_main()


    def handle_main(self):
        '''
        Handler to display main menu options based on user's role.
        1 = Administrator
        2 = Specialist
        3 = Third-Party Authority
        '''
        if self.urole == 1:
            self.admin_menu()
        elif self.urole == 2:
            self.specialist_menu()
        elif self.urole == 3:
            self.authority_menu()
        else:
            print(RED + f"Error: User Role not set correctly. Current value set to: {self.urole}")


    def admin_menu(self):
        '''
        Displays main menu options for the administrator role.
        Depending on choice, will trigger the operation from the admin_operations module.
        Choices include: Creating a new user, modifying an existing user,
        deactivating (soft deleting) an existing user, unlocking a user, logout.
        '''
        print(BLUE + '\nPlease select what you want to do:')
        print(' 1. Create New User')
        print(' 2. Modify Existing User')
        print(' 3. Deactivate User')
        print(' 4. Unlock User')
        print(' 5. Logout' + WHITE)
        choice = self.choice_input(5)
        if choice == 1:
            self.create_user()
        elif choice == 2:
            self.modify_user()
        elif choice == 3:
            self.deactivate_user()
        elif choice == 4:
            self.unlock_user()
        else:
            self.logout()


    def specialist_menu(self):
        '''
        Displays main menu options for the specialist (employee) role.
        Depending on choice, will trigger the operation from the operations module.
        Choices include: Search existing sources, create a new source, logout.
        '''
        print(BLUE + '\nPlease select what you want to do:')
        print(' 1. Search Source')
        print(' 2. Create New Source Entry')
        print(' 3. Change Password')
        print(' 4. Logout' + WHITE)
        choice = self.choice_input(4)
        if choice == 1:
            self.search_sources()
        elif choice == 2:
            self.create_source()
        elif choice == 3:
            changed_pswd = self.change_password()
            if changed_pswd:
                print(YELLOW+'\nYou will now be logged out. ', end='')
                print('Please login with your new password to use the system.')
                self.logout()
            else:
                self.handle_main()
        else:
            self.logout()


    def authority_menu(self):
        '''
        Displays main menu options for the authority (third-party) role.
        Depending on choice, will trigger the operation from the operations module.
        Choices include: Search existing sources, logout.
        '''
        print(BLUE + '\nPlease select what you want to do:')
        print(' 1. Search Source')
        print(' 2. Change Password')
        print(' 3. Logout' + WHITE)
        choice = self.choice_input(3)
        if choice == 1:
            self.search_sources()
        elif choice == 2:
            changed_pswd = self.change_password()
            if changed_pswd:
                print(YELLOW+'\nYou will now be logged out. ', end='')
                print('Please login with your new password to use the system.')
                self.logout()
            else:
                self.handle_main()
        else:
            self.logout()


    def create_user(self):
        '''
        Prompts information and inputs for new user creation. If entered details pass validation,
        calls admin_operations module to execute the creation on the database level.

        Validation rules:
        First Name: >2 characters and may only contain letters, spaces and '-'
        Last Name: >2 characters and may only contain letters, spaces and '-'
        Date of Birth: Exactly 10 characters and may only contain numbers and '-'
        Email: Must contain exactly 1x '@' and atleast 1x '.' and end with a letter.
        May contain alphanum and '-', '.', '_', '+'

        If user is registered successfully, the user password will be autogenerated
        and sent to the user's email address.
        '''
        print(BLUE + '\nCreate a New User')
        print('---------------------------' + WHITE)
        inpt_first = self.name_input("First")
        inpt_last = self.name_input("Last")
        inpt_email = self.email_input(register=True)
        inpt_dob = self.dob_input()
        print(BLUE + '\nPlease select the user role:')
        print(' 1. Administrator')
        print(' 2. Specialist')
        print(' 3. External Authority' + WHITE)
        inpt_role = self.choice_input(3)

        result=adops.register_new_user(inpt_first,inpt_last,inpt_dob,inpt_email,inpt_role,self.uid)
        if result:
            print(GREEN + "User has successfully been created!")
        else:
            print(RED + "Error: User has not been created successfully. Please try again.")

        choice = self.y_n_input(WHITE + "\nDo you want to create another user? (y/n): ")
        if choice == 'y':
            self.create_user()
        else:
            self.admin_menu()


    def modify_user(self): #pylint: disable=too-many-branches
        '''
        Function to prompt user modification options.
        Admin can change user's first name, last name, dob and user role.
        '''
        print(BLUE + '\nModify an existing User')
        print('---------------------------' + WHITE)
        inpt_email = self.email_input()
        result = adops.fetch_user_info(email=inpt_email)
        if result is not None:
            print(BLUE + '\nUser Found:')
            print(f'ID: {result[0]}\t|\tFirst Name: {result[1]}\t|\t', end='')
            print(f'Last Name: {result[2]}\t|\tEmail: {result[3]}\t|\tDate of Birth: ', end='')
            print(f'{result[4]}\t|\tCurrent Status: {result[5]}\n')
            print('What would you like to change?')
            print(' 1.) First Name')
            print(' 2.) Last Name')
            print(' 3.) Date of Birth')
            print(' 4.) Cancel' + WHITE)
            edit_option = self.choice_input(4)
            if edit_option==1:
                inpt_first = self.name_input("new First")
                changed = adops.modify_user(result[0], 'first_name', inpt_first, self.uid)
                if changed:
                    print(GREEN + "User has successfully been modified!")
                else:
                    print(RED + "Error: User has not been modified successfully. Please try again.")
            elif edit_option==2:
                inpt_last = self.name_input("new Last")
                changed = adops.modify_user(result[0], 'last_name', inpt_last, self.uid)
                if changed:
                    print(GREEN + "User has successfully been modified!")
                else:
                    print(RED + "Error: User has not been modified successfully. Please try again.")
            elif edit_option==3:
                inpt_dob = self.dob_input()
                changed = adops.modify_user(result[0], 'dob', inpt_dob, self.uid)
                if changed:
                    print(GREEN + "User has successfully been modified!")
                else:
                    print(RED + "Error: User has not been modified successfully. Please try again.")
        else:
            print(RED + 'No User found for the email address.')
        choice = self.y_n_input(WHITE + "\nDo you want to modify another user? (y/n): ")
        if choice == 'y':
            self.modify_user()
        else:
            self.handle_main()


    def deactivate_user(self):
        '''
        Prompts dialogue for deactivating an existing user.
        If successful, the user in question will have his status changed to 'deactivated'.
        '''
        print(BLUE + '\nDeactivate an Existing User')
        print('---------------------------' + WHITE)
        deact_email = self.email_input()
        result = adops.fetch_user_info(email=deact_email)
        if result is not None:
            if result[5] != 2:
                print(BLUE + 'User Found:')
                print(f'ID: {result[0]}\t|\tFirst Name: {result[1]}\t|\tLast Name: ', end='')
                print(f'{result[2]}\t|\tEmail: {result[3]}\t|\tCurrent Status: {result[5]}\n'+WHITE)
                choice = self.y_n_input("Are you sure you want to deactivate this user? (y/n): ")
                if choice == 'y':
                    deactivated = adops.deactivate_user(result[0], self.uid, result[5])
                    if deactivated:
                        print(GREEN + "User has successfully been deactivated.")
                    else:
                        print(RED + 'Error: User could not be deactivated. Please try again.')
            else:
                print(RED + 'Error: User is already deactivated.')
        else:
            print(RED + 'No User found for the email address.')
        choice = self.y_n_input(WHITE + "\nDo you want to deactivate another user? (y/n): ")
        if choice == 'y':
            self.deactivate_user()
        else:
            self.admin_menu()


    def unlock_user(self):
        '''
        Prompts dialogue for unlocking a locked-out user.
        If successful, the user in question will have his status changed back to 'active'
        '''
        print(BLUE + '\nUnlock an Existing User')
        print('---------------------------'+ WHITE)
        unlock_email = self.email_input()
        result = adops.fetch_user_info(email=unlock_email)
        if result is not None:
            if result[5] == 3:
                print(BLUE + 'User Found:')
                print(f'ID: {result[0]}\t|\tFirst Name: {result[1]}\t|\tLast Name: ', end='')
                print(f'{result[2]}\t|\tEmail: {result[3]}\t|\tCurrent Status: {result[5]}\n'+WHITE)
                choice = self.y_n_input("Are you sure you want to unlock this user? (y/n): ")
                if choice == 'y':
                    unlocked = adops.unlock_user(result[0], self.uid)
                    if unlocked:
                        print(GREEN, end='')
                        print("User has successfully been unlocked! The User can now login again.")
                    else:
                        print(RED + 'Error: User could not be unlocked. Please try again.')
            else:
                print(RED + 'Error: User is currently not locked.')
        else:
            print(RED + 'No User found for the email address.')
        choice = self.y_n_input(WHITE + "\nDo you want to unlock another user? (y/n): ")
        if choice == 'y':
            self.unlock_user()
        else:
            self.admin_menu()


    def search_sources(self): #pylint: disable=too-many-branches,too-many-statements
        '''
        Displays options for Source Search. Once a Source has been selected, will display the
        main information regarding the source, as well as provide the option to modify it.
        '''
        print(BLUE + '\nSearch Source')
        print('---------------------------')
        print('\nPlease select the field you want to search:')
        print(' 1. Name')
        print(' 2. Url')
        print(' 3. Description')
        print(' 4. Threat Level' + WHITE)
        input_field = self.choice_input(4)
        if input_field == 4:
            search_term = self.choice_input(5)
        else:
            search_term = self.search_string_input("Please enter text to search")
        field_name = self.map_input_field(input_field)
        result = ops.search_for_source(field_name, search_term)

        if len(result) == 0:
            print(RED + "No sources found")
            self.search_sources()

        print(BLUE + "\nId\tName")
        print("--\t--------------")
        for item in result:
            print((str(item[0]) + "\t" +item[1]))

        print(WHITE + '\nPlease enter the Source Id to view details:')
        selected_id = self.source_id_input()
        # Check if entered Source Id is valid
        is_valid_id = False
        for item in result:
            if item[0] == selected_id:
                log.operation_log("View Source", self.uid, selected_id) # log view source event
                is_valid_id = True
        if not is_valid_id:
            print(RED + "Invalid source Id")
            self.search_sources()
        source_details = ops.get_source_by_id(selected_id)

        if source_details is None:
            print (RED + "Error occured")
            self.search_sources()

        print (BLUE + "\nId : " + str(source_details[0]))
        print ("Name : " + source_details[1])
        print ("Url : " + source_details[2])
        print ("\nDescription : \n" + source_details[4])
        print ("\nThreat Level : " + str(source_details[3]))
        print ("Created Date : " + source_details[5].strftime("%m/%b/%Y"))
        print ("Modified Date : " + source_details[6].strftime("%m/%b/%Y"))

        print(YELLOW + '\nPlease select what you want to do:')

        if self.urole == 3:
            print(' 1. Search new source')
            print(' 2. Main menu' + WHITE)
        else:
            print(' 1. Edit')
            print(' 2. Search new source')
            print(' 3. Main menu' + WHITE)

        choice = self.choice_input(3)

        if self.urole == 3:
            if choice == 1:
                self.search_sources()
            elif choice == 2:
                self.specialist_menu()
        else:
            if choice == 1:
                print(BLUE + '\nPlease select the field you want to edit:')
                print(' 1. Name')
                print(' 2. Url')
                print(' 3. Description')
                print(' 4. Threat Level' + WHITE)
                input_edit_field = self.choice_input(4)

                if input_edit_field == 2:
                    new_value = self.source_create_url_input("Please enter new url")
                elif input_edit_field == 4:
                    new_value = self.choice_input(5)
                else:
                    new_value = self.search_string_input(WHITE + "Please enter new value")

                edit_field_name = self.map_input_field(input_edit_field)
                ops.modify_source(int(selected_id), edit_field_name, new_value, self.uid)
                print(GREEN + '\nSource has been modified successfully')
                self.specialist_menu()

            elif choice == 2:
                self.search_sources()
            elif choice == 3:
                self.specialist_menu()


    def create_source(self):
        '''
        Displays options to enter a new source into the system.
        If validations are met, will action the creation using the operations module.
        '''
        print(BLUE + '\nCreate a New Source')
        print('---------------------------' + WHITE)
        inpt_name = self.source_create_string_input("Please enter the Source Name")
        inpt_url = self.source_create_url_input("Please enter the Source Url")
        inpt_description = self.source_create_string_input("Please enter the Source Description")

        print(YELLOW + '\nPlease enter the threat level:')
        print(' 0 : Min - 5 : Max' + WHITE)
        inpt_threat_level = self.choice_input(5)

        result=ops.create_new_source(inpt_name,inpt_url,inpt_threat_level,inpt_description,self.uid)
        if result:
            print(GREEN + "Source has successfully been created!")
        else:
            print(RED + "Error: Source has not been created successfully. Please try again.")

        choice = self.y_n_input(WHITE + "\nDo you want to create another Source? (y/n): ")
        if choice == 'y':
            self.create_source()
        else:
            self.specialist_menu()


    def change_password(self) -> bool:
        '''
        Function and prompt to change password. User will need to enter his existing password.
        User will then have to enter the new password and confirm it.
        If all correct, password will be updated on the database.
        Returns True if successful and False if not.
        '''
        inpt_password = stdiomask.getpass(WHITE+'Please enter your current Password: ')
        login = auth.existing_user(self.username,inpt_password)

        if login is None or login is False: # Condition if Password was not found or is incorrect
            print(RED + 'The Password you have entered is incorrect. Please check and try again.')
            return False

        print(YELLOW+'\nPlease Note: Your password must be at least 12 characters ',end='')
        print('long, include letters and numbers, as well as atleast one special character.')
        new_password = stdiomask.getpass(WHITE + '\nPlease enter your new Password: ')
        confirm_password = stdiomask.getpass('Please confirm your new Password: ')
        valid_pswd = self.password_validator(new_password)

        if valid_pswd:
            if new_password == inpt_password:
                print(RED+'\nError: Your new password may not be the same as your old one.')
                return False
            if new_password == confirm_password:
                changed = ops.change_password(self.uid, auth.hash_pswd(new_password))
                if changed:
                    print(GREEN + '\nYour password has been successfully updated.')
                    return True
                print(RED + '\nError: Your password could not be updated.', end='')
                print('Please check with the Administrator Team for further instructions.')
                return False
            print(RED + '\nError: Your entered passwords do not match. Please try again.')
            return False
        print(RED)
        print("Error: Your password does not confirm with the system's password standards.")
        return False


    def logout(self):
        '''Message to be displayed when logout is chosen.'''
        print(BLUE, end='')
        print("\nThank you for using the NCSC Suspect Sources System. ", end='')
        print(f"See you soon, {self.first_name}!\n" + WHITE)
        sys.exit()


    def choice_input(self, num_choices:int) -> int:
        '''
        Wrapper to validate the user input for a menu selection.
        The amount of different options to choose from can be set with the argument "num_choices".
        Returns the chosen option as an Integer.
        '''
        user_input = input(WHITE + "\nSelect option: ")
        try:
            int_input = int(user_input)
        except ValueError:
            print(RED + "Error: Invalid selection. Please check your input and try again.")
            return self.choice_input(num_choices)
        if 0 < int_input <= num_choices:
            return int_input
        print(RED + "Error: Invalid selection. Please check your input and try again.")
        return self.choice_input(num_choices)


    def username_input(self) -> str:
        '''
        Wrapper to validate and sanitise the user input for username.
        Ensures entered string is following the validation rules. If so, returns the entered string.
        '''
        valid_char = ('.','_','-')
        min_len = 5

        input_user = input(WHITE + "\nPlease enter your Username: ")

        if len(input_user) < min_len: # checks the length of the entered username
            print(RED + "Error: Entered username is invalid. Please check and try again.")
            return self.username_input()
        for char in input_user: # checks each character of user input
            if char.isalnum():
                continue # continue if current char is either alpha or numerical
            if char in valid_char:
                continue # continue if current char is part of the valid characters tuple
            print(RED + "Error: Entered username is invalid. Please check and try again.")
            return self.username_input()
        return input_user # returns entered string if all validation rules are met


    def name_input(self, name_type:str) -> str:
        '''
        Wrapper to validate and sanitise the user input for first and lastname.
        Ensures entered string is following the validation rules. If so, returns the entered string.
        Validation: >2 characters and may only contain letters, spaces and '-'
        The argument "name_type" defines whether the entered name is a first or last name.
        "first" = first name
        "last" = last name
        '''
        valid_char = (' ','-')
        min_len = 3

        input_name = input(WHITE + f"\nPlease enter the User's {name_type} Name: ")

        if len(input_name) < min_len: # checks the length of the entered name
            print(RED + "Error: Entered Name is invalid. Please check and try again.")
            return self.name_input(name_type)
        for char in input_name: # checks each character of name input
            if char.isalpha():
                continue # continue if current char is a letter
            if char in valid_char:
                continue # continue if current char is part of the valid characters tuple
            print(RED + "Error: Entered Name is invalid. Please check and try again.")
            return self.name_input(name_type)
        return input_name # returns entered string if all validation rules are met


    def email_input(self, register=False) -> str:
        '''
        Wrapper to validate and sanitise the user input for email.
        Ensures entered string is following the validation rules. If so, returns the entered string.
        Validation: Must contain exactly 1x '@', atleast 1x '.' and end with a letter.
        May contain alnum and '-', '.', '_', '+'
        '''
        valid_char = ('-', '.', '_', '+')
        min_len = 7
        num_at_sign = 0
        contains_dot = False
        ends_with_letter = False

        input_email = input(WHITE + "\nPlease enter the User's Email Address: ")

        if register:
            email_exists = adops.fetch_user_info(email=input_email)
            if email_exists:
                print(RED + "Error: Entered Email Address is already tied to a User in the system.")
                return self.email_input()

        if len(input_email) < min_len:
            print(RED + "Error: Entered Email Address is invalid. Please check and try again.")
            return self.email_input()

        if input_email[-1].isalpha(): # checks if email ends with a letter
            ends_with_letter = True

        if '.' in input_email: # checks if email contains atleast one '.'
            contains_dot = True

        for char in input_email: # checks each character of name input
            if char.isalnum():
                continue # continue if character is a letter or number
            if char in valid_char:
                continue # continue if character is part of the valid_char tuple
            if char == '@':
                num_at_sign += 1 # counts the number of times the '@' sign appears
                continue
            print(RED + "Error: Entered Email Address is invalid. Please check and try again.")
            return self.email_input()

        if num_at_sign == 1 and contains_dot and ends_with_letter:
            return input_email # if all validations are met, the input string is returned
        print(RED + "Error: Entered Email Address is invalid. Please check and try again.")
        return self.email_input()


    def dob_input(self) -> str:
        '''
        Wrapper to validate and sanitise the user input date of birth.
        Ensures that string is following validation rules. If so, returns the entered string.
        Validation: Exactly 10 characters and may only contain numbers and '-'
        '''
        valid_char = ('-')
        exact_len = 10

        input_dob = input(WHITE + "\nPlease enter the User's Date of Birth (Format YYYY-MM-DD): ")

        if len(input_dob) != exact_len:
            print(RED + "Error: Entered Date of Birth is invalid. Please check and try again.")
            return self.dob_input()
        for char in input_dob:
            if char.isnumeric():
                continue
            if char in valid_char:
                continue
            print(RED + "Error: Entered Date of Birth is invalid. Please check and try again.")
            return self.dob_input()
        return input_dob


    def password_validator(self, password:str) -> bool: #pylint: disable=no-self-use
        '''
        Checks if a given password is conform to the system's standards.
        A password must be atleast 12 characters long, include letters and numbers,
        and atleast one special character. Returns True if conform and False if not.
        '''
        min_len = 12
        includes_letter = False
        includes_number = False
        includes_special = False

        valid_special_char = '[@_!#$%^&*()<>?/\}{~:;]-.,' #pylint: disable=anomalous-backslash-in-string

        if len(password) < min_len:
            return False
        for char in password:
            if char.isalpha():
                includes_letter = True
            elif char.isnumeric():
                includes_number = True
            elif char in valid_special_char:
                includes_special = True
        if includes_special and includes_number and includes_letter:
            return True
        return False


    def y_n_input(self, question:str) -> str:
        '''Validates a yes/no question and returns the str if answer is either 'y' or 'n'.'''
        input_choice = input(WHITE + question).lower()
        if input_choice in ('y', 'n'):
            return input_choice
        print(RED+"Error: Please answer either 'y' for 'yes' or 'n' for 'no'.")
        return self.y_n_input(question)


    def source_create_url_input(self, messege) -> str:
        '''Validates url input for source creation.'''
        input_text = input(WHITE+f"\n{messege}: ")
        if checkers.is_url(input_text) is False:
            print(RED + "Error: Entered data is invalid. Please check and try again.")
            return self.source_create_url_input(messege)
        return input_text # returns entered string if all validation rules are met


    def source_create_string_input(self, messege) -> str:
        '''Validates string user input for source creation.'''
        min_len = 5
        input_text = input(WHITE+f"\n{messege}: ")
        if len(input_text) < min_len: # checks the length of the entered text
            print(RED + "Error: Entered data is invalid. Please check and try again.")
            return self.source_create_string_input(messege)
        return input_text # returns entered string if all validation rules are met


    def search_string_input(self, messege) -> str:
        '''Validates string user input search term.'''
        min_len = 3
        input_text = input(WHITE + f"\n{messege}: ")
        if len(input_text) < min_len: # checks the length of the entered text
            print(RED + "Error: Search term should be more than or equal to three characters.")
            return self.search_string_input(messege)
        return input_text # returns entered string if all validation rules are met


    def source_id_input(self) -> int:
        '''Validates User Input for Source Id.'''
        user_input = input(WHITE + "\nSelect Id: ")
        try:
            int_input = int(user_input)
        except ValueError:
            print(RED + "Error: Invalid id. Please check your input and try again.")
            return self.source_id_input()
        return int_input


    def map_input_field(self, input_field:int) -> str: #pylint: disable=no-self-use
        '''Map user input integer value to database field.'''
        if input_field == 1:
            return "name"
        if input_field == 2:
            return "url"
        if input_field == 3:
            return "description"
        return "threat_level"
