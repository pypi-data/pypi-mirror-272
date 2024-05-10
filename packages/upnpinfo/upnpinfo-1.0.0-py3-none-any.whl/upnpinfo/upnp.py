from __future__ import annotations
import logging

from upnpclient import Device, discover


def discover_upnp_devices(timeout: int) -> list[Device]:
    """Perform a UPnP discovery of all devices on the local network."""
    # Hide the default ssdp logging. Main motivation is to hide the following:
    #   "Error 'Document is empty, line 1, column 1 ...'"
    ssdp_logger = logging.getLogger("ssdp")
    ssdp_logger.setLevel(logging.CRITICAL)

    return discover(timeout=timeout)


def get_upnp_device(location) -> Device:
    """Get a UPnP Device instance for the device at the given location."""
    return Device(location=location)


def service_actions(device: Device) -> dict:
    """Get all the actions available for all of a Device's services.

    The returned dict is keyed by service name, and the value is a list of
    action names (strings) available on that service.
    """
    service_names = []

    try:
        service_names = sorted(list(device.service_map.keys()))
    except AttributeError:
        pass

    actions = {}

    for service_name in service_names:
        actions[service_name] = [
            action.name
            for action in sorted(
                device.service_map[service_name].actions, key=lambda action: action.name
            )
        ]

    return actions


def device_summary(device: Device) -> dict:
    """Get a summary of the given UPnP device."""
    return {
        "friendly_name": device.friendly_name or None,
        "udn": device.udn or None,
        "device_type": device.device_type or None,
        "manufacturer": device.manufacturer or None,
        "manufacturer_url": device.manufacturer_url or None,
        "model_name": device.model_name or None,
        "model_number": device.model_number or None,
        "model_description": device.model_description or None,
        "location": device.location or None,
        "services": service_actions(device) or None,
    }
