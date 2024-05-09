from json.decoder import JSONDecodeError
import logging

from evdev import InputDevice, categorize, ecodes
from evdev.events import InputEvent  # , KeyEvent
import requests

logger = logging.getLogger(__name__)


def handle_key_press(data: InputEvent) -> str:
    """Converts data.scancode to a digit.

    Digits: 0-9

    Args:
        data: InputEvent object representing a key press event.

    Returns:
        The last digit of the scancode.
    """
    digit = (data.scancode - 1) % 10
    return str(digit)


def send_post_request(
    session: requests.Session,
    url: str,
    tag_id: str,
    timeout: int = 5,
    ssl_verify: bool = False,
) -> dict:
    """Sends a POST request to the URL with the tag ID.

    Args:
        session: The requests.Session object.
        url: The URL to send the POST request.
        tag_id: The tag ID to send in the request body.
        ssl_verify: Whether to verify the SSL certificate.
            False allows to use self cert in local/internal network.

    Returns:
        A dictionary containing the` response data` and `status code`.
    """

    body = {"tag_id": tag_id}
    data = {"status_code": None, "response": None}
    try:
        response = session.post(url, json=body, timeout=timeout, verify=ssl_verify)
    except requests.exceptions.RequestException:
        logger.exception("Failed to send POST request")
        return
    else:
        data["status_code"] = response.status_code
    try:
        data["response"] = response.json()
    except JSONDecodeError:
        logger.exception("Error parsing response")
        return
    return data


def main_loop(reader: InputDevice, url: str, api_token: str, api_auth_scheme: str):
    """Main loop of the RFID reader.

    Args:
        reader: InputDevice object representing the RFID reader.
        url: The URL to send the POST request.
        api_token: The API token to send in the request headers.
        api_auth_scheme: The API authentication scheme to send in the request headers.
            example: Token (Basic, Bearer not supported)
    """
    rfid_tag = ""
    headers = {"Authorization": f"{api_auth_scheme} {api_token}"}
    session = requests.Session()
    session.headers.update(headers)
    logger.info(f"Listening for RFID scans on device: {reader.path}")

    # event: KeyEvent
    for event in reader.read_loop():
        if event.type != ecodes.EV_KEY:
            # logger.debug(f"Skipping non-key event: {event}")
            continue

        data: InputEvent = categorize(event)

        if data.keystate != 1:
            # logger.debug(f"Skipping non-press event: {data}")
            continue

        if 2 <= data.scancode <= 11:
            rfid_tag += handle_key_press(data)
        elif data.scancode == 28:
            logger.info(f"RFID Tag ID: {rfid_tag}")
            logger.info("Sending POST request")
            response_data = send_post_request(session, url, rfid_tag)
            logger.info(f"Response: {response_data}")
            rfid_tag = ""
