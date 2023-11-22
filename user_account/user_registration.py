# Dorothy Tran 101141902
import os, sys, password

""" Helper function to check if a user already exists in the password file """
def existing_user_check(userid, path) -> bool:
    path = os.path.join("files", "passwd.txt")
    try:
        with open(path, 'r') as file:
            for f in file:
                if f.startswith("userId : ") and userid == f.split(":")[1].strip():
                    return True # Existing user in password file
            return False # No existing user is found
    except FileNotFoundError:
        print(f"File {path} not found")
        return False

"""
Problem 4c
2.1.1 User Enrolment: Loading a Password
Function enrolls a user and checks if their inputted password complies with the password policy.
Their userid and password is stored in a secure password file.
"""
def enroll_user(new_userid: str, pw: str, role: str):
    # Check if password complies with password policy
    result, message = password.password_policy_check(new_userid, pw)
    # Password file that stores the userid, password and salt
    path = os.path.join("files", "passwd.txt")
    
    # Password does not comply with policy
    if not result:
        return False, message
    try: 
        if not existing_user_check(new_userid, path):
            salt, hash = password.hash(pw)
            with open(path, "a") as f:
                f.write(f"userId : {new_userid}\n")
                f.write(f"password : {hash}\n")
                f.write(f"salt : {salt}\n")
                message = "Sucessfully enrolled ", new_userid, " to system."
        else:
            message = "User already exists in the system. Please try again."
    except FileNotFoundError:
        message = "File not found."
        return False, message
    return True, message

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