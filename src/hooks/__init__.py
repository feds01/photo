import sys
from src.core.config_extractor import *

sys.path.extend([Config().get_key_value('application_root')])