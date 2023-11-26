# Dorothy Tran 101141902
import hashlib, os, re

""" Hashes a password with a generated random 32 byte salt """
def hash_function(password: str):
    password_salt = os.urandom(32)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), password_salt, 100000)    
    return password_salt, password_hash

""" Verifies hashed passwords """
def verify_hash(input_password: str, salt: bytes, hash: bytes) -> bool:
        generated_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), salt, 100000)
        if(generated_hash == hash):
              print("Password is correct.")
              return True
        else:
              print("Password is incorrect!")
              return False
        
def retrieve_stored_hash_salt(username: str):
    path = os.path.join("files", "passwd.txt")
    try:
        with open(path, 'r') as file:
            for f in file:
                    f = f.strip()
                    if f.startswith("username : ") and username == f.split(":")[1].strip():
                        # Username matches input username
                        stored_password_hash = file.readline().strip()
                        stored_password_salt = file.readline().strip()

                        # Extract hashed password and salt from the lines
                        hashed_password = re.search(r'password : (.+)', stored_password_hash).group(1)
                        salt = re.search(r'salt : (.+)', stored_password_salt).group(1)

                        # Convert strings to bytes
                        hashed_password = bytes.fromhex(hashed_password)
                        salt = bytes.fromhex(salt)

                        return hashed_password, salt
            # Username not found
            return None, None
    except FileNotFoundError:
        print("Password file not found.")
        return None, None

""" 
Helper function that reads a stored file of weak common passwords and checks if an 
input password is a weak password
"""
def weak_password_check(input_password):
    path = os.path.join("files", "weakpasswd.txt")
    try:
        with open(path, 'r') as file:
            for weak_pw in file:
                if weak_pw.strip().lower() == input_password.lower():
                    return True # Password is a weak
            return False # Password is not weak
    except FileNotFoundError:
        print(f"File {path} not found")
        return False
        
""" Helper function that uses Python regex to check if the password contains prohibited format patterns """        
def prohibited_format_check(password):
    # Prohibited password formats
    prohibited_formats = [r"\b(0[1-9]|[12]\d|3[01])[-/](0[1-9]|1[0-2])[-/](19\d\d|20\d\d)\b", # Calendar date format
                        r"^[A-Z]{4}\d{1,3}$", # License Plate format
                        "^\d{10}$", # Telephone format ##########
                        r"^\d{3}-\d{3}-\d{4}$", # Telephone format ###-###-####
                        r"\b\d{4,}\b"] # Common numbers
    return all(re.search(pattern, password) for pattern in prohibited_formats)
        
""" Checks if a created password complies with the password policy """
def password_policy_check(userid: str, password: str):
    message = ""
    validPassword = True
    
    # List of valid special characters
    special_chars = {'!','@', '#', '$', '%', '?', '∗'}

    # Passwords must be least 8-12 characters in length
    if not (8 <= len(password) <= 12):
        message += "Passwords must be least 8-12 characters in length.\n"
    
    # At least one upper-case letter
    if not any(p.isupper() for p in password):
        message += "Passwords must have at least one upper-case letter.\n"
    
    # At least one lower-case letter
    if not any(p.islower() for p in password):
        message += "Passwords must have at least one lower-case letter.\n"
    
    # At least one numerical digit
    if not any(p.isdigit() for p in password):
        message += "Passwords must have at least one numerical digit.\n"
    
    # At least one special character from the set
    if not (any(p in special_chars for p in password)):
        message += "Passwords must have at least one special character from the set.\n"
    
    # Passwords found on a list of common weak passwords must be prohibited
    if weak_password_check(password):
         validPassword = False
         message += "Password is weak. Please use a more complex password\n"
        
    # Matching the format of calendar dates, license plate, telephone numbers or common numbers must be prohibited
    containsProhibitedFormat = prohibited_format_check(password)
    if containsProhibitedFormat:
        message = "Password must not contain format of calendar dates, license plate, telephone numbers or common numbers. Pick another password.\n"
        validPassword = False

    # Passwords matching the user ID must be prohibited
    if(userid in password):
        message += "Passwords must not match the user ID\n"

    if not message:
        message = "Input password is successful\n"
        validPassword = True
    else: 
        message += "Please try again."
        validPassword = False    
    return validPassword, message