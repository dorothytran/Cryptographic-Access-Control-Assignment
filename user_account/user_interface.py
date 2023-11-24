# Dorothy Tran 101141902
import os, re, sys, getpass
sys.path.append('./user_account')
import user_registration

# TO DO LIST:
# List what role they want to enroll to
# Login implementation

path = os.path.join("files", "passwd.txt")

""" Interactive user interface to enroll a user while doing proactive password checking """
def enrollment_ui():
    while True:
        new_userid = input("Enter username: ")  # Prompt user to enter a username first to check
        if re.match("^[A-Za-z0-9_-]*$", new_userid):
            if not user_registration.existing_user_check(new_userid.lower()):
                #new_password = getpass.getpass("Enter password: ") # Hide users password when they type
                new_password = input("Enter password: ")
                result, message, role = user_registration.enroll_user(new_userid, new_password)
                if result: # Password complies with password policy
                    print(message)
                    role_establishment_commands()
                    break
                else:
                    print(message)
                    print("Please re-enter credentials.")
            else:
                print(f"{new_userid} already exists in the system. Please try again.")
        else:
            print("Invalid username. Please try again with only letters, numbers, and underscores.")

""" Helper function for users to input a command of role selection"""
def role_establishment_commands():
    print("------------------------------------------------")
    print("Select a User Role")
    print ("R  : Regular Client")
    print ("TE : Teller")
    print ("FA : Financial Advistor")
    print ("C  : Compliance Officer")
    print ("P  : Premium Client")
    print ("I  : Investment Analyst")
    print ("FP : Financial Planner")
    print ("TS : Technical Support")
    print()
    role_selection = input("Select a Role: ").upper()
    return role_selection

valid_commands = ['R','TE','FA','C','P','I','FP','TS']

"""def set_role_enrollment(selected_role: int):
    roleSet = False
    while selected_role != valid_commands[7]:
        if selected_role == valid_commands[0]:"""


""" Interactive user interface to login an existing user to the system """ 
def login():  
    userid = str(input("Enter username: \n"))
    validUser = user_registration.existing_user_check(userid, path)
    if validUser:
        pw = str(input("Enter your password: "))
    else:
        user_interface()

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
        login()
    else:
        print("Invalid command. Please type 'Y' or 'N'")
        user_interface()

user_interface()