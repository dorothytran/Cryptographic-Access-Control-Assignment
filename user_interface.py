# Dorothy Tran 101141902
import os, re, sys, getpass
sys.path.append('./user_account')
import user_registration, access_control, access_enum

# TO DO LIST
# - Verify login functionality
# - Loop the user interface to login when a user registers into the system
# - Do the last access control policy coding... 

# Hard-coded values
valid_commands = ['R','TE','FA','C','P','I','FP','TS']
path = os.path.join("files", "passwd.txt")

""" Interactive user interface to enroll a user while doing proactive password checking """
def enrollment_ui():
    while True:
        new_username = input("Create a username: ").lower()  # Prompt user to enter a username first to check
        if re.match("^[A-Za-z0-9_-]*$", new_username):
            existing_user = user_registration.existing_user_check(new_username)
            
            if not existing_user:
                new_password = input("Create a password: ")
                role = set_role_enrollment()
                result, message = user_registration.enroll_user(new_username, new_password, role)
                
                if result: # Password complies with password policy
                    print(message)
                    access_control.set_role_permission(role)
                    print(f"Your role has been set to {role.value}")
                    break
                else:
                    print(message)
                    print("Please re-enter credentials:")
            else:
                print(f"{new_username} already exists in the system. Please try again.")
        else:
            print("Invalid username. Please try again with only letters, numbers, and underscores.")

""" Helper function for users to input a command of role selection"""
def role_establishment_commands():
    print("------------------------------------------------")
    print("Select a User Role:")
    print("R  : Regular Client")
    print("TE : Teller")
    print("FA : Financial Advistor")
    print("C  : Compliance Officer")
    print("P  : Premium Client")
    print("I  : Investment Analyst")
    print("FP : Financial Planner")
    print("TS : Technical Support")
    print()

""" Helper function to enroll a user based on input commands"""
def set_role_enrollment():
    isSet = False
    while not isSet:
        role_establishment_commands()
        selected_role = input("Please select a role from the list: ").upper()
        if selected_role in valid_commands:
            role = {
                'R':    access_enum.UserRole.CLIENT,
                'TE':   access_enum.UserRole.TELLER,
                'FA':   access_enum.UserRole.FINANCIAL_ADVISOR,
                'C':    access_enum.UserRole.COMPLIANCE_OFFICER,
                'P':    access_enum.UserRole.PREMIUM_CLIENT,
                'I':    access_enum.UserRole.INVESTMENT_ANALYST,
                'FP':   access_enum.UserRole.FINANCIAL_PLANNER,
                'TS':   access_enum.UserRole.TECH_SUPPORT
            }[selected_role]
            isSet = True # Role has been selected by the user
            return role
        else:
            print("Invalid command. Please input a valid role command from the list of commands.")

""" Interactive user interface to login an existing user to the system """ 
def login():  
    input_username = input("Enter username: ").lower()
    existing_user = user_registration.existing_user_check(input_username)
    
    if existing_user:
        # getpass.getpass("Create a password: ") # Hide users password when they type
        input_password = input("Enter your password: ")
        valid = user_registration.verify_login(input_username.lower(), input_password)
        if valid:
            print("ACCESS GRANTED")
        else:
            print("Password is invaldid")
    else:
        print(f"The username {input_username} does not exist in the system. Please try again.")

""" User Interface of Finvest Holdings to manage users"""
def user_interface():
    print("------------------------------------------------")
    print("Finvest Holdings")
    print("Client Holdings and Information System")
    print("------------------------------------------------")
    print("Would you like to register a user to the system?")
    
    # Interactive commands
    register_user = str(input("Enter 'Y' or 'N': ").upper())
    if register_user == "Y":
        print("----------------")
        print("User Enrollment")
        print("----------------")
        enrollment_ui()
    elif register_user == "N":
        print("----------------")
        print("User Login")
        print("----------------")
        login()
    else:
        print("Invalid command. Please type 'Y' or 'N'")
        user_interface()

# Run
user_interface()