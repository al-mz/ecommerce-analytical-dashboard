

import configparser
import json
import logging
from pathlib import Path

def load_config_file(config_path:Path, logger:logging.Logger = logging.getLogger('config_file')) -> dict:
    """Returns the config file loaded from the specified path, as a dictionary.
    Args:
        config_path (Path): Path to the config file
        logger (logging.Logger, optional): Logger that will be used. Defaults to logging.getLogger('config_file').
    Returns:
        dict: Dictionary with the config variables loaded.
    """
    if logger is not None:
        logger.info('Loading config')
    else:
        print('Loading config')
    converters = {
                'list_int': lambda x: [int(i.strip()) for i in x.split(',')],
                'int_none': lambda x: None if x.lower() == 'none' else int(x),
                'list_str': lambda x: [i.strip() for i in x.split(',')],
                'path': lambda x: Path(x),
                }
    config_data = configparser.ConfigParser(converters=converters)
    config_data.read(config_path)
    config_file = {}

    # Path config
    section = 'path_config'
    config_file['data_path'] = config_data.getpath(section, 'data_path')
    config_file['utils_path'] = config_data.getpath(section, 'utils_path')
    config_file['postgres_env'] = config_data.getpath(section, 'postgres_env')
    config_file['superset_env'] = config_data.getpath(section, 'superset_env')
    
    if logger is not None:
        logger.info(f'Config: \n{json.dumps({str(key): str(value) for key, value in config_file.items()}, sort_keys = True, indent = 4)}')
    else:
        print(f'Config: \n{json.dumps({str(key): str(value) for key, value in config_file.items()}, sort_keys = True, indent = 4)}') 
    return config_file