# Dorothy Tran 101141902
import os, sys, base64
sys.path.append('./user_account')
import password

# Password file that stores the userid, password and salt
path = os.path.join("files", "passwd.txt")

""" Helper function to check if a user already exists in the password file """
def existing_user_check(username):
    try:
        with open(path, 'r') as file:
            for f in file:
                f = f.strip().lower()
                if f.startswith("username:"):
                    stored_username = f.split(":")[1].strip().lower()
                    if (username == stored_username):
                        return True  # Existing user
            return False  # No existing user
    except FileNotFoundError:
        print(f"File {path} not found")
        return False

""" Helper method to get the last id of the password file """
def last_file_userId():
    try:
        with open(path, 'r') as file:
            lastUserId = 0
            for f in file:
                if f.startswith("userId:"):
                    intValue = int(f.split(":")[1].strip())
                    lastUserId = max(lastUserId, intValue)
            return lastUserId
    except FileNotFoundError:
        print(f"File {path} not found")
        return 0

"""
Problem 4c
2.1.1 User Enrolment: Loading a Password
Function enrolls a user and checks if their inputted password complies with the password policy.
Their userid and password is stored in a secure password file.
"""
def enroll_user(username: str, pw: str, user_role: str):
    try:
        if not existing_user_check(username.lower()):
            cleaned_pw = pw.strip()
            result, message = password.password_policy_check(username, cleaned_pw)
            if not result:
                return False, message
            else:        
                salt, hash_pw = password.hash_function(cleaned_pw)

                # Using hexadecimal strings
                salt_hash = hash_pw.hex()
                salt_hex = salt.hex()

                # Retrieve the last userId to add to the password file
                last_id_value = last_file_userId()
                new_id = last_id_value + 1

                with open(path, "a") as f:
                    f.write(f"userId:{new_id}\n")
                    f.write(f"username:{username}\n")
                    f.write(f"role:{user_role}\n")
                    f.write(f"hash:{salt_hash}\n")
                    f.write(f"salt:{salt_hex}\n")
                    message = f"Successfully enrolled {username} to Finvest Holdings.\n"
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