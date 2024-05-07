import json
from typing import Optional

from duwi_smart_sdk.util.sign import md5_encrypt
from duwi_smart_sdk.util.timestamp import current_timestamp
from duwi_smart_sdk.const.const import URL
from duwi_smart_sdk.util.http import post
from duwi_smart_sdk.model.req.device_control import ControlDevice


class ControlClient:
    """
    Client for controlling devices through the Duwi's cloud service.
    """

    def __init__(self,
                 app_key: str,
                 app_secret: str,
                 access_token: str,
                 app_version: str,
                 client_version: str,
                 client_model: str = None
                 ):
        """
        Initializes the control client with the necessary authentication details.

        :param app_key: The application key for SDK authentication.
        :param app_secret: The application secret for SDK authentication.
        :param access_token: The access token for interacting with the cloud service.
        """
        self._url = URL
        self._app_key = app_key
        self._app_secret = app_secret
        self._access_token = access_token
        self._app_version = app_version
        self._client_version = client_version
        self._client_model = client_model

    async def control(self, body: Optional[ControlDevice]) -> str:
        """
        Sends a device control command to the cloud service.

        :param body: Optional, an instance of ControlDevice containing the command details.
        :return: The status of the operation as a string.
        """
        # Convert the body to a JSON string, minimizing spaces.
        body_string = json.dumps(body.to_dict(), separators=(',', ':')) if body else ""

        # Generate a signature using the body string, app secret, and the current timestamp.
        sign = md5_encrypt(f"{body_string}{self._app_secret}{current_timestamp()}")

        # Prepare the request headers.
        headers = {
            'Content-Type': 'application/json',
            'accessToken': self._access_token,
            'appkey': self._app_key,
            'secret': self._app_secret,
            'time': str(current_timestamp()),  # Ensure it's converted to string
            'sign': sign,
            'appVersion': self._app_version,
            'clientVersion': self._client_version,
            'clientModel': self._client_model
        }

        # Convert the body to a dictionary if it's not None, else set as None.
        body_dict = body.to_dict() if body else None

        # Send the control command using the POST method.
        status, message, res = await post(f"{self._url}/device/batchCommandOperate", headers, body_dict)

        return status
