from check import is_valid_file, is_key_exists, is_file_exists
import json

def show_file(file):
    is_file_exists(file)
    data = is_valid_file(file)
    print(json.dumps(data, indent=4))

def update_file(file, configuration):
    is_key_exists(configuration, 'name', '--name NAME')
    is_key_exists(configuration, 'cmd', '-C COMMAND')
    configurations = is_valid_file(file)
    with open(file, 'w') as configurationfile:
        configurationfile.seek(0)
        #configurations.append(configuration)
        name = configuration['name']
        del configuration['name']
        configurations[F'{name}'] = configuration
        json.dump(configurations, configurationfile, indent=4)

def create_file(file, configuration):
    is_key_exists(configuration, 'name', '--name NAME')
    is_key_exists(configuration, 'cmd', '-C COMMAND')
    with open(file, 'w') as configurationfile:
        name = configuration['name']
        del configuration['name']
        json.dump({F'{name}': configuration}, configurationfile, indent=4)