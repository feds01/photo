import os
import random
from src.core.config import *


def check_process_count(v=True, return_pnum=False):
    _raw_value = os.cpu_count() * Config.get('thread.instance_multiplier')

    if _raw_value <= 0:
        Fatal('process count cannot be %s' % _raw_value,
              'incorrect config magic process number of %s' % _raw_value,
              'instance_multiplier=%s' % (_raw_value / os.cpu_count())).stop()
    elif _raw_value >= 32:
        if not v:
            config_warning('magic process number is extremely large.')
        else:
            pass

    if type(_raw_value) != int:
        try:
            if round(_raw_value, 0) == _raw_value:
                _raw_value = int(_raw_value)
            else:
                Fatal('process count cannot be float.', 'incorrect config magic process number of %s' %
                  (_raw_value / os.cpu_count())).stop()
        except TypeError as error:
            Fatal('process count cannot be float.', 'incorrect config magic process number of %s' %
                  _raw_value, 'incorrect type: %s' % type(_raw_value), '%s' % error).stop()
            if not v:
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