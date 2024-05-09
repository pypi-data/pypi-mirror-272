import requests
import pychacha
import yaml
import sys
#called by command line

def main():
    
    #create config files
    if sys.argv[1]=="init":

        default_config={
            "key": "change_me",
            "remote": "https://example.com/trigger.html",
            "folders": ["."]
        }
        
        with open(".config.txt", "w+") as f:

            f.write(yaml.dump(default_config))

        print("Default config saved to .config.txt")
        print("Customize the config before continuing!")

    elif sys.argv[1]=="begin":

        #Main periodic loop goes here
        #while true, check remote address. If triggered, encrypt



