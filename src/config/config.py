import yaml
import os
from dataclasses import dataclass, field
from dataclass_wizard import property_wizard
from collections import defaultdict
from typing import Dict, Optional, Annotated

@dataclass
class ConfigParser:

    config_path:    str  = field(default = './config/example.yaml')
    user:           Annotated[
        defaultdict[str, str], field(default_factory = lambda: defaultdict(str))]
    languages:      Annotated[
         defaultdict[str, str], field(default_factory = lambda: defaultdict(str))]
    hobbies:           Annotated[
        defaultdict[str, str], field(default_factory = lambda: defaultdict(str))]
    contact:           Annotated[
        defaultdict[str, str], field(default_factory = lambda: defaultdict(str))]

    # We add these _variables to help the IDE identify the @property utilities.
    # This is a workaround for using @property together with @dataclass.
    # see https://florimond.dev/en/posts/2018/10/reconciling-dataclasses-and-properties-in-python
    _config_path:   str  = field(init = False)
    _user:          Optional[Dict[str, str]] = field(init = False, repr = False)
    _languages:     Optional[Dict[str, str]] = field(init = False, repr = False)
    _hobbies:       Optional[Dict[str, str]] = field(init = False, repr = False)
    _contact:       Optional[Dict[str, str]] = field(init = False, repr = False)

    def __post_init__(self):
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        self.user = data.get('User', {})
        self.languages = data.get('Languages', {})
        self.hobbies = data.get('Hobbies', {})
        self.contact = data.get('Contact', {})

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
