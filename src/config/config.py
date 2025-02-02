import yaml
import os
from dataclasses import dataclass, field

@dataclass
class ConfigParser:

    _config_path = field(default = './config/example.yaml')
    _user = field(default = {})
    _languages = field(default = {})
    _hobbies = field(default = {})
    _contact = field(default = {})

    def __post_init__(self):
        self.load_config()

    def load_config(self):
        if not os.path.exists(self._config_path):
            raise FileNotFoundError(f"Configuration file not found: {self._config_path}")

        with open(self._config_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        self._user = data.get('User', {})
        self._languages = data.get('Languages', {})
        self._hobbies = data.get('Hobbies', {})
        self._contact = data.get('Contact', {})

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def languages(self):
        return self._languages

    @languages.setter
    def languages(self, value):
        self._languages = value

    @property
    def hobbies(self):
        return self._hobbies

    @hobbies.setter
    def hobbies(self, value):
        self._hobbies = value

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        self._contact = value
