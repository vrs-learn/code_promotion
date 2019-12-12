import platform

def get_key():
    if platform.system() == "Windows":
        import winreg
        REG_PATH=r"Software\BMC Software\TSOCodeMigration\Settings"
        try :
            registry_key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,REG_PATH,0,winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, "CMKey")
            winreg.CloseKey(registry_key)
            return value
        except :
            return "changeit"
    else:
        return "changeit"

def encrypt_value(user_value,user_key):
    from cryptography.fernet import Fernet
    import base64, hashlib
    password=hashlib.md5(user_key.encode()).hexdigest()
    key = base64.urlsafe_b64encode(password.encode())
    cipher_suite = Fernet(key)
    encoded_text = cipher_suite.encrypt(user_value.encode())
    return encoded_text.decode()

def decrypt_value(encr_value,user_key):
    from cryptography.fernet import Fernet
    import base64, hashlib
    password=hashlib.md5(user_key.encode()).hexdigest()
    key = base64.urlsafe_b64encode(password.encode())
    cipher_suite = Fernet(key)
    decoded_text = cipher_suite.decrypt(encr_value.encode())
    return decoded_text.decode()

## MAIN

if __name__=="__main__":
    user_key=get_key()
    user_str=input("Enter some text to encrypt :")
    encr_value=encrypt_value(user_str,user_key)
    print("\n Encrypted Value is :"+str(encr_value))
    decr_value=decrypt_value(encr_value,user_key)
    print("\n Decrypted Values is :"+str(decr_value))
