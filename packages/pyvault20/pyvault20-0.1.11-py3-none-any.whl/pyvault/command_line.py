import requests
import pychacha
import yaml
import sys
import time

def CONFIG(**kwargs):

    if kwargs:
        config=CONFIG()
        config.update(kwargs)
        with open(".config.txt", "w+") as f:
            f.write(yaml.dump(config))
            f.truncate()
        return True

    else:
        with open(".config.txt", "r+") as f:
            CONFIG = yaml.load(f.read())
        return CONFIG

def encrypt():

    config=CONFIG()
    c = pychacha.ChaCha(config['key'])

    CONFIG(status="partial")
    for folder in CONFIG['folders']:
        c.encrypt_folder(folder)
    CONFIG(status="cypher")
    CONFIG(key="")
    return True

def decrypt(key):

    config=CONFIG()
    c = pychacha.ChaCha(key)
    folders=config['folders']
    folders.reverse()

    CONFIG(status="partial")
    for folder in folders:
        c.decrypt_folder(folder)
    CONFIG(status="plain")
    return True


#called by command line
def main():
    
    #create config files
    if sys.argv[1]=="init":

        default_config={
            "interval": 600,
            "key": "change_me",
            "remote": "https://example.com/trigger.html",
            "folders": ["."],
            "status": "plain"
        }

        with open(".config.txt", "w+") as f:

            f.write(yaml.dump(default_config))

        print("Default config saved to .config.txt")
        print("Customize the config before continuing!")

    elif sys.argv[1]=="begin":

        config=CONFIG()

        while True:

            try:
                r = requests.get(CONFIG['remote'])
                r.raise_for_status()

            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):

                encrypt()

            try:
                instructions=yaml.load(r.content)
            except:
                pass


            if instructions['directive']=="encrypt" and config['status']=="plain":
                encrypt()

            elif instructions['directive']=="decrypt" and config['status']=="cypher":
                decrypt(key=instructions['key'])

            time.sleep(CONFIG['interval'])

    elif sys.argv[1]==decrypt:
        if config['status']!="cypher":
            raise ValueError("Cannot decrypt while not encrypted")

        decrypt(key=sys.argv[2])