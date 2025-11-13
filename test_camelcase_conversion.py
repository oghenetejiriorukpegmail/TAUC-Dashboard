#!/usr/bin/env python3
"""
Test script to verify snake_case to camelCase conversion in request_utils.py
"""

import json
from tauc_openapi.base.request_utils import RequestUtils


def test_to_camel_case():
    """Test the _to_camel_case method."""
    print("Testing _to_camel_case()...")

    test_cases = [
        ("network_name", "networkName"),
        ("mesh_unit_list", "meshUnitList"),
        ("pre_config", "preConfig"),
        ("operation_mode", "operationMode"),
        ("enable_band_steering", "enableBandSteering"),
        ("ssid", "ssid"),  # No underscores - stays the same
        ("mac", "mac"),
    ]

    for snake, expected_camel in test_cases:
        result = RequestUtils._to_camel_case(snake)
        status = "✓" if result == expected_camel else "✗"
        print(f"  {status} {snake} -> {result} (expected: {expected_camel})")
        assert result == expected_camel, f"Failed: {snake} -> {result}, expected {expected_camel}"

    print("  All basic conversions passed!\n")


def test_to_camel_case_dict():
    """Test the _to_camel_case_dict method with nested structures."""
    print("Testing _to_camel_case_dict()...")

    # Test case matching the AddNetwork request structure
    snake_dict = {
        "network_name": "TestNetwork",
        "mesh_unit_list": [
            {
                "sn": "SN123",
                "mac": "AA:BB:CC:DD:EE:FF"
            }
        ],
        "pre_config": {
            "operation_mode": "Router",
            "wireless": {
                "ssid": "MyNetwork",
                "password": "secret123",
                "enable_band_steering": True
            },
            "internet": {
                "type": "dynamic_ip"
            }
        }
    }

    expected_camel = {
        "networkName": "TestNetwork",
        "meshUnitList": [
            {
                "sn": "SN123",
                "mac": "AA:BB:CC:DD:EE:FF"
            }
        ],
        "preConfig": {
            "operationMode": "Router",
            "wireless": {
                "ssid": "MyNetwork",
                "password": "secret123",
                "enableBandSteering": True
            },
            "internet": {
                "type": "dynamicIp"
            }
        }
    }

    result = RequestUtils._to_camel_case_dict(snake_dict)

    print("  Input (snake_case):")
    print(f"    {json.dumps(snake_dict, indent=4)}")
    print("\n  Output (camelCase):")
    print(f"    {json.dumps(result, indent=4)}")
    print("\n  Expected (camelCase):")
    print(f"    {json.dumps(expected_camel, indent=4)}")

    # Verify structure
    assert result["networkName"] == "TestNetwork", "networkName mismatch"
    assert "meshUnitList" in result, "meshUnitList missing"
    assert "preConfig" in result, "preConfig missing"
    assert result["preConfig"]["operationMode"] == "Router", "operationMode mismatch"
    assert result["preConfig"]["wireless"]["enableBandSteering"] == True, "enableBandSteering mismatch"

    print("\n  ✓ Nested structure conversion passed!\n")


def test_json_serialization():
    """Test JSON serialization with dataclasses."""
    print("Testing JSON serialization with dataclasses...")

    from tauc_openapi.models.service_activation_services import (
        AddNetworkRequest, MeshUnit, PreConfig, PreConfigWireless, PreConfigInternet
    )

    # Create a sample request
    request = AddNetworkRequest(
        network_name="TestNetwork123",
        mesh_unit_list=[
            MeshUnit(sn="SN001", mac="AA:BB:CC:DD:EE:01")
        ],
        pre_config=PreConfig(
            operation_mode="Router",
            wireless=PreConfigWireless(
                ssid="TestSSID",
                password="TestPassword",
                enable_band_steering=True
            ),
            internet=PreConfigInternet(
                type="dynamic_ip"
            )
        )
    )

    # Process the request body
    body = RequestUtils.process_request_body(request.get_url(), request)

    print("  Generated JSON body:")
    if body:
        # Pretty print the JSON
        body_dict = json.loads(body)
        print(f"    {json.dumps(body_dict, indent=4)}")

        # Verify camelCase conversion
        assert "networkName" in body_dict, "networkName not found in JSON"
        assert "meshUnitList" in body_dict, "meshUnitList not found in JSON"
        assert "preConfig" in body_dict, "preConfig not found in JSON"

        if "preConfig" in body_dict and body_dict["preConfig"]:
            assert "operationMode" in body_dict["preConfig"], "operationMode not found"
            if "wireless" in body_dict["preConfig"]:
                assert "enableBandSteering" in body_dict["preConfig"]["wireless"], "enableBandSteering not found"

        print("\n  ✓ JSON serialization with camelCase conversion passed!\n")
    else:
        print("  ✗ No body generated!")
        raise AssertionError("Request body is None")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing snake_case to camelCase Conversion")
    print("=" * 60 + "\n")

    try:
        test_to_camel_case()
        test_to_camel_case_dict()
        test_json_serialization()

        print("=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe fix is working correctly. Network creation should now work.")
        return 0

    except Exception as e:
        print("=" * 60)
        print(f"✗ TEST FAILED: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
