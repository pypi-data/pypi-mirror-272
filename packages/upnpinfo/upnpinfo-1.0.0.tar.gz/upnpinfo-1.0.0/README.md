# upnpinfo

`upnpinfo` is a commandline tool for retrieving UPnP device information from the local network.
It's a simple CLI wrapper around [upnpclient](https://github.com/flyte/upnpclient).

## Installation

`upnpinfo` requires Python 3.8 or higher.

```sh
pip install upnpinfo
```

## Features

### Discover UPnP devices

By default, `upnpclient` will perform UPnP discovery on the local network and display a summary
table showing all discovered devices.

![Discovery](https://github.com/mjoblin/upnpinfo/raw/main/media/upnpinfo_discovery.png)

### Display detailed information on a single device

Use the `--device` flag to view detailed information on a single device, including the device's
services and actions. The provided device can be a UPnP friendly name, a unique UDN, or a UPnP
location URL.

![Device](https://github.com/mjoblin/upnpinfo/raw/main/media/upnpinfo_device.png)

### JSON output

Output can be optionally generated in JSON format.

![JSON output](https://github.com/mjoblin/upnpinfo/raw/main/media/upnpinfo_json.png)

### Help information

The following flags are supported.

![Help](https://github.com/mjoblin/upnpinfo/raw/main/media/upnpinfo_help.png)

## Ideas

It would be cool if `upnpinfo` had an interactive mode, allowing for browsing of devices and
device services, and supporting manual action invocation.