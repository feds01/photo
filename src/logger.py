import logging
from src.core.config import Config, Fatal

if (Config.get("debug")):

    if(Config.get("log_file") is ""):
        Fatal("Debug mode enabled, but no log file provided")

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=Config.get('log_file'),
                        filemode='w')

    logger = logging.FileHandler(Config.get('log_file'))

else:
    logger = logging.getLogger("main-logger")
    logger.disabled = True

logger.setLevel(logging.DEBUG)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('connected to debug console v0.10.')

# Now, define a couple of other loggers which might represent areas in your
# application:


