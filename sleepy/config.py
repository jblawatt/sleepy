
from configparser import ConfigParser


def get():
    config = ConfigParser()
    config.read('sleepyrc')
    return config

