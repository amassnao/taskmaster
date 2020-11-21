from check import is_key_exists, is_valid_environment, is_valid_return_codes

def surround_exit(func, *args, exitcode=2):
    try:
        func(*args)
    except ValueError as error:
        print(error)
        exit(exitcode)

def clean_options(options):
    configuration = vars(options)
    surround_exit(is_key_exists, configuration, 'configurationfile', '-c configurationfile')
    #surround_exit(is_valid_return_codes, options.returncodes)
    if options.exitcodes:
        options.exitcodes = [int(n) for n in options.exitcodes.split(',')]
    if options.env:
        surround_exit(is_valid_environment, options.env)
        environment = options.env.split(',')
        options.env = environment
    file = options.configurationfile
    show = options.show
    configuration['configurationfile'] = None
    configuration['show'] = None
    configuration['standalone'] = None
    keys = list(configuration.keys())
    for e in keys:
        if not configuration[e]:
            del configuration[e]
    return file, show, configuration