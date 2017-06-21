import os
import random
from src.core.config_extractor import *

def check_process_count(silent=False, return_pnum=False):
    _raw_value = os.cpu_count() * Config.get('thread.instance_multiplier')

    if _raw_value <= 0:
        Fatal('process count cannot be %s' % _raw_value, True,
              'incorrect config magic process number of %s' % _raw_value,
              'instance_multiplier=%s' % (_raw_value / os.cpu_count()))
    elif _raw_value >= 32:
        if not silent:
            config_warning('magic process number is extremely large.')
        else:
            pass

    if type(_raw_value) != int:
        try:
            if round(_raw_value, 0) == _raw_value:
                _raw_value = int(_raw_value)
            else:
                Fatal('process count cannot be float.', True, 'incorrect config magic process number of %s' %
                  (_raw_value / os.cpu_count()))
        except TypeError as error:
            Fatal('process count cannot be float.', True, 'incorrect config magic process number of %s' %
                  _raw_value, 'incorrect type: %s' % type(_raw_value), '%s' % error)
        finally:
            if not silent:
                config_warning('magic process instance multiplier number was processed as float.')

    return _raw_value if return_pnum else True


def get_candidates(process_count, candidates):
    selected_candidates = []
    x = 0  # controller for number of needed candidates

    while x < candidates:
        attempt = random.randint(0, process_count-1)  # inclusive range
        if attempt in selected_candidates:
            continue
        else:
            selected_candidates.append(attempt)
            x += 1

    return selected_candidates