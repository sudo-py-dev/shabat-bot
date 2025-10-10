
import os
import json
from tools.logger import logger
from enum import Enum


def load_json(file_path: str) -> dict:
    try:
        if not os.path.exists(file_path):
            return {}
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {e}")
        return {}


messages = load_json("locales/messages.json")
privileges = load_json("locales/privileges.json")


class Messages:
    def __init__(self, language: str = "he"):
        self.language = language
        self.messages = dict(messages)

    def __getattr__(self, name):
        if self.language and name in self.messages.get(self.language, {}):
            return self.messages[self.language][name]
        else:
            # Fallback to English if the message doesn't exist in the current language
            if name in self.messages.get("en", {}):
                return self.messages["en"][name]
            else:
                return f"Message '{name}' not found"

    def __setattr__(self, name, value):
        if name == 'language' or name == 'messages':
            super().__setattr__(name, value)
        else:
            # Handle dynamic message setting
            if hasattr(self, 'language') and hasattr(self, 'messages') and self.language:
                if self.language in self.messages and name in self.messages[self.language]:
                    self.messages[self.language][name] = value
                elif self.language in self.messages:
                    self.messages[self.language][name] = value
                # Don't set as instance attribute for message keys

    def languages(self):
        """Return a list of all available language codes."""
        return list(self.messages.keys())
    
    def languages_names(self):
        """Return a list of all available language names."""
        return [self.messages[language]['language'] for language in self.messages]


class PrivilegesMessages:
    def __init__(self, language: str = "he"):
        self.language = language
        self.privileges = dict(privileges)

    def __getattr__(self, name):
        if self.language and name in self.privileges.get(self.language, {}):
            return self.privileges[self.language][name]
        else:
            # Fallback to English if the message doesn't exist in the current language
            if name in self.privileges.get("en", {}):
                return self.privileges["en"][name]
            else:
                return f"Privilege '{name}' not found"

    def __setattr__(self, name, value):
        if name == 'language' or name == 'privileges':
            super().__setattr__(name, value)
        else:
            # Handle dynamic message setting
            if hasattr(self, 'language') and hasattr(self, 'privileges') and self.language:
                if self.language in self.privileges and name in self.privileges[self.language]:
                    self.privileges[self.language][name] = value
                elif self.language in self.privileges:
                    self.privileges[self.language][name] = value
                # Don't set as instance attribute for message keys

    def exists_privilege(self, privilege: str) -> bool:
        return privilege in self.privileges.get(self.language, {})


class AccessPermission(Enum):
    """Enum for access permission."""
    ALLOW = 1
    """User has permission to perform the action."""
    DENY = 2
    """User does not have permission to perform the action."""
    NOT_ADMIN = 3
    """User is not an admin."""
    CHAT_NOT_FOUND = 4
    """Chat is not found."""
    NEED_UPDATE = 5
    """Chat needs update."""
