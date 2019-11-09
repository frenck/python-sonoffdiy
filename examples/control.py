# pylint: disable=W0621
"""Asynchronous Python client for Sonoff DIY device."""

import asyncio

from sonoffdiy import SonoffDIY


async def main(loop):
    """Show example on controlling your Sonoff DIY device."""
    async with SonoffDIY("10.10.10.197", device_id="100090bc7b", loop=loop) as diy:
        info = await diy.update_info()
        print(info)

        if not info.on:
            await diy.turn_on()
        else:
            await diy.turn_off()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
