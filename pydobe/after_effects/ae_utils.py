# AE GLOBAL FUNCTIONS
from pydobe.core import eval_script_returning_object


def time_to_current_format(time, fps):
    return eval_script_returning_object(f'timeToCurrentFormat({time}, {fps})')


def current_format_to_time(time, fps):
    if type(time) == int:
        return eval_script_returning_object(f'currentFormatToTime({time}, {fps})')
    return eval_script_returning_object(f'currentFormatToTime("{time}", {fps})')
