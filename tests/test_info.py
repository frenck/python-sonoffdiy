"""Tests for retreiving information from Sonoff DIY device."""
import aiohttp
import pytest
from sonoffdiy import SonoffDIY
from sonoffdiy.const import STATE_RESTORE
from sonoffdiy.exceptions import SonoffDIYError


@pytest.mark.asyncio
async def test_info_update(event_loop, aresponses):
    """Test getting Sonoff DIY device information and states."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {"deviceid": "100090ab1a", "data": {}}

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=str(
                '{"seq": 6,"error": 0,"data": '
                '"{\\"switch\\":\\"on\\",\\"startup\\":\\"stay\\",'
                '\\"pulse\\":\\"off\\",\\"pulseWidth\\":1500,'
                '\\"ssid\\":\\"frenck\\",\\"otaUnlock\\":true}"}',
            ),
        )

    aresponses.add("example.com:8081", "/zeroconf/info", "POST", response_handler)

    aresponses.add(
        "example.com:8081",
        "/zeroconf/signal_strength",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 0, "data": {"signalStrength": -48}}',
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        info = await diy.update_info()
        assert info
        assert info.on
        assert info.power_on_state == STATE_RESTORE
        assert not info.pulse
        assert info.pulse_width == 1500
        assert info.ssid == "frenck"
        assert info.ota_unlock
        assert info.signal_strength == -48
        assert info.signal_strength_percentage == 100


@pytest.mark.asyncio
async def test_signal_strength(event_loop, aresponses):
    """Test retreiving Sonoff DIY device WiFi signal strength."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {"deviceid": "100090ab1a", "data": {}}

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 6,"error": 0,"data": {}}',
        )

    aresponses.add("example.com:8081", "/zeroconf/info", "POST", response_handler)

    aresponses.add(
        "example.com:8081",
        "/zeroconf/signal_strength",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 0, "data": {"signalStrength": -60}}',
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        info = await diy.update_info()
        assert info
        assert info.signal_strength == -60
        assert info.signal_strength_percentage == 80


@pytest.mark.asyncio
async def test_signal_strength_0(event_loop, aresponses):
    """Test retreiving Sonoff DIY device WiFi signal strength with -100 dB."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {"deviceid": "100090ab1a", "data": {}}

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 6,"error": 0,"data": {}}',
        )

    aresponses.add("example.com:8081", "/zeroconf/info", "POST", response_handler)

    aresponses.add(
        "example.com:8081",
        "/zeroconf/signal_strength",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 0, "data": {"signalStrength": -100}}',
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        info = await diy.update_info()
        assert info
        assert info.signal_strength == -100
        assert info.signal_strength_percentage == 0


@pytest.mark.asyncio
async def test_no_data(event_loop, aresponses):
    """Test error is raised when info data is missing from API call."""
    # Handle to run asserts on request in
    aresponses.add(
        "example.com:8081",
        "/zeroconf/info",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 6,"error": 0}',
        ),
    )

    aresponses.add(
        "example.com:8081",
        "/zeroconf/signal_strength",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 0, "data": {"signalStrength": -100}}',
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        with pytest.raises(SonoffDIYError):
            await diy.update_info()


@pytest.mark.asyncio
async def test_info_none(event_loop, aresponses):
    """Test info data is None when communication has occured."""
    # Handle to run asserts on request in
    aresponses.add(
        "example.com:8081",
        "/zeroconf/info",
        "POST",
        aresponses.Response(
            status=500,
            headers={"Content-Type": "application/json"},
            text="Invalid response",
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        with pytest.raises(SonoffDIYError):
            await diy.update_info()
        assert diy.info is None
