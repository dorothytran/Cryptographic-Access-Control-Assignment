# Dorothy Tran
import hashlib, os, re

""" Hashes a password with a generated random 32 byte salt """
def hash_function(password: str):
    password_salt = os.urandom(32)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), password_salt, 100000)    
    salted_hash = password_salt + password_hash
    salt = salted_hash[:32]
    return salted_hash, salt

""" Verifies hashed passwords """
def verify_hash(input_password: str, salted_hash: str):
    salt = bytes.fromhex(salted_hash[:64])
    generated_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), salt, 100000).hex()
    password_hash = salted_hash[64:]
    if generated_hash == password_hash:
        return True
    else: 
        return False
        
""" Helper function that  checks if an input password is a weak password """
def weak_password_check(input_password):
    path = os.path.join("files", "weakpasswd.txt")
    try:
        with open(path, 'r') as file:
            for weak_pw in file:
                if weak_pw.strip().lower() in input_password.lower():
                    return True # Password is a weak
            return False # Password is not weak
    except FileNotFoundError:
        print(f"File {path} not found")
        return False
        
""" Helper function that uses Python regex to check if the password contains prohibited format patterns """        
def prohibited_format_check(password):
    prohibited_formats = [
                    r'\b(0[1-9]|[12]\d|3[01])[-/](0[1-9]|1[0-2])[-/](19\d\d|20\d\d)\b', # Calendar date format
                    r'^[A-Z]{4}\d{1,3}$', # License Plate format AAAA###
                    r'^\d{10}$', # Telephone format ##########
                    r'^\d{3}-\d{3}-\d{4}$', # Telephone format ###-###-####
                    r'^\d+$'] # Common numbers 123456789
    for prohibited_pattern in prohibited_formats:
        if re.search(prohibited_pattern, password):
            return True  
    return False 
        
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
        message += "Passwords must have at least one special character from: *, !, @, #, $, %, ?. \n"
    
    # Passwords found on a list of common weak passwords must be prohibited
    if weak_password_check(password):
         validPassword = False
         message += "Password is weak. Please use a strong password\n"
        
    # Matching the format of calendar dates, license plate, telephone numbers or common numbers must be prohibited
    containsProhibitedFormat = prohibited_format_check(password)
    if containsProhibitedFormat:
        message = "Password must not contain format of calendar dates, license plate, telephone numbers or common numbers. Pick another password.\n"
        validPassword = False

    # Passwords matching the user ID must be prohibited
    if(userid in password):
        message += "Passwords must not match the user ID\n"

    if not message: # An error message was not printed out
        validPassword = True
    else: 
        message += "Please try again."
        validPassword = False    
    return validPassword, message

# Tests
# username = "testuser"
# testpassword1 = "test123"
# valid, message = password_policy_check(username, testpassword1)
# testpassword2 = "Averylongpassword1!"
# valid, message = password_policy_check(username, testpassword2)
# testpassword3 = "testuser"
# valid, message = password_policy_check(username, testpassword3)
# testpassword4 = "6130000000"
# valid, message = password_policy_check(username, testpassword4)
# print(message)
