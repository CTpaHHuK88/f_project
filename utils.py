import hashlib
import os

def hash_password(value):
    hash_object = hashlib.sha512(value.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig

def secret_key():    
    print(os.urandom(24))

