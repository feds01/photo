import logging
from src.core.config_extractor import Config

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=Config.get('log_file'),
                    filemode='w')

logger = logging.FileHandler(Config.get('log_file'))
logger.setLevel(logging.DEBUG)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('connected to debug console v0.10.')

# Now, define a couple of other loggers which might represent areas in your
# application:


