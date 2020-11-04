
import json
from os import path

def is_valid_file(file):
    with open(file, 'r') as configurationfile:
        configurations = json.load(configurationfile)
        if not isinstance(configurations, list):
            raise ValueError('file must contain list []')
        for configuration in configurations:
            if not isinstance(configuration, dict):
                raise ValueError('elements must be type of dict')
            else:
                keys = configuration.keys()
                expectedKeys = ["command", "nprocess", "startup", "output", "error", "umask", "restart", "returncodes", "starttime", "stoptime", "attempts", "stopsignal", "environment", "directory"]
                for key in keys:
                    if key not in expectedKeys:
                        raise ValueError(F'allowed keys {expectedKeys}')
                if len(keys) != len(expectedKeys):
                    raise ValueError(F'number of keys must be equal to {len(keys)}')
        return configurations

def is_key_exists(data, key, message):
    if key not in data.keys() or not data[key]:
        raise ValueError(F'Missing Required Parameter: {message}')


def is_file_exists(file):
    if not path.exists(file):
        raise ValueError('File Not Found')

