"""Tests for `sonoffdiy.SonoffDIY`."""
import asyncio

import aiohttp
import pytest
from sonoffdiy import SonoffDIY
from sonoffdiy.__version__ import __version__
from sonoffdiy.exceptions import SonoffDIYConnectionError, SonoffDIYError


@pytest.mark.asyncio
async def test_json_request(event_loop, aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        "example.com:8081",
        "/",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 0, "data": {"test": "ok"}}',
        ),
    )
    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY("example.com", session=session, loop=event_loop)
        response = await diy._request("/")
        assert response["test"] == "ok"


@pytest.mark.asyncio
async def test_encoded_json_request(event_loop, aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        "example.com:8081",
        "/",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 0, "data": "{\\"test\\": \\"ok\\"}"}',
        ),
    )
    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY("example.com", session=session, loop=event_loop)
        response = await diy._request("/")
        assert response["test"] == "ok"


@pytest.mark.asyncio
async def test_internal_session(event_loop, aresponses):
    """Test internal client session is handled correctly."""
    aresponses.add(
        "example.com:8081",
        "/",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 0, "data": {"test": "ok"}}',
        ),
    )
    async with SonoffDIY("example.com", loop=event_loop) as diy:
        response = await diy._request("/")
        assert response["test"] == "ok"


@pytest.mark.asyncio
async def test_internal_eventloop(aresponses):
    """Test internal event loop creation is handled correctly."""
    aresponses.add(
        "example.com:8081",
        "/",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 0, "data": {"test": "ok"}}',
        ),
    )
    async with SonoffDIY("example.com") as diy:
        response = await diy._request("/")
        assert response["test"] == "ok"


@pytest.mark.asyncio
async def test_request_port(event_loop, aresponses):
    """Test Sonoff DIY device running on non-standard port."""
    aresponses.add(
        "example.com:8888",
        "/",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 0, "data": {"test": "ok"}}',
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY("example.com", port=8888, session=session, loop=event_loop)
        response = await diy._request("/")
        assert response["test"] == "ok"


@pytest.mark.asyncio
async def test_request_user_agent(event_loop, aresponses):
    """Test client sending correct user agent headers."""
    # Handle to run asserts on request in
    async def response_handler(request):
        assert request.headers["User-Agent"] == f"PythonSonoffDIY/{__version__}"
        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY("example.com", session=session, loop=event_loop)
        await diy._request("/")


@pytest.mark.asyncio
async def test_request_custom_user_agent(event_loop, aresponses):
    """Test client sending correct user agent headers."""
    # Handle to run asserts on request in
    async def response_handler(request):
        assert request.headers["User-Agent"] == "LoremIpsum/1.0"
        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com",
            session=session,
            loop=event_loop,
            user_agent="LoremIpsum/1.0",
        )
        await diy._request("/")


@pytest.mark.asyncio
async def test_timeout(event_loop, aresponses):
    """Test request timeout from Sonoff DIY device."""
    # Faking a timeout by sleeping
    async def response_handler(_):
        await asyncio.sleep(2)
        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 1, "error": 0}',
        )

    aresponses.add("example.com:8081", "/", "POST", response_handler)

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY(
            "example.com", session=session, loop=event_loop, request_timeout=1
        )
        with pytest.raises(SonoffDIYConnectionError):
            assert await diy._request("/")


@pytest.mark.asyncio
async def test_invalid_content_type(event_loop, aresponses):
    """Test request timeout from Sonoff DIY device."""
    aresponses.add(
        "example.com:8081",
        "/",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "other/content"},
            text='{"seq": 26, "error": 0, "data": {"test": "ok"}}',
        ),
    )
    aresponses.add(
        "example.com:8081",
        "/",
        "POST",
        aresponses.Response(
            status=200, text='{"seq": 26, "error": 0, "data": {"test": "ok"}}',
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY("example.com", session=session, loop=event_loop)
        with pytest.raises(SonoffDIYError):
            await diy._request("/")
        with pytest.raises(SonoffDIYError):
            await diy._request("/")


@pytest.mark.asyncio
async def test_missing_error_response(event_loop, aresponses):
    """Test missing error code response from Sonoff DIY device."""
    aresponses.add(
        "example.com:8081",
        "/",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "data": {"test": "ok"}}',
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY("example.com", session=session, loop=event_loop)
        with pytest.raises(SonoffDIYError):
            await diy._request("/")


@pytest.mark.asyncio
async def test_error_response(event_loop, aresponses):
    """Test error response from Sonoff DIY device."""
    aresponses.add(
        "example.com:8081",
        "/",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"seq": 26, "error": 422}',
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY("example.com", session=session, loop=event_loop)
        with pytest.raises(SonoffDIYError):
            await diy._request("/")


@pytest.mark.asyncio
async def test_http_error(event_loop, aresponses):
    """Test HTTP error response handling."""
    aresponses.add(
        "example.com:8081",
        "/",
        "POST",
        aresponses.Response(text="OMG PUPPIES!", status=404),
    )
    aresponses.add(
        "example.com:8081",
        "/",
        "POST",
        aresponses.Response(text="OMG PUPPIES!", status=500),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        diy = SonoffDIY("example.com", session=session, loop=event_loop)
        with pytest.raises(SonoffDIYError):
            assert await diy._request("/")

        with pytest.raises(SonoffDIYError):
            assert await diy._request("/")
