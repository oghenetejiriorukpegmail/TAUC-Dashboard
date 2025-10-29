"""Client authentication type enumeration."""

from enum import Enum


class ClientType(Enum):
    """Authentication type for TAUC API client."""

    ACCESS_KEY = "AkSk"
    OAUTH_TWO = "Oauth2"
