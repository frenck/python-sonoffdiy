"""Tests for action performed against a Sonoff DIY device."""
import aiohttp
import pytest
from sonoffdiy import SonoffDIY
from sonoffdiy.const import STATE_OFF, STATE_ON, STATE_RESTORE, STATE_STAY
from sonoffdiy.exceptions import SonoffDIYError


@pytest.mark.asyncio
async def test_switch_on(event_loop, aresponses):
    """Test turning on Sonoff DIY device switch."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {"deviceid": "100090ab1a", "data": {"switch": STATE_ON}}

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/zeroconf/switch", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        await diy.turn_on()


@pytest.mark.asyncio
async def test_switch_off(event_loop, aresponses):
    """Test turning off Sonoff DIY device switch."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {"deviceid": "100090ab1a", "data": {"switch": STATE_OFF}}

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/zeroconf/switch", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        await diy.turn_off()


@pytest.mark.asyncio
async def test_pulse_on(event_loop, aresponses):
    """Test turning on Sonoff DIY device pulse mode."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {"deviceid": "100090ab1a", "data": {"pulse": STATE_ON}}

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/zeroconf/pulse", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        await diy.pulse_on()


@pytest.mark.asyncio
async def test_pulse_on_with_width(event_loop, aresponses):
    """Test turning oon Sonoff DIY device pulse mode and setting pulse width."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {
            "deviceid": "100090ab1a",
            "data": {"pulse": STATE_ON, "pulse_width": 1000},
        }

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/zeroconf/pulse", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        await diy.pulse_on(pulse_width=1000)


@pytest.mark.asyncio
async def test_pulse_off(event_loop, aresponses):
    """Test turning off Sonoff DIY device pulse mode."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {"deviceid": "100090ab1a", "data": {"pulse": STATE_OFF}}

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/zeroconf/pulse", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        await diy.pulse_off()


@pytest.mark.asyncio
async def test_pulse_width(event_loop, aresponses):
    """Test setting Sonoff DIY device pulse width."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {
            "deviceid": "100090ab1a",
            "data": {"pulse": STATE_ON, "pulse_width": 1000},
        }

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add(
        "example.com:8081",
        "/zeroconf/info",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 0, "data": {"pulse": "on"}}',
        ),
    )

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

    aresponses.add("example.com:8081", "/zeroconf/pulse", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        await diy.pulse_width(1000)


@pytest.mark.asyncio
async def test_wifi(event_loop, aresponses):
    """Test setting Sonoff DIY device WiFi settings."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {
            "deviceid": "100090ab1a",
            "data": {"ssid": "frenck", "password": "choochoo"},
        }

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/zeroconf/wifi", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        await diy.wifi("frenck", "choochoo")


@pytest.mark.asyncio
async def test_ota_unlock(event_loop, aresponses):
    """Test unlocking Sonoff DIY device OTA."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {"deviceid": "100090ab1a", "data": {}}

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/zeroconf/ota_unlock", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        await diy.ota_unlock()


@pytest.mark.asyncio
async def test_ota_flash(event_loop, aresponses):
    """Test flashing Sonoff DIY device."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {
            "deviceid": "100090ab1a",
            "data": {
                "downloadUrl": "https://frenck.dev",
                "sha256sum": "1d869a86cd206fc09aaa",
            },
        }

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/zeroconf/ota_flash", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        await diy.ota_flash(
            "https://frenck.dev", "1d869a86cd206fc09aaa",
        )


@pytest.mark.asyncio
async def test_power_on_state(event_loop, aresponses):
    """Test setting Sonoff DIY device power on state."""
    # Handle to run asserts on request in
    async def response_handler(request):
        data = await request.json()
        assert data == {
            "deviceid": "100090ab1a",
            "data": {"startup": STATE_STAY},
        }

        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/zeroconf/startup", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        await diy.power_on_state(STATE_RESTORE)


@pytest.mark.asyncio
async def test_power_on_state_invalid(event_loop):
    """Test setting invalid power on state."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", device_id="100090ab1a", session=session, loop=event_loop,
        )
        with pytest.raises(SonoffDIYError):
            await diy.power_on_state("frenck")
