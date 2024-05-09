import logging
import evdev

logger = logging.getLogger(__name__)


class DeviceInputError(Exception):
    pass


class DeviceInputNotFound(DeviceInputError):
    pass


def find_rfid_reader(device_name: str) -> evdev.InputDevice:
    """Attempt to locate an RFID reader device by a known identifier in its name.

    When input device is found then returns something like /dev/input/event8.

    Args:
        device_name: the exact name of the device.
            Use `ls /dev/input/by-id/` or `python -m evdev.evtest`.
            Example "Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader"

    Returns:
        RFID reader path of the input device or empty string if not found.

    Raises:
        DeviceInputNotFound:
    """
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        logger.debug(f"Checking device name: {device.name}, Path: {device.path}")
        if device_name in device.name:
            return device
    raise DeviceInputNotFound


if __name__ == "__main__":
    device_name = "Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader"
    rfid_reader_path = find_rfid_reader(device_name)

    if rfid_reader_path:
        # Use the found RFID reader path for further processing
        print(f"RFID Reader Path: {rfid_reader_path}")
    else:
        print("No RFID reader detected.")
