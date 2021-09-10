import configparser
import os

config = configparser.ConfigParser()
config.read('app/parameters')

ACCESS_KEY_FIXER = config['DEFAULT']['ACCESS_KEY_FIXER']
TOKEN_BMX = config['DEFAULT']['TOKEN_BMX']
if not ACCESS_KEY_FIXER:
    ACCESS_KEY_FIXER = os.environ.get('ACCESS_KEY_FIXER')
if not TOKEN_BMX:
    TOKEN_BMX = os.environ.get("TOKEN_BMX")

TOKEN_TEST = config['DEFAULT']['TOKEN_TEST']
TIMES = int(config['DEFAULT']['TIMES'])
MINUTES = int(config['DEFAULT']['MINUTES'])
SECONDS = int(config['DEFAULT']['SECONDS'])
