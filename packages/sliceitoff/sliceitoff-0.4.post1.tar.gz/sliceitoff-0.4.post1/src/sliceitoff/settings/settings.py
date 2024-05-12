""" settings.settings - handles settings reading, updating and writing """
import os
from pathlib import Path
from .static import DEFAULT_SETTINGS

TEST_CONFIG_FILE = os.getenv("TEST_CONFIG_FILE")

class Settings:
    """ Handles loading and saving settings from config file"""
    def __init__(self):
        self.settings=[]
        if TEST_CONFIG_FILE:
            self.config_filename = Path(TEST_CONFIG_FILE)
        else:
            if os.name == 'nt':
                self.config_filename = (Path.home().resolve()
                        .joinpath('sliceitoff.cfg'))
            else:
                self.config_filename = (Path.home().resolve()
                        .joinpath('.config').joinpath('sliceitoffrc'))
        if not self.config_filename.is_file():
            self.settings=DEFAULT_SETTINGS[:]
            return
        with open(self.config_filename, "r", encoding="utf-8") as config_file:
            for line in config_file:
                entry = self.validate_line(line)
                if not entry:
                    continue
                self.settings.append(entry)

    def validate_line(self, line):
        """ Validates and splits config line """
        if not line or line[0] == '#':
            return None
        data = line.split('=')
        if len(data) != 2:
            return None
        return data[0].strip(), data[1].strip()

    def get_values(self, option):
        """ Gets all values for certain option """
        return [x[1] for x in self.settings if x[0]==option]

    def put_values(self, option, values):
        """ Puts multiple values with same option name """
        for x in values:
            self.put_value(option, x)

    def remove_values(self, option):
        """ Removes all values with given option name """
        for x in self.settings[:]:
            if x[0]==option:
                self.settings.remove(x)

    def replace_values(self, option, values):
        """ After replacement only given values are attached to the option """
        self.remove_values(option)
        self.put_values(option, values)

    def get_value(self, option):
        """ Gets first value of the option """
        v = self.get_values(option)
        if not v:
            return None
        return v[0]

    def get_value_or_default(self, option):
        """ Gets first value if found otherwise default """
        v = self.get_value(option)
        if v:
            return v
        return [x[1] for x in DEFAULT_SETTINGS if x[0]==option][0]

    def put_value(self, option, value):
        """ Puts single value with option name """
        self.settings.append((option, value))

    def replace_value(self, option, value):
        """ Replaces even multiple values from option just to add one """
        self.remove_values(option)
        self.put_value(option, value)

    def save(self):
        """ Saves options to config file """
        with open(self.config_filename, 'w', encoding="utf-8") as config_file:
            for option, value in self.settings:
                config_file.write(f"{option}={value}\n")

# Initialize only one time
try:
    # pylint: disable = used-before-assignment
    # This is intented behaviour
    settings
except NameError:
    settings = Settings()
