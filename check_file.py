
from os import path
import json

def isValidFile(file):
    if not path.exists(file):
       print(file + ': file not found!')
       return
    with open(file, 'r') as configurationfile:
        try:
            configurations = json.load(configurationfile)
            if not isinstance(configurations, list):
                raise 'error'
            for configuration in configurations:
                print
        except:
            print(options.configurationfile + ': not a valid file!')
            exit(2)
        print(json.dumps(configurations, indent=4))