"""Asynchronous Python client for Sonoff DIY devices."""
import asyncio
import json
import socket
from typing import Dict, Optional, Union

import aiohttp
import async_timeout
from yarl import URL

from .__version__ import __version__
from .const import ERROR_CODES, STATE_OFF, STATE_ON, STATE_RESTORE, STATE_STAY
from .exceptions import SonoffDIYConnectionError, SonoffDIYError
from .models import Info


class SonoffDIY:
    """Main class for handling connections with a Sonoff DIY device."""

    info: Optional[Info] = None

    def __init__(
        self,
        host: str,
        device_id: str = "",
        loop: asyncio.events.AbstractEventLoop = None,
        port: int = 8081,
        request_timeout: int = 3,
        session: aiohttp.client.ClientSession = None,
        user_agent: str = None,
    ) -> None:
        """Initialize connection with a Sonoff DIY device."""
        self._loop = loop
        self._session = session
        self._close_session = False

        self.device_id = device_id
        self.host = host
        self.port = port
        self.request_timeout = request_timeout
        self.user_agent = user_agent

        if user_agent is None:
            self.user_agent = f"PythonSonoffDIY/{__version__}"

    async def _request(
        self, uri: str = "", data: Optional[Dict[str, Union[int, str]]] = None,
    ) -> Optional[Dict[str, Union[bool, int, str]]]:
        """Handle a request to a Sonoff DIY device."""
        url = URL.build(
            scheme="http", host=self.host, port=self.port, path="/zeroconf/"
        ).join(URL(uri))

        if self._loop is None:
            self._loop = asyncio.get_event_loop()

        if self._session is None:
            self._session = aiohttp.ClientSession(loop=self._loop)
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    "POST",
                    url,
                    json={"deviceid": self.device_id, "data": data or {}},
                    headers={
                        "User-Agent": self.user_agent,
                        "Accept": "application/json, */*",
                    },
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise SonoffDIYConnectionError(
                "Timeout occurred while connecting to Sonoff DIY device"
            ) from exception
        except (
            aiohttp.ClientError,
            aiohttp.ClientResponseError,
            socket.gaierror,
        ) as exception:
            raise SonoffDIYConnectionError(
                "Error occurred while communicating with Sonoff DIY device"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise SonoffDIYError(
                "Unexpected response from Sonoff DIY device",
                {"Content-Type": content_type, "response": text},
            )

        response_data = await response.json()
        if "error" not in response_data:
            raise SonoffDIYError(
                "Unexpected response from Sonoff DIY device", response_data
            )

        if response_data["error"] != 0:
            error = ERROR_CODES.get(response_data["error"], "Unknown error occurred")
            raise SonoffDIYError(error, response_data)

        if "data" not in response_data:
            return None

        # itead doesn't know how JSON works apparently, so they might return
        # it packed inside the response as a serialized string.
        if isinstance(response_data["data"], str):
            return json.loads(response_data["data"])

        return response_data["data"]

    async def update_info(self) -> Optional[Info]:
        """Get all information about the Sonoff DIY device."""
        try:
            data = await self._request("info")
            signal_strength = await self._request("signal_strength")
        except SonoffDIYError as exception:
            self.info = None
            raise exception

        if data is None:
            self.info = None
            raise SonoffDIYError("Did not receive data from Sonoff DIY device")

        if signal_strength is not None:
            data.update(signal_strength)

        self.info = Info.from_dict(self.device_id, data)
        return self.info

    async def turn_on(self) -> None:
        """Turn on Sonoff DIY device."""
        await self._request("switch", {"switch": STATE_ON})

    async def turn_off(self) -> None:
        """Turn off Sonoff DIY device."""
        await self._request("switch", {"switch": STATE_OFF})

    async def pulse_on(self, pulse_width: Optional[int] = None) -> None:
        """Turn on inching on Sonoff DIY device."""
        data: Dict[str, Union[int, str]] = {"pulse": STATE_ON}
        if pulse_width is not None:
            data["pulse_width"] = pulse_width

        await self._request("pulse", data)

    async def pulse_off(self) -> None:
        """Turn off inching on Sonoff DIY device."""
        await self._request("pulse", {"pulse": STATE_OFF})

    async def pulse_width(self, pulse_width: int) -> None:
        """Set pulse width for Sonoff DIY device."""
        await self.update_info()
        pulse = STATE_ON if self.info and self.info.pulse else STATE_OFF
        await self._request("pulse", {"pulse": pulse, "pulse_width": pulse_width})

    async def wifi(self, ssid: str, password: str) -> None:
        """Set WiFi network for the Sonoff DIY device to connect to."""
        await self._request("wifi", {"ssid": ssid, "password": password})

    async def ota_unlock(self) -> None:
        """Unlock Sonoff DIY device for OTA updates."""
        await self._request("ota_unlock")

    async def ota_flash(self, url: str, sha: str) -> None:
        """OTA flash firmware to the Sonoff DIY device."""
        await self._request("ota_flash", {"downloadUrl": url, "sha256sum": sha})

    async def power_on_state(self, state: str) -> None:
        """Set state of switch when powering up."""
        if state not in (STATE_ON, STATE_OFF, STATE_RESTORE, STATE_STAY):
            raise SonoffDIYError("Invalid startup value, accepted: on, off, restore")
        # Translate restore back to stay, which is weird termonology
        if state == STATE_RESTORE:
            state = STATE_STAY
        await self._request("startup", {"startup": state})

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "SonoffDIY":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
