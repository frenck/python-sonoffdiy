"""Exceptions for Sonoff DIY devices."""


class SonoffDIYError(Exception):
    """Generic Sonoff DIY exception."""

    pass


class SonoffDIYConnectionError(SonoffDIYError):
    """Sonoff DIY connection exception."""

    pass
