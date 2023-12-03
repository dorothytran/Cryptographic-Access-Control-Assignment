# Dorothy Tran
import os
import password, access_enum, access_control

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
            return False  # Not an existing user
    except FileNotFoundError:
        print(f"File {path} not found")
        return False

""" Helper method to get the last id of the password file """
def last_file_userId():
    lastUserId = 0
    try:
        with open(path, 'r') as file:
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
2.1.1 User Enrollment: Loading a Password
Function enrolls a user and checks if their inputted password complies with the password policy.
Their userid and password is stored in a secure password file.
"""
def enroll_user(username: str, pw: str, user_role: str):
    try:
        if not existing_user_check(username.lower()):
            result, message = password.password_policy_check(username, pw.strip())
            if not result:
                return False, message
            else:        
                hash_pw, salt = password.hash_function(pw.strip())
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
def verify_password(username, input_password):
    try:
        with open(path, 'r') as file:
            user_info = file.read().splitlines()
            # Iterate through 5 lines in the password file
            for i in range(0, len(user_info), 5):
                if f"username:{username}" in user_info[i:i + 5]:
                    user_found = user_info[i:i + 5]
                    break
            else:
                return False 
        stored_hash = user_found[3][5:] # Get stored hash from the password file
        if password.verify_hash(input_password, stored_hash): # Verify password hash and concatenated salt
            return True
        else:
            return False
    except FileNotFoundError:
        message = "File not found."
        return False

""" Function that parses the password file and retrieves the user id """
def get_stored_userid(input_username):
    try:
        with open(path, 'r') as file:
            lastLine = ""
            for f in file:
                if f.startswith("username:"):
                    lines = f.strip().split('\n')[0]
                    data = lines.split(':')
                    if len(data) != 2:
                        return None
                    stored_username = data[1]
                    if stored_username == input_username:
                        id = lastLine.split(':')
                        if len(id) != 2:
                            return None
                        print("UserId:", id[1])
                        return id[1]
                lastLine = f
            return None # If the username is not found
    except FileNotFoundError:
        print(f"File {path} not found")
        return False

""" Switch case function to get the UserRole enum"""
def get_role(role_str):
    if role_str == "UserRole.REGULAR_CLIENT":
        return access_enum.UserRole.REGULAR_CLIENT
    elif role_str == "UserRole.PREMIUM_CLIENT":
        return access_enum.UserRole.PREMIUM_CLIENT
    elif role_str == "UserRole.FINANCIAL_PLANNER":
        return access_enum.UserRole.FINANCIAL_PLANNER
    elif role_str == "UserRole.FINANCIAL_ADVISOR":
        return access_enum.UserRole.FINANCIAL_ADVISOR
    elif role_str == "UserRole.INVESTMENT_ANALYST":
        return access_enum.UserRole.INVESTMENT_ANALYST
    elif role_str == "UserRole.TECH_SUPPORT":
        return access_enum.UserRole.TECH_SUPPORT
    elif role_str == "UserRole.TELLER":
        return access_enum.UserRole.TELLER
    elif role_str == "UserRole.COMPLIANCE_OFFICER":
        return access_enum.UserRole.COMPLIANCE_OFFICER
    else:
        return None

""" Function that parses the password file and retrieves the user role """
def get_stored_user_role(input_username):
    try:
        with open(path, 'r') as file:
            userData = file.read().split("userId:")
            for data in userData:
                trimmedData = data.strip() # trim the whitespaces
                if trimmedData:
                    extracted_user_info = {}
                    fileLines = trimmedData.split("\n") # split the lines in the password file
                    for f in fileLines:
                        if ':' in f:
                            key, value = f.split(":",1)
                            extracted_user_info[key.strip()] = value.strip() # trim the whitespaces
                    if ("username" in extracted_user_info) and (extracted_user_info['username'] == input_username):
                        # Print out the role permissions for the user's role
                        return access_control.print_role_permission(get_role(extracted_user_info.get('role', None)))
        return None # user was not found
    except FileNotFoundError:
        return None
        
# Tests
# test_username = "VeronicaSaro"
# test_password = "TestPass1!"
# role = access_enum.UserRole.INVESTMENT_ANALYST
# enrolled, message = enroll_user(test_username, test_password, role)
# print(message)
