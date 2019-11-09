"""Models for Sonoff DIY devices."""

import attr

from .const import STATE_OFF, STATE_ON, STATE_RESTORE, STATE_STAY


@attr.s(auto_attribs=True, frozen=True)
class Info:
    """Object holding information and states of the Sonoff DIY device."""

    device_id: str
    on: bool
    ota_unlock: bool
    power_on_state: str
    pulse_width: int
    pulse: bool
    signal_strength_percentage: int
    signal_strength: int
    ssid: str

    @staticmethod
    def from_dict(device_id: str, data: dict):
        """Return device object from Sonoff DIY API response."""

        signal_strength = data.get("signalStrength", -100)
        if signal_strength <= -100:
            signal_strength_percentage = 0
        elif signal_strength >= -50:
            signal_strength_percentage = 100
        else:
            signal_strength_percentage = 2 * (signal_strength + 100)

        power_on_state = data.get("startup", STATE_OFF)
        if power_on_state == STATE_STAY:
            power_on_state = STATE_RESTORE

        return Info(
            device_id=device_id,
            on=data.get("switch") == STATE_ON,
            ota_unlock=data.get("otaUnlock", False),
            power_on_state=power_on_state,
            pulse_width=data.get("pulseWidth", 0),
            pulse=data.get("pulse") == STATE_ON,
            signal_strength_percentage=signal_strength_percentage,
            signal_strength=signal_strength,
            ssid=data.get("ssid", ""),
        )
