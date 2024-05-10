import requests

class KeyAuth():

    def auth(keyslink, keylength, key):
        keys = requests.get(keyslink)
        if len(key) == keylength:
            if key in keys.text:
                return True
            else:
                return False
        else:
            return False
