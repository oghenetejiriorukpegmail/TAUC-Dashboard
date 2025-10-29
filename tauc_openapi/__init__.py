"""
TP-Link TAUC OpenAPI Python SDK

A Python client library for interacting with TP-Link's Trusted ACS User Console (TAUC) REST API.
Provides programmatic access to manage TP-Link network devices including routers and mesh systems.

Version: 1.8.3
"""

from .execute.api_client import ApiClient
from .base.exceptions import TAUCApiException
from .base.client_type import ClientType

__version__ = "1.8.3"
__all__ = ["ApiClient", "TAUCApiException", "ClientType"]
