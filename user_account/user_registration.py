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
            for line in file:
                line = line.strip().lower()
                if line.startswith("username:"):
                    stored_username = line.split(":")[1].strip().lower()
                    if (username == stored_username):
                        return True  # Existing user in password file
            return False  # No existing user is found
    except FileNotFoundError:
        print(f"File {path} not found")
        return False

""" Helper method to get the last id of the password file """
def get_last_userId():
    try:
        with open(path, 'r') as file:
            last = 0
            for f in file:
                if f.startswith("userId:"):
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
def enroll_user(username: str, pw: str, user_role: str):
    try:
        cleaned_username = username.replace("/", "").replace("\\", "").strip()

        if not existing_user_check(cleaned_username.lower()):
            cleaned_pw = pw.strip()

            result, message = password.password_policy_check(cleaned_username, cleaned_pw)

            if not result:
                return False, message
            else:
                last_id_value = get_last_userId()
                new_id = last_id_value + 1
                
                salt, hash = password.hash_function(cleaned_pw)
                # Use base64 encoding for storing the hash
                encoded_hash = base64.b64encode(hash).decode('utf-8')
                # Convert salt to a hexadecimal string
                salt_hex = salt.hex()

                with open(path, "a") as f:
                    f.write(f"userId:{new_id}\n")
                    f.write(f"username:{cleaned_username}\n")
                    f.write(f"role:{user_role}\n")
                    f.write(f"hash:b'{encoded_hash}'\n")
                    f.write(f"salt:b'{salt_hex}'\n")
                    message = f"Successfully enrolled {cleaned_username} to Finvest Holdings.\n"
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