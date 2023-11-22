# Dorothy Tran 101141902
import sys, user_account
sys.path.append('./user_registration')
sys.path.append('./password')

# enrolling a user
# List what role they want to enroll to
# login successful
        
def login():  
    userid = str(input("Enter username: \n"))
    path = os.path.join("files", "passwd.txt")
    validUser = user_account.existing_user_check(userid, path)
    if validUser:
        pw = str(input("Enter your password: "))
    else:
        user_interface()

def user_interface():
    print("Finvest Holdings")
    print("Client Holdings and Information System")
    print("-----------------------------------------------------")
    print("Would you like to register a user to the system?")
    register_user = str(input("Enter 'Y' or 'N': ").upper())
    if register_user == "Y":
        new_userid = str(input("Enter username: "))
    elif register_user == "N":
        login()
    else:
        print("Invalid command. Please type 'Y' or 'N'")
        user_interface()

user_interface()