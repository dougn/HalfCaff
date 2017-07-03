import glob
from setuptools import setup

APP = ['HalfCaff.py']
APP_NAME = "HalfCaff"
DATA_FILES = glob.glob('halfcaff/*.icns')
OPTIONS = {
    'iconfile': 'halfcaff/halfcaff.icns',
    'argv_emulation': False,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)