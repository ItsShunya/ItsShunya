from datetime import datetime
from dataclasses import dataclass, field
from dataclass_wizard import YAMLWizard

@dataclass
class User:
    username:           str
    birthday:           datetime
    operative_system:   list[str]  = field(default_factory=list)
    position:           str | None = None
    ide:                list[str]  = field(default_factory = list)

@dataclass
class Languages:
    programming:    list[str] = field(default_factory = list)
    other:          list[str] = field(default_factory = list)
    real:           list[str] = field(default_factory = list)

@dataclass
class Activities:
    software:       list[str] = field(default_factory = list)
    hardware:       list[str] = field(default_factory = list)
    other:          list[str] = field(default_factory = list)

@dataclass
class Contact:
    personal_mail:  str | None = None
    work_mail:      str | None = None
    linkedin:       str | None = None
    discord:        str | None = None
    stackoverflow:  str | None = None

@dataclass
class ConfigParser(YAMLWizard):
    #config_path: str = field(default='./config/example.yaml', repr=False)
    user:       User
    languages:  Languages
    activities: Activities
    contact:    Contact
