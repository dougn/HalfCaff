import os
import inspect
import functools
import rumps

_RESOURCE_DIR = None
_APP_URL = None

def is_dev_mode():
    return '/site-packages.zip/' not in __file__

def get_app_url():
    global _APP_URL
    if is_dev_mode():
        return None
    if _APP_URL is not None:
        return _APP_URL
    _APP_URL = os.path.dirname(get_resource_dir())
    return _APP_URL

def get_resource_dir():
    global _RESOURCE_DIR
    if _RESOURCE_DIR is not None:
        return _RESOURCE_DIR
    d = os.path.dirname
    base = d(__file__)
    if is_dev_mode():
        _RESOURCE_DIR =  base
    else:
        _RESOURCE_DIR = d(d(d(d(base))))
    return _RESOURCE_DIR

def icon(name):
    return get_resource_dir() + '/' + name

def get_timer(func):
    if inspect.ismethod(func):
        func = func.__func__
    timers = getattr(rumps.timer, '*timers', [])
    for timer in timers:
        if timer.callback is func:
            return timer
    return None

def print_except(func):
    def wrapper(func, *args, **kwdargs):
        try:
            return func(*args, **kwdargs)
        except:
            ## replace with full stack trace
            print sys.exc_info()
            raise
    return functools.partial(wrapper, func)
        