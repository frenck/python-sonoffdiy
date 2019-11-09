"""Models for Sonoff DIY devices."""

ERROR_CODES = {
    400: "Request body is not valid JSON",
    401: "Unauthorized request",
    403: "OTA function is locked",
    404: "Device does not support requested Device ID",
    408: "Timeout while downloading firmware",
    413: "OTA firmware exceeds device allowed size limit",
    422: "Invalid request parameters",
    424: "Firmware download failed",
    471: "Firmware integrity check failed",
    500: "Device ID or API key is not authorized by vendor's OTA service",
    503: "Could not connect to vendor's OTA unlock service",
}

STATE_OFF = "off"
STATE_ON = "on"
STATE_RESTORE = "restore"
STATE_STAY = "stay"
