# Python: Asynchronous client for Sonoff DIY devices

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE.md)

[![Build Status][build-shield]][build]
[![Code Coverage][codecov-shield]][codecov]
[![Code Quality][code-quality-shield]][code-quality]

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

[![Support my work on Patreon][patreon-shield]][patreon]

Asynchronous Python client for Sonoff DIY devices.

## About

This package allows you to control and monitor Sonoff DIY devices
programmatically. It is mainly created to allow third-party programs to automate
the behavior of a Sonoff DIY device.

An excellent example of this might be Home Assistant, which allows you to write
automations, to turn on parental controls when the kids get home.

## Installation

```bash
pip install sonoffdiy
```

## Usage

```python
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
```

## Changelog & Releases

This repository keeps a change log using [GitHub's releases][releases]
functionality. The format of the log is based on
[Keep a Changelog][keepchangelog].

Releases are based on [Semantic Versioning][semver], and use the format
of ``MAJOR.MINOR.PATCH``. In a nutshell, the version will be incremented
based on the following:

- ``MAJOR``: Incompatible or major changes.
- ``MINOR``: Backwards-compatible new features and enhancements.
- ``PATCH``: Backwards-compatible bugfixes and package updates.

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

In case you'd like to contribute, a `Makefile` has been included to ensure a
quick start.

```bash
make venv
source ./venv/bin/activate
make dev
```

Now you can start developing, run `make` without arguments to get an overview
of all make goals that are available (including description):

```bash
$ make
Asynchronous Python client for Sonoff DIY devices.

Usage:
  make help                            Shows this message.
  make dev                             Set up a development environment.
  make lint                            Run all linters.
  make lint-black                      Run linting using black & blacken-docs.
  make lint-flake8                     Run linting using flake8 (pycodestyle/pydocstyle).
  make lint-pylint                     Run linting using PyLint.
  make lint-mypy                       Run linting using MyPy.
  make test                            Run tests quickly with the default Python.
  make coverage                        Check code coverage quickly with the default Python.
  make install                         Install the package to the active Python's site-packages.
  make clean                           Removes build, test, coverage and Python artifacts.
  make clean-all                       Removes all venv, build, test, coverage and Python artifacts.
  make clean-build                     Removes build artifacts.
  make clean-pyc                       Removes Python file artifacts.
  make clean-test                      Removes test and coverage artifacts.
  make clean-venv                      Removes Python virtual environment artifacts.
  make dist                            Builds source and wheel package.
  make release                         Release build on PyP
  make tox                             Run tests on every Python version with tox.
  make venv                            Create Python venv environment.
```

## Authors & contributors

The original setup of this repository is by [Franck Nijhof][frenck].

For a full list of all authors and contributors,
check [the contributor's page][contributors].

## License

MIT License

Copyright (c) 2019 Franck Nijhof

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[build-shield]: https://github.com/frenck/python-sonoffdiy/workflows/Continuous%20Integration/badge.svg
[build]: https://github.com/frenck/python-sonoffdiy/actions
[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/frenck
[code-quality-shield]: https://img.shields.io/lgtm/grade/python/g/frenck/python-sonoffdiy.svg?logo=lgtm&logoWidth=18
[code-quality]: https://lgtm.com/projects/g/frenck/python-sonoffdiy/context:python
[codecov-shield]: https://codecov.io/gh/frenck/python-sonoffdiy/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/frenck/python-sonoffdiy
[contributors]: https://github.com/frenck/python-sonoffdiy/graphs/contributors
[frenck]: https://github.com/frenck
[keepchangelog]: http://keepachangelog.com/en/1.0.0/
[license-shield]: https://img.shields.io/github/license/frenck/python-sonoffdiy.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2019.svg
[patreon-shield]: https://www.frenck.nl/images/patreon.png
[patreon]: https://www.patreon.com/frenck
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[releases-shield]: https://img.shields.io/github/release/frenck/python-sonoffdiy.svg
[releases]: https://github.com/frenck/python-sonoffdiy/releases
[semver]: http://semver.org/spec/v2.0.0.html
