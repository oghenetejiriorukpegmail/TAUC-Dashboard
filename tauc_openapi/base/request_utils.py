"""Utilities for processing TAUC requests - CORRECTED to match Java SDK."""

import json
import re
from typing import Dict, Optional, Any, get_type_hints
from urllib.parse import urlencode
from dataclasses import fields, is_dataclass
from .tauc_request import TAUCRequest
from .exceptions import TAUCApiException


class RequestUtils:
    """Utilities for processing request parameters."""

    @staticmethod
    def process_path_variables(url: str, request: TAUCRequest) -> str:
        """
        Replace path variables in URL with values from request object.

        Path variables are determined by matching {variable} in URL with request attributes.

        Args:
            url: URL template with {variable} placeholders
            request: Request object with path variable values

        Returns:
            URL with variables replaced

        Raises:
            TAUCApiException: If required path variable is missing
        """
        # Find all {variable} patterns in URL
        pattern = re.compile(r'\{(\w+)\}')
        matches = pattern.findall(url)

        result = url
        for var_name in matches:
            # Convert snake_case to camelCase if needed
            # Try original name first, then try snake_case conversion
            value = getattr(request, var_name, None)
            if value is None:
                # Try with underscores (network_id -> networkId)
                camel_name = RequestUtils._to_camel_case(var_name)
                value = getattr(request, camel_name, None)

            if value is None:
                raise TAUCApiException(f"Missing path variable: {var_name}")

            result = result.replace(f"{{{var_name}}}", str(value))

        return result

    @staticmethod
    def _to_camel_case(snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    @staticmethod
    def _is_path_variable(url: str, attr_name: str) -> bool:
        """Check if attribute is a path variable in the URL."""
        pattern = re.compile(r'\{(\w+)\}')
        path_vars = pattern.findall(url)
        return attr_name in path_vars or RequestUtils._to_camel_case(attr_name) in path_vars

    @staticmethod
    def process_query_params(url: str, request: TAUCRequest) -> Optional[Dict[str, str]]:
        """
        Extract query parameters from request object.

        Query parameters are attributes that:
        1. Have metadata marking them as query params, OR
        2. Are simple types (str, int, float, bool) AND not path variables

        Args:
            url: Request URL (to identify path variables)
            request: Request object

        Returns:
            Dictionary of query parameters, or None if no parameters
        """
        params = {}

        if not is_dataclass(request):
            return None

        for field in fields(request):
            # Skip if it's a path variable
            if RequestUtils._is_path_variable(url, field.name):
                continue

            # Check if field is marked as query parameter
            is_query = field.metadata.get('param_type') == 'query' if field.metadata else False

            # Get value
            value = getattr(request, field.name, None)

            if value is None:
                continue

            # Include if explicitly marked as query, or if it's a simple type
            if is_query or isinstance(value, (str, int, float, bool)):
                # Use metadata name if provided, otherwise use field name
                param_name = field.metadata.get('param_name', field.name) if field.metadata else field.name
                params[param_name] = str(value)

        return params if params else None

    @staticmethod
    def process_headers(request: TAUCRequest) -> Dict[str, str]:
        """
        Extract headers from request object.

        Args:
            request: Request object

        Returns:
            Dictionary of headers
        """
        headers = request.get_headers().copy()
        headers['Content-Type'] = request.get_content_type()
        return headers

    @staticmethod
    def process_request_body(url: str, request: TAUCRequest) -> Optional[str]:
        """
        Serialize request body based on content type.

        Body includes all fields that are NOT path or query parameters.
        Matches Java SDK logic: fields without @TAUCRequestPath, @TAUCRequestQuery, @TAUCRequestHeader
        become part of the request body.

        Args:
            url: Request URL (to identify path variables)
            request: Request object

        Returns:
            Serialized request body (JSON string), or None if no body
        """
        content_type = request.get_content_type()

        if content_type == "application/json; charset=UTF-8;":
            if not is_dataclass(request):
                return None

            body_dict = {}
            has_explicit_body = False

            # First check if there's an explicit body field
            for field in fields(request):
                if field.metadata.get('param_type') == 'body' if field.metadata else False:
                    # Explicit body field - use only this
                    value = getattr(request, field.name, None)
                    if value is not None:
                        return json.dumps(value, default=RequestUtils._json_serializer)
                    has_explicit_body = True

            # No explicit body, build from non-path/query fields
            for field in fields(request):
                # Skip path variables
                if RequestUtils._is_path_variable(url, field.name):
                    continue

                # Skip query parameters
                is_query = field.metadata.get('param_type') == 'query' if field.metadata else False
                if is_query:
                    continue

                # Skip header parameters
                is_header = field.metadata.get('param_type') == 'header' if field.metadata else False
                if is_header:
                    continue

                # Skip simple types that look like query params (unless explicitly marked as body)
                value = getattr(request, field.name, None)
                if value is None:
                    continue

                # Include in body if it's a complex type or explicitly not a simple query param
                if not isinstance(value, (type(None), type)) and not callable(value):
                    body_dict[field.name] = value

            if body_dict:
                # Convert snake_case keys to camelCase before JSON serialization
                camel_case_body = RequestUtils._to_camel_case_dict(body_dict)
                return json.dumps(camel_case_body, default=RequestUtils._json_serializer)

            return None

        elif content_type == "application/x-www-form-urlencoded":
            # Form-encoded data - matches Java SDK logic
            # Includes all fields except path variables, query params, and header params
            if not is_dataclass(request):
                return None

            form_dict = {}
            for field in fields(request):
                # Skip path variables
                if RequestUtils._is_path_variable(url, field.name):
                    continue

                # Skip query parameters
                is_query = field.metadata.get('param_type') == 'query' if field.metadata else False
                if is_query:
                    continue

                # Skip header parameters
                is_header = field.metadata.get('param_type') == 'header' if field.metadata else False
                if is_header:
                    continue

                value = getattr(request, field.name, None)
                if value is not None:
                    # Convert to string (form data is always strings)
                    form_dict[field.name] = str(value)

            return urlencode(form_dict) if form_dict else None

        return None

    @staticmethod
    def _to_camel_case_dict(snake_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Convert dictionary with snake_case keys to camelCase keys, filtering out None values."""
        camel_dict = {}
        for key, value in snake_dict.items():
            # Skip None values - Java SDK doesn't send null fields
            if value is None:
                continue

            # Convert key to camelCase
            camel_key = RequestUtils._to_camel_case(key)

            # Recursively convert nested dictionaries
            if isinstance(value, dict):
                converted = RequestUtils._to_camel_case_dict(value)
                # Only add if non-empty after filtering
                if converted:
                    camel_dict[camel_key] = converted
            elif isinstance(value, list):
                camel_dict[camel_key] = [
                    RequestUtils._to_camel_case_dict(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                camel_dict[camel_key] = value

        return camel_dict

    @staticmethod
    def _json_serializer(obj: Any) -> Any:
        """Custom JSON serializer for complex objects - converts snake_case to camelCase."""
        if is_dataclass(obj):
            # Convert dataclass to dict with snake_case keys
            snake_dict = {field.name: getattr(obj, field.name) for field in fields(obj)}
            # Convert to camelCase keys to match Java SDK
            return RequestUtils._to_camel_case_dict(snake_dict)
        elif hasattr(obj, '__dict__'):
            # Convert object dict to camelCase
            return RequestUtils._to_camel_case_dict(obj.__dict__)
        else:
            return str(obj)
