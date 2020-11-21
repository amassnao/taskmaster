
import json
from os import path
from jsonschema import Draft7Validator, ValidationError
import sys
import pkgutil

fileSchema = {
    'type': 'object',
    'additionalProperties': {
        'type': 'object',
        'properties' : {
            'cmd': {'type': 'string'},
            'workingdir': {'type': 'dir'},
            'autostart' : {'type': 'boolean'},
            'autorestart': {'type': 'boolean'},
            'exitcodes': {
                'type': 'array',
                'items': {'type': 'integer'}
            },
            'startretries': {'type': 'integer'},
            'starttime': {'type': 'integer'},
            'stopsignal': {
                'type': 'array',
                'items': {
                    "type": "string",
                    "enum": ['SIGINT', 'SIGHUB', 'SIGILL', 'SIGQUIT', 'SIGTRAP', 'SIGABRT', 'SIGBUS', 'SIGFPE', 'SIGKILL', 'SIGUSR1', 'SIGUSR2', 'SIGPIPE', 'SIGALRM', 'SIGTERM']
                }
            },
            'stoptime': {'type': 'integer'},
            "stdout": {'type': 'string'},
            "stderr": {'type': 'string'},
        },
        'additionalProperties': False
    }
}


def is_dir(checker, instance):
    return isinstance(instance, str) and path.isdir(instance)


def is_valid_file(file):
    with open(file, 'r') as configurationfile:
        configurations = json.load(configurationfile)
        try:
            Draft7Validator.TYPE_CHECKER = Draft7Validator.TYPE_CHECKER.redefine_many({'dir': is_dir})
            Draft7Validator(fileSchema).validate(instance=configurations)
            return configurations
        except ValidationError as e:
            print(e)

def is_key_exists(data, key, message):
    if key not in data.keys() or not data[key]:
        raise ValueError(F'Missing Required Parameter: {message}')


def is_file_exists(file):
    if not path.exists(file):
        raise ValueError('File Not Found')

def is_valid_return_codes(returncodes):
    returncodes = returncodes.split(',')
    for code in returncodes:
        if not code.isnumeric():
            raise ValueError(F'Invalid Return Code')

def is_valid_environment(environment):
    environment = environment.split(',')
    for keyval in environment:
        key_val = keyval.split('=')
        if len(key_val) != 2:
            raise ValueError(F'Invalid Environment Format')

if __name__ == '__main__':
    if sys.argv[1]:
        is_valid_file(sys.argv[1])