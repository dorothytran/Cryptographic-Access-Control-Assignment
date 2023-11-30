# Dorothy Tran 101141902
import os
import password, access_control

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
2.1.1 User Enrolment: Loading a Password
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

def verify_login(username, input_password):
    try:
        with open(path, 'r') as file:
            user_info = file.read().splitlines()
            for i in range(0, len(user_info), 5):  # Iterate through the data in 5 lines
                if f'username:{username}' in user_info[i:i + 5]:
                    user_found = user_info[i:i + 5]
                    break
            else:
                return False 
        stored_hash = user_found[3][5:] # Extract stored salted hash and salt
        if password.verify_hash(input_password, stored_hash):
            return True
        else:
            print("Invalid password.")
            return False
    except FileNotFoundError:
        message = "File not found."
        return False
    
def extract_pw_file_info():
    user_info_list = []
    with open(path, 'r') as file:
        userData = file.readlines()
        for data in userData:
            user_info = {}
            for key, value in (pair.split(':') for pair in data.strip().split('\n')):
                user_info[key.strip()] = value.strip()
            user_info_list.append(user_info)
    return user_info_list

def get_client_information(username):
    try:
        with open(path, 'r') as file:
            user_data = file.read()
        
        entries = user_data.strip().split('\n\n')

        for entry in entries:
            lines = entry.strip().split('\n')
            user_info = {}

            for line in lines:
                key, value = line.split(':')
                user_info[key.strip()] = value.strip()

            # Check if the current entry corresponds to the given username
            if user_info.get('username') == username:
                print("User Id:", user_info.get('userId'))
                print("Role: ", user_info.get('role'))
                #access_control.set_role_permission(user_info.get('role'))
                return {
                    'userId': user_info.get('userId'),
                    'role': user_info.get('role')
                }
        return None

    except FileNotFoundError:
        print(f"File not found at path: {path}")
        return None