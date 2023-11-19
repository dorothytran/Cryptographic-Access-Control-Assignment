# Dorothy Tran 101141902
import os, sys, password
sys.path.append('./password_policy')
sys.path.append('./files')

""" Helper function to check if a user already exists in the password file """
def existing_user_check(userid, filepath) -> bool:
    try:
        with open(filepath, 'r') as file:
            for f in file:
                if f.startswith("userId : ") and userid == f.split(":")[1].strip():
                    return True # Existing user in password file
                return False # No existing user is found
    except FileNotFoundError:
        print(f"File {filepath} not found")
        return False

"""
2.1.1 User Enrolment: Loading a Password
Function enrolls a user and checks if their inputted password complies with the password policy.
Their userid and password is stored in a secure password file.
"""
def enroll_user(new_userid: str, pw: str, role: str):
    # Check if password complies with password policy
    result, message = password.password_policy_check(new_userid, pw)
    
    # Password does not comply with policy
    if not result:
        return False, message

    # Password file that stores the userid, password and salt
    path = os.path.join("files", "password_file.txt")
    if not existing_user_check(new_userid, path):
        salt, hash = password.hash(pw)
        with open(path, "a") as f:
            f.write(f"userId : {new_userid}\n")
            f.write(f"password : {hash}\n")
            f.write(f"salt : {salt}\n")
            message = "Sucessfully enrolled ", new_userid, " to system."
    else:
        message = "User already exists in the system. Please try again."
    return True, message

"""
Function checks if the user login credentials match with the credentials stored in the password file
- UserID is searched in the password file, take the plaintext salt and the hashcode and compare to verify
- Implement the password verification mechanism
"""
def verify_login_credentials(userid, input_password, filepath):
    message = ""
    validCredentials = False
    salt, stored_hash = password.hash(input_password)
    