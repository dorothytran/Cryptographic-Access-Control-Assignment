# Dorothy Tran 101141902
import sys
sys.path.append('./user_account')

""" Input to register a user to Finvest Holdings system """
def user_registration():
    print("Would you like to register a user to the system?")
    register = str(input("Enter Yes or No: "))
    if(register == "Yes"):
        new_userid = str(input("Enter username: \n"))
        
def login():
    print("Finvest Holdings")
    print("Client Holdings and Information System")
    print("----------------------------------------------------")   
    userid = str(input("Enter username: \n"))
    pw = str(input("Enter your password: "))

def main():
    login()

# Run the program
if __name__ == "__main__":
    main()