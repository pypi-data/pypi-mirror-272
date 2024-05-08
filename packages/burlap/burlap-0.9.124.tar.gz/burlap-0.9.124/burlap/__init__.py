import collections
import importlib
import inspect
import json
import logging
import os
import pkgutil
import sys
import types
import warnings

try:
    import yaml
    from fabric.api import env, hide, settings
    from fabric.decorators import task, runs_once
    from fabric.tasks import WrappedCallableTask
    from fabric.utils import _AliasDict

    # Variables cached per-role. Must be after deepcopy.
    env._rc = type(env)()

    # Force dictionaries to be serialized in multi-line format.
    def _represent_dictorder(self, data):
        return self.represent_mapping('tag:yaml.org,2002:map', data.items())

    def _represent_tuple(self, data):
        return self.represent_sequence('tag:yaml.org,2002:seq', data)

    def _construct_tuple(self, node):
        return tuple(self.construct_sequence(node))

    def _represent_function(self, data):
        return self.represent_scalar('tag:yaml.org,2002:null', 'null')

    yaml.add_representer(type(env), _represent_dictorder)
    yaml.add_representer(_AliasDict, _represent_dictorder)
    yaml.add_constructor('tag:yaml.org,2002:python/tuple', _construct_tuple)
    yaml.add_representer(types.FunctionType, _represent_function)
except ImportError as exc:
    print(f'Unable to initialize fabric or yaml: {exc}', file=sys.stderr)

try:
    env
except NameError as exc:
    print(f'Unable to initialize env: {exc}', file=sys.stderr)
    env = None
    env_default = {}

try:
    from . import common
    Satchel = common.Satchel
    ServiceSatchel = common.ServiceSatchel
    ContainerSatchel = common.ContainerSatchel
    env_default = common.save_env()
except (ImportError, NameError) as exc:
    print(f'Unable to initialize common: {exc}', file=sys.stderr)
    common = None

try:
    from . import debug
except (ImportError, NameError) as exc:
    print(f'Unable to initialize debug: {exc}', file=sys.stderr)
    debug = None

VERSION = (0, 9, 124)
__version__ = '.'.join(map(str, VERSION))

burlap_populate_stack = int(os.environ.get('BURLAP_POPULATE_STACK', 1))
no_load = int(os.environ.get('BURLAP_NO_LOAD', 0))

# Show virtually all logging messages by default.
default_loglevel = logging.getLevelName(os.environ.get('LOGLEVEL', 'INFO').upper())
logger = logging.getLogger()
handler = logging.StreamHandler()
try:
    logger.setLevel(default_loglevel)
    handler.setLevel(default_loglevel)
except ValueError:
    logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Silence INFO-level Paramiko noise.
logging.getLogger('paramiko').setLevel(logging.WARNING)


def _get_environ_handler(name, d):
    """
    Dynamically creates a Fabric task for each configuration role.
    """

    def func(site=None, **kwargs):
        from fabric import state # pylint: disable=import-outside-toplevel

        # We can't auto-set default_site, because that break tasks that have
        # to operate over multiple sites.
        # If a task requires a site, it can pull from default_site as needed.
        #site = site or d.get('default_site') or env.SITE

        BURLAP_SHELL_PREFIX = int(os.environ.get('BURLAP_SHELL_PREFIX', '0'))
        if BURLAP_SHELL_PREFIX:
            print('#!/bin/bash')
            print('# DO NOT EDIT. AUTO-GENERATED WITH:')
            print('#')
            print('#     BURLAP_SHELL_PREFIX=1 BURLAP_COMMAND_PREFIX=0 fab {}'.format(' '.join(sys.argv[1:])))
            print('#')

        BURLAP_COMMAND_PREFIX = int(os.environ.get('BURLAP_COMMAND_PREFIX', '1'))
        with_args = []
        if not BURLAP_COMMAND_PREFIX:
            for k in state.output:
                state.output[k] = False

        hostname = kwargs.get('hostname')
        hostname = hostname or kwargs.get('name')
        hostname = hostname or kwargs.get('hn')
        hostname = hostname or kwargs.get('h')

        verbose = int(kwargs.get('verbose', '0'))
        common.set_verbose(verbose)

        # Load environment for current role.
        env.update(env_default)
        env[common.ROLE] = os.environ[common.ROLE] = name
        if site:
            env[common.SITE] = os.environ[common.SITE] = site
        env.update(d)

        # Load host retriever.
        retriever = None
        if env.hosts_retriever:
            # Dynamically retrieve hosts.
            retriever = common.get_hosts_retriever()
            if verbose:
                print('Using retriever:', env.hosts_retriever, retriever)

        # Load host translator.
        translator = None
        if hostname:
            # Filter hosts list by a specific host name.
            module_name = '.'.join(env.hostname_translator.rsplit('.', maxsplit=1)[:-1])
            func_name = env.hostname_translator.rsplit('.', maxsplit=1)[-1]
            translator = getattr(importlib.import_module(module_name), func_name)

        # Re-load environment for current role, incase loading
        # the retriever/translator reset some environment values.
        env.update(env_default)
        env[common.ROLE] = os.environ[common.ROLE] = name
        if site:
            env[common.SITE] = os.environ[common.SITE] = site
        env.update(d)

        # Dynamically retrieve hosts.
        if env.hosts_retriever:
            if verbose:
                print('Building host list with retriever %s...' % env.hosts_retriever)
            env.hosts = list(retriever(site=site))
            if verbose:
                print('Found hosts:')
                print(env.hosts)

        # Filter hosts list by a specific host name.
        if hostname:
            _hostname = hostname
            hostname = translator(hostname=hostname)
            _hosts = env.hosts
            env.hosts = [_ for _ in env.hosts if _ == hostname]
            assert env.hosts, f'Hostname {_hostname} does not match any known hosts.'

        if env.is_local is None:
            if env.hosts:
                env.is_local = 'localhost' in env.hosts or '127.0.0.1' in env.hosts
            elif env.host_string:
                env.is_local = 'localhost' in env.host_string or '127.0.0.1' in env.host_string

        for cb in common.post_role_load_callbacks:
            cb()

        # Ensure satchels don't cache values from previously loaded roles.
        common.reset_all_satchels()

        if env.hosts and not env.host_string:
            env.host_string = env.hosts[0]

        if verbose:
            print(f'Loaded role {name}.', file=sys.stderr)

    func.__doc__ = f'Sets enivronment variables for the "{name}" role.'
    func.role = name
    return func


def update_merge(d, u):
    """
    Recursively merges two dictionaries.

    Uses fabric's AttributeDict so you can reference values via dot-notation.
    e.g. env.value1.value2.value3...

    http://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            r = update_merge(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def find_yaml_settings_fn(name, local=False, fn='settings.yaml'):
    # If name is a valid path, then use that.
    if os.path.isfile(fn):
        return fn
    # Otherwise, include file names are symbolic and implicitly refer to a "settings.yaml" file
    # in an explicitly named role directory.
    if local:
        settings_fn = os.path.join(common.ROLE_DIR, name, 'settings_local.yaml')
    else:
        settings_fn = os.path.join(common.ROLE_DIR, name, fn)
    if os.path.isfile(settings_fn):
        return settings_fn


def load_yaml_settings(name, priors=None, verbose=0):
    verbose = int(verbose)
    config = type(env)()
    if priors is None:
        priors = set()
    if name in priors:
        return config
    priors.add(name)

    settings_fn = find_yaml_settings_fn(name)
    if not settings_fn:
        warnings.warn(f'Warning: Could not find Yaml settings for role {name}.')
        return config
    if verbose:
        print('Loading settings:', settings_fn)
    with open(settings_fn, encoding='utf8') as fin:
        config.update(yaml.safe_load(fin) or type(env)())

    if 'inherits' in config:
        parent_name = config['inherits']
        del config['inherits']
        parent_config = load_yaml_settings(parent_name, priors=priors, verbose=verbose)
        parent_config.update(config)
        config = parent_config

    # Load includes.
    includes = config.pop('includes', [])
    load_includes = []
    for _include_fn in includes:
        load_includes.append(_include_fn)
        include_fn = find_yaml_settings_fn(name=name, fn=_include_fn)
        assert include_fn, 'Invalid include file: %s' % _include_fn
        if verbose:
            print('Loading include settings:', include_fn)
        with open(include_fn, encoding='utf8') as fin:
            data = yaml.safe_load(fin)
        config.update(data)

    # Load local overrides.
    settings_local_fn = find_yaml_settings_fn(name, local=True)
    if settings_local_fn:
        if verbose:
            print('Loading local settings:', settings_local_fn)
        with open(settings_local_fn, encoding='utf8') as fin:
            data = yaml.safe_load(fin) or type(env)()
        includes = data.pop('includes', [])
        config.update(data)

        # Load local includes.
        for _include_fn in includes:
            load_includes.append(_include_fn)
            include_fn = find_yaml_settings_fn(name=name, fn=_include_fn)
            assert include_fn, 'Invalid include file: %s' % _include_fn
            if verbose:
                print('Loading include settings:', include_fn)
            with open(include_fn, encoding='utf8') as fin:
                data = yaml.safe_load(fin)
            config.update(data)

    config['includes'] = load_includes

    return config


try:

    @task
    @runs_once
    def shell(*args, **kwargs):
        return debug.debug.shell(*args, **kwargs)
except NameError:
    pass

CHECK_VERSION = int(os.environ.get('BURLAP_CHECK_VERSION', '1'))


def check_version():
    """
    Compares the local version against the latest official version on PyPI and displays a warning message if a newer release is available.

    This check can be disabled by setting the environment variable BURLAP_CHECK_VERSION=0.
    """
    global CHECK_VERSION
    if not CHECK_VERSION:
        return
    # Ensure we only check once in this process.
    CHECK_VERSION = 0
    # Lookup most recent remote version.
    try:
        from urllib.request import urlopen # pylint: disable=import-outside-toplevel
    except ImportError:
        # The only reason this would fail is if it's being run during the initial setup.py install, when dependencies haven't all been installed yet.
        return
    try:
        with urlopen('https://pypi.org/pypi/burlap/json') as response:
            data = json.loads(response.read().decode())
        remote_release = sorted(tuple(map(int, _.split('.'))) for _ in data['releases'].keys())[-1]
        remote_release_str = '.'.join(map(str, remote_release))
        local_release = VERSION
        local_release_str = '.'.join(map(str, local_release))
        # Display warning.
        if remote_release > local_release:
            print('\033[93m')
            print(f'You are using burlap version {local_release_str}, however version {remote_release_str} is available.')
            print("You should consider upgrading via the 'pip install --upgrade burlap' command.")
            print('\033[0m')
    except Exception as exc:
        print('\033[93m')
        print(f'Unable to check for updated burlap version: {exc}')
        print('\033[0m')


check_version()


def populate_fabfile():
    """
    Automatically includes all submodules and role selectors
    in the top-level fabfile using spooky-scary black magic.

    This allows us to avoid manually declaring imports for every module, e.g.

        import burlap.pip
        import burlap.vm
        import burlap...

    which has the added benefit of allowing us to manually call the commands
    without typing "burlap".

    This is soley for convenience. If not needed, it can be disabled
    by specifying the environment variable:

        export BURLAP_POPULATE_STACK=0
    """
    stack = inspect.stack()
    fab_frame = None
    for frame_obj, script_fn, line, _, _, _ in stack:
        if 'fabfile.py' in script_fn:
            fab_frame = frame_obj
            break
    if not fab_frame:
        return
    try:
        locals_ = fab_frame.f_locals
        for module_name, module in sub_modules.items():
            locals_[module_name] = module
        for role_name, role_func in role_commands.items():
            assert role_name not in sub_modules, (f'The role {role_name} conflicts with a built-in submodule. Please choose a different name.')
            locals_[role_name] = role_func
        locals_['common'] = common

        # Put all debug commands into the global namespace.
        locals_['shell'] = shell

        # Put all virtual satchels in the global namespace so Fabric can find them.
        for _module_alias in common.post_import_modules:
            exec(f'import {_module_alias}') # pylint: disable=exec-used
            locals_[_module_alias] = locals()[_module_alias]

    finally:
        del stack


def load_role_handler(name):
    _config = load_yaml_settings(name)
    _f = _get_environ_handler(name, _config)
    _f = WrappedCallableTask(_f, name=name)
    return _f


# Dynamically create a Fabric task for each role.
role_commands = {}
if common and not no_load:
    if os.path.isdir(common.ROLE_DIR):
        for _name in os.listdir(common.ROLE_DIR):
            _settings_fn = os.path.join(common.ROLE_DIR, _name, 'settings.yaml')
            if _name.startswith('.') or not os.path.isfile(_settings_fn):
                continue
            _f = load_role_handler(_name)
            _var_name = 'role_' + _name
            _cmd = f'{_var_name} = _f'
            exec(_cmd) # pylint: disable=exec-used
            role_commands[_var_name] = _f

    # Auto-import all sub-modules.
    sub_modules = {'common': common}
    __all__ = []
    print('__path__:', __path__)
    for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
        if module_name in locals():
            continue
        if module_name.startswith('tests'):
            continue
        __all__.append(module_name)
        module = loader.find_spec(module_name).loader.load_module(module_name)
        sub_modules[module_name] = module

    if burlap_populate_stack:
        populate_fabfile()

    # Execute any callbacks registered by sub-modules.
    # These are useful for calling inter-sub-module functions
    # after the modules tasks are registered so task names don't get
    # mistakenly registered under the wrong module.
    for cb in common.post_callbacks:
        cb()
