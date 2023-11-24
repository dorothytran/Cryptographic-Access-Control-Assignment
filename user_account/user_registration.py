# Dorothy Tran 101141902
import os, sys
sys.path.append('./user_account')
import password, user_interface

# Password file that stores the userid, password and salt
path = os.path.join("files", "passwd.txt")

""" Helper function to check if a user already exists in the password file """
def existing_user_check(username):
    try:
        with open(path, 'r') as file:
            for f in file:
                if f.startswith("username : ") and username == f.split(":")[1].strip().lower():
                    return True # Existing user in password file
            return False # No existing user is found
    except FileNotFoundError:
        print(f"File {path} not found")
        return False

""" Helper method to get the last id of the password file """
def get_last_userId() -> int:
    try:
        with open(path, 'r') as file:
            last = 0
            for f in file:
                if f.startswith("userId : "):
                    intValue = int(f.split(":")[1].strip())
                    last = max(last, intValue)
            return last
    except FileNotFoundError:
        print(f"File {path} not found")
        return 0

"""
Problem 4c
2.1.1 User Enrolment: Loading a Password
Function enrolls a user and checks if their inputted password complies with the password policy.
Their userid and password is stored in a secure password file.
"""
def enroll_user(username: str, pw: str):
    user_role = user_interface.role_establishment_commands()
    try: 
        if not existing_user_check(username.lower()):
            # Check if password complies with password policy
            result, message = password.password_policy_check(username, pw)
            
            # If the password does not comply with policy
            if not result:
                return False, message
            else:
                last_id_value = get_last_userId()
                new_id = last_id_value + 1
                salt, hash = password.hash_function(pw)
                with open(path, "a") as f:
                    f.write(f"userId : {new_id}\n")
                    f.write(f"username: {username}")
                    f.write(f"role : {user_role}\n") 
                    f.write(f"password : {hash}\n")
                    f.write(f"salt : {salt}\n")
                    message = f"Sucessfully enrolled {username} to Finvest Holdings."
        else:
            message = "User already exists in the system. Please try again."
    except FileNotFoundError:
        message = "File not found."
        return False, message
    return True, message, user_role

"""
Problem 4b
Function checks if the user login credentials match with the credentials stored in the password file
- UserID is searched in the password file, take the plaintext salt and the hashcode and compare to verify
- Implement the password verification mechanism
"""
def verify_login(userid, input_password):
    message = ""
    validCredentials = False
    path = os.path.join("files", "passwd.txt")

    if not existing_user_check(userid, path):
        message = "User does not exist in the system. Please try again."
        return False, message # Invalid userid or doesn't exist
    try:
        with open(path, 'r') as file:
            for f in file:
                key, value = map(str.strip, f.split(':'))
                if key == 'userId' and value == userid:
                    stored_salt = file.readline().strip().split(': ')[1]
                    stored_hash = file.readline().strip().split(': ')[1]
                    validCredentials = password.verify_hash(input_password, stored_salt.encode(), stored_hash.encode())
                    message = ""
                    break
            if validCredentials:
                message = "Login was successful."
            else:
                message = "Password was incorrect. Please try again."
        return validCredentials, message
    except FileNotFoundError:
        message = "File not found."
        return False, message