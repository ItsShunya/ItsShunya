"""Configuration parser module for user data using dataclasses and YAML."""

from datetime import datetime
from dataclasses import dataclass, field

from dataclass_wizard import YAMLWizard


@dataclass
class User:
    """
    A dataclass representing user configuration and metadata.

    Attributes
    ----------
    username : str
        The username of the user.
    name : str
        The user's real name.
    surname : str
        The user's real surname.
    birthday : datetime
        The user's date of birth.
    operative_system : str | None, optional
        Operating system the user is using.
    position : str | None, optional
        The user's position or role (if applicable).
    company : str | None, optional
        The company where the user works.
    ide : str | None, optional
        IDE used by the user.
    """

    username:           str
    name:               str
    surname:            str
    birthday:           datetime
    operative_system:   str | None = None
    position:           str | None = None
    company:            str | None = None
    ide:                str | None = None


@dataclass
class Languages:
    """
    A dataclass representing programming and other languages used by the user.

    Attributes
    ----------
    programming : list[str], optional
        List of programming languages the user knows.
    other : list[str], optional
        List of other non-programming languages the user knows.
    real : list[str], optional
        List of real-world languages the user speaks.
    """

    programming:    list[str] = field(default_factory=list)
    other:          list[str] = field(default_factory=list)
    real:           list[str] = field(default_factory=list)


@dataclass
class Activities:
    """
    A dataclass representing user's software, hardware, and other activities.

    Attributes
    ----------
    software : list[str], optional
        List of software-related activities the user is involved in.
    hardware : list[str], optional
        List of hardware-related activities the user is involved in.
    other : list[str], optional
        List of other activities the user is involved in.
    """

    software:   list[str] = field(default_factory=list)
    hardware:   list[str] = field(default_factory=list)
    other:      list[str] = field(default_factory=list)


@dataclass
class Contact:
    """
    A dataclass representing user's contact information.

    Attributes
    ----------
    personal_mail : str | None, optional
        User's personal email address (if applicable).
    web: str | None, optional
        User's website.
    work_mail : str | None, optional
        User's work email address (if applicable).
    linkedin : str | None, optional
        User's LinkedIn profile URL (if applicable).
    discord : str | None, optional
        User's Discord username or ID (if applicable).
    stackoverflow : str | None, optional
        User's Stack Overflow profile URL (if applicable).
    """

    personal_mail:  str | None = None
    web:            str | None = None
    work_mail:      str | None = None
    linkedin:       str | None = None
    discord:        str | None = None
    stackoverflow:  str | None = None


@dataclass
class ConfigParser(YAMLWizard):
    """
    A dataclass for parsing and storing configuration data.

    Inherits from YAMLWizard to enable YAML serialization/deserialization.

    Attributes
    ----------
    user : User
        User configuration and metadata.
    languages : Languages
        Programming and other languages used by the user.
    activities : Activities
        Software, hardware, and other activities the user is involved in.
    contact : Contact
        User's contact information.
    """

    user:       User
    languages:  Languages
    activities: Activities
    contact:    Contact
