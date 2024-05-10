import json
from urllib.parse import urlparse

import click
from rich.columns import Columns
from rich.console import Console
from rich.table import box, Table
from rich.text import Text
from rich.traceback import install

from upnpinfo import (
    device_summary,
    discover_upnp_devices,
    get_upnp_device,
    service_actions,
)


install(suppress=[click])


@click.command()
@click.option(
    "--timeout",
    "-t",
    help="UPnP discovery timeout (seconds).",
    metavar="SECS",
    type=click.INT,
    default=1,
    show_default=True,
)
@click.option(
    "--device",
    "-d",
    help="Device name, UDN, or UPnP location URL.",
    metavar="DEVICE",
    type=click.STRING,
)
@click.option(
    "--no-color",
    help="Disable color.",
    is_flag=True,
    default=False,
)
@click.option(
    "--json",
    "as_json",
    help="Display results as JSON.",
    is_flag=True,
    default=False,
)
def cli(timeout, device, no_color, as_json):
    """
    Retrieves UPnP device information from the local network.

    Defaults to showing a summary of all devices found on the local network
    using UPnP discovery. Use --device to retrieve detailed information on a
    specific device.
    """
    console = Console(no_color=no_color, highlight=not no_color)

    if device:
        handle_show_single_device(console, device, timeout, no_color, as_json)
    else:
        handle_show_all_devices(console, timeout, no_color, as_json)


def handle_show_all_devices(console, timeout, plain_output, as_json):
    """Discover UPnP devices on the local network and display a summary."""
    with console.status("Discovering UPnP devices..."):
        devices = discover_upnp_devices(timeout=timeout)

    unique_devices = []  # Remove duplicate devices (based on UDN)
    device_udns = []

    for device in devices:
        # if device.udn not in device_udns:
        if device.udn not in device_udns:
            unique_devices.append(device)
            device_udns.append(device.udn)

    if len(unique_devices) <= 0:
        console.print("No UPnP devices found.")

        return

    # Create a list of unique device information summary dicts
    device_summaries = []

    for device in unique_devices:
        device_summaries.append(device_summary(device))

    if as_json:
        # Dump the device summaries as JSON
        console.print(json.dumps(device_summaries, indent=4))
    else:
        # Display a table of unique device information summaries
        table = Table(
            show_header=True,
            header_style=None if plain_output else "bold",
            box=box.SIMPLE_HEAD,
            pad_edge=False,
        )

        table.add_column("Name", no_wrap=True)
        table.add_column("Manufacturer")
        table.add_column("Description")
        table.add_column("Model")
        table.add_column("Type")
        table.add_column("Address")

        for device in sorted(
            device_summaries, key=lambda device: device["friendly_name"].lower()
        ):
            # Extract just the hostname from the full location URL
            parsed_location = urlparse(device["location"])
            address = parsed_location.hostname

            # Extract just the device type name from the full device type
            # e.g. urn:schemas-upnp-org:device:MediaRenderer:1 -> MediaRenderer
            device_type = device["device_type"]

            try:
                device_type = device_type.split(":")[3]
            except IndexError:
                pass

            table.add_row(
                device["friendly_name"] or "-",
                device["manufacturer"] or "-",
                device["model_description"] or "-",
                device["model_name"] or "-",
                device_type or "-",
                address or "-",
            )

        # Display the table and a footer message showing how to get detailed
        # info on a device

        script_name = click.get_current_context().info_name

        console.print(
            table,
            Text(f"Run \"{script_name} --device '<name>'\" to view device details.\n"),
        )


def handle_show_single_device(console, device_input, timeout, plain_output, as_json):
    """Display detailed information on a single UPnP device."""
    # Check if the input is a URL. If it's not then we assume it's a device
    # name and attempt to find that name in the list of all discovered devices.
    device_input_as_url = urlparse(device_input)

    if device_input_as_url.hostname is None:
        # See if the device input was a device name or a UDN
        with console.status(f"Finding device: {device_input} ..."):
            all_devices = discover_upnp_devices(timeout=timeout)

        try:
            location = [
                device
                for device in all_devices
                if device.friendly_name == device_input or device.udn == device_input
            ][0].location
        except (IndexError, AttributeError):
            console.print(f"UPnP device not found: {device_input}")

            return
    else:
        # Device input was a URL
        location = device_input

    try:
        # Get device details from the device URL
        with console.status(f"Retrieving details for device: {device_input} ..."):
            device = get_upnp_device(location)
    except Exception as e:
        console.print(e)

        return

    actions = service_actions(device)

    if as_json:
        # Dump the device details as JSON
        console.print(json.dumps(device_summary(device), indent=4))
    else:
        # Prepare a table of device details
        details_table = Table(
            show_header=False,
            box=box.SIMPLE_HEAD,
            padding=0,
            pad_edge=False,
        )

        details_table.add_column("Field", justify="right")
        details_table.add_column(
            "Value", justify="left", style=None if plain_output else "bold"
        )

        details_table.add_row("Friendly name:", device.friendly_name or "-")
        details_table.add_row("UDN:", device.udn or "-")
        details_table.add_row("Device type:", device.device_type or "-")
        details_table.add_row("Manufacturer:", device.manufacturer or "-")
        details_table.add_row("Manufacturer URL:", device.manufacturer_url or "-")
        details_table.add_row("Model name:", device.model_name or "-")
        details_table.add_row("Model number:", device.model_number or "-")
        details_table.add_row("Model description:", device.model_description or "-")
        details_table.add_row("Location:", device.location or "-")
        details_table.add_row("Services:", ", ".join(sorted(actions.keys())) or "-")

        # Prepare columns showing the actions available for each service
        service_columns = []

        for service_name in actions.keys():
            service_table = Table(
                show_header=True,
                header_style=None if plain_output else "bold",
                box=box.SIMPLE_HEAD,
                pad_edge=False,
            )

            service_table.add_column(service_name)

            for service_action in actions[service_name]:
                service_table.add_row(service_action)

            service_columns.append(service_table)

        # Display the details table and (if present) the service action tables
        if len(service_columns) > 0:
            console.print(
                details_table, Text(" Service actions:"), Columns(service_columns)
            )
        else:
            console.print(details_table)


if __name__ == "__main__":
    cli()
