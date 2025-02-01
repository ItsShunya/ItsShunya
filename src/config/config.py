import yaml
import os

class ConfigParser:
    def __init__(self, config_path='./config/config.yaml'):
        self._config_path = config_path
        self._user = {}
        self._languages = {}
        self._hobbies = {}
        self._contact = {}
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