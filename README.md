# vboxpower

VirtualBox Power Driver for MAAS (Metal as a Service)

A way to manage the power of VirtualBox virtual machines via the MAAS webhook driver.

## What is MAAS?

MAAS (Metal as a Service) is a tool to turns real servers into bare-metal cloud. With MAAS, you can automate server provisioning and installing OS remotely on both physical and virtual servers. [MAAS.io](https://maas.io/) for more information.

## What is vboxpower?

`vboxpower` is a wrapper to enabling MAAS to manage VirtualBox virtual machines power directly. As you know, MAAS does not natively support VirtualBox power management. Before vboxpower, you had to use `manual` power type for VirtualBox machines, the process of starting/stopping virtual machines did manually but with vboxpower this process is done automatically. So to speak, the prophecy of the vboxpower is translating power commands between VirtualBox and MAAS.

## How to install vboxpower:

Both MAAS and vboxpower are written in Python language. So, you don't need another language to run vboxpower.

### Prerequisites:

  1. VirtualBox 6+ installed and running.
  2. VirtualBox SDK https://www.virtualbox.org/wiki/Downloads
  3. VirtualBox Extension Pack to support PXE boot.

### VirtualBox SDK installation tips:

Download and extract VirtualBox SDK and run the following command.

```bash
sudo VBOX_INSTALL_PATH=/usr/lib/virtualbox python vboxapisetup.py install
```

### Get started:

To deploy vboxpower, you need `python3-pip` to install the required packages.

The deploy script creates systemd service and copies `vboxpower.py` to `/opt/maas/vboxpower` directory.

After deployment, the deploy script starts the vboxpower service.

```bash
sudo apt update && apt install -y python3-pip
sudo ./start
```

### Test vboxpower:

The vboxpower is listening on port 5241/tcp on all interfaces.

You should be able to see the list of available VirtualBox virtual machines with `curl` command.

```bash
curl 192.168.56.1:5241
{
  "machines": [
    {
      "links": {
        "off": "/pfsense/off",
        "on": "/pfsense/on",
        "status": "/pfsense/status"
      },
      "name": "pfsense",
      "status": "running"
    },
    {
      "links": {
        "off": "/maas/off",
        "on": "/maas/on",
        "status": "/maas/status"
      },
      "name": "maas",
      "status": "running"
    }
  ]
}
```

### Integration with MAAS:

Each virtual machine exposes three endpoints that are used for vm power management.

  - http://**HOST_IP**:5241/**VM_NAME**/on
  - http://**HOST_IP**:5241/**VM_NAME**/off
  - http://**HOST_IP**:5241/**VM_NAME**/status

Use these endpoints on MAAS Webhook power URI, respectively.

I have tested the process on Ubuntu 20.04, MAAS 3.0, and VirtualBox 6.1.16 completely.

Other versions should be work without problem.

![demo](https://raw.githubusercontent.com/ssbostan/vboxpower/master/demo.gif)

## How to contribute:

All contributions are welcomed. If you find any bugs, please file an issue.

Copyright 2021 Saeid Bostandoust <ssbostan@linuxmail.org>
