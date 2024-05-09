# Laboratory access door system

System service to control access to the Laboratory door. Use supervisor for daemonize and it's resilent to usb disconnections.

Web interface: <https://github.com/rodrigodeleonv/door-access-mgm>


# TODO: PACKAGE THIS RELEASE

## Install

Simple installation script.

```bash
sudo curl -fsSL https://raw.githubusercontent.com/rodrigodeleonv/lab-door-access/main/installer.sh | bash
```

1. Install the service
1. You need to configure: `/opt/rfid/config-reader.yml`
1. Go to admin (ex <https://127.0.0.1/admin/>) search or create the API Token
1. Configure the correct URL endpoint
1. Restart the service: `sudo supervisorctl restart rfid-usb-reader`

Optional

1. Logs: `tail -f /opt/rfid/app.log`
1. Verify service: `sudo supervisorctl status`

## Development

### Configure Poetry

- [Poetry publish - One time setup](https://stackoverflow.com/a/72524326)
- [How to publish with Poetry](https://towardsdatascience.com/packages-part-2-how-to-publish-test-your-package-on-pypi-with-poetry-9fc7295df1a5)

```bash
# Poetry
#
# test PyPi
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config pypi-token.test-pypi  pypi-YYYYYYYY
poetry publish --build -r test-pypi
#
# production PyPi
poetry config pypi-token.pypi pypi-XXXXXXXX
poetry publish --build
# poetry build
rm -rf dist/*
```

### Debug

```bash

sudo $(which python) -m venv /opt/rfid-reader/env
sudo cp requirements-prod.txt /opt/rfid-reader/requirements.txt
sudo cp config-reader.yml /opt/rfid-reader/
# sudo source env/bin/activate
# sudo pip install -r requirements.txt

# How to install dependencies using test-pypi
sudo /opt/rfid-reader/env/bin/pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple lab-door-access

# Supervisor
sudo apt install supervisor -y
sudo cp usb-reader.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart rfid-usb-reader
sudo supervisorctl status

# Clean
sudo rm /etc/supervisor/conf.d/usb-reader.conf
sudo supervisorctl reread
sudo supervisorctl update
#
sudo apt remove supervisor
```

## USB RFID Redears

First, you need to identify the device. For example you have a USB RFID reader.
It's likely that your RFID reader is functioning as a keyboard emulation device (HID keyboard).

```bash
# Use one of the following commands to find device

# 1
$ ls -lh /dev/input/by-id/
total 0
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Dell_Dell_USB_Keyboard-event-kbd -> ../event5
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-event-if01 -> ../event2
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-event-if02 -> ../event4
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-event-kbd -> ../event0
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-if01-event-mouse -> ../event1
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-if01-mouse -> ../mouse0
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-if02-event-kbd -> ../event3
lrwxrwxrwx 1 root root 9 Apr  8 13:26 usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd -> ../event8  # <-- This is the Device

# 2: You need python evdev
$ python -m evdev.evtest
ID  Device               Name                                Phys                                Uniq
---------------------------------------------------------------------------------------------------------------------------------
0   /dev/input/event0    Microsoft Microsoft® Nano Transceiver v1.0 usb-0000:01:00.0-1.3/input0
1   /dev/input/event1    Microsoft Microsoft® Nano Transceiver v1.0 Mouse usb-0000:01:00.0-1.3/input1
2   /dev/input/event2    Microsoft Microsoft® Nano Transceiver v1.0 Consumer Control usb-0000:01:00.0-1.3/input1
3   /dev/input/event3    Microsoft Microsoft® Nano Transceiver v1.0 Consumer Control usb-0000:01:00.0-1.3/input2
4   /dev/input/event4    Microsoft Microsoft® Nano Transceiver v1.0 System Control usb-0000:01:00.0-1.3/input2
5   /dev/input/event5    Dell Dell USB Keyboard              usb-0000:01:00.0-1.4/input0
6   /dev/input/event6    vc4-hdmi-0                          vc4-hdmi-0/input0
7   /dev/input/event7    vc4-hdmi-1                          vc4-hdmi-1/input0
8   /dev/input/event8    Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader usb-0000:01:00.0-1.2/input0         08FF20140315  # <-- This is the Device
```
