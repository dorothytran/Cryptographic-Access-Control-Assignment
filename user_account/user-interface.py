# Dorothy Tran 101141902
import os, sys, getpass
sys.path.append('./user_account')
import user_registration

# List what role they want to enroll to
# login successful

path = os.path.join("files", "passwd.txt")

def enrollment_ui():
    while True:
        # Prompt user to enter a username first to check
        new_userid = input("Enter username: ")
        
        if not user_registration.existing_user_check(new_userid.lower()):
            new_password = getpass.getpass("Enter password: ")
            user_registration.enroll_user(new_userid, new_password)
            break
        else:
            print(f"{new_userid} already exists in the system. Please try again.")
        
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