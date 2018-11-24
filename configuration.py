import yaml
import logging

configuration = yaml.load(open('config.yaml', 'r'))

logger_config = configuration['logger']
format, level = logger_config['format'], logging.getLevelName(logger_config['level'])

logging.basicConfig(format=format, level=level)

logging.info('configuration »» loaded successfully for: %s' % ', '.join(configuration.keys()))
