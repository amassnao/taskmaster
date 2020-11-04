from check import is_key_exists

def surround_exit(func, *args, exitcode=2):
    try:
        func(*args)
    except ValueError as error:
        print(error)
        exit(exitcode)

def clean_options(options):
    configuration = vars(options)
    file = options.configurationfile
    show = options.show
    surround_exit(lambda : is_key_exists(configuration, 'configurationfile', '-c configurationfile'))
    del configuration['configurationfile']
    del configuration['show']
    return file, show, configuration