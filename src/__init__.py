import sys
from src.core.config_extractor import *

application_root = 'G:\\Photo'

sys.path.extend([Config().get_key_value('application_root')])