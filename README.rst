****************************
Mopidy-RotaryEncoder
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-RotaryEncoder.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-RotaryEncoder/
    :alt: Latest PyPI version

Mopidy frontend extension to control the volume through a rotary encoder


Installation
============

Install by running::

    pip install Mopidy-RotaryEncoder

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-RotaryEncoder to your Mopidy configuration file::

    [rotaryencoder]
    enabled = true
    datapin = 17 #RaspberryPi GPIO BCM-Pin
    clkpin = 18 #RaspberryPi GPIO BCM-Pin
    swpin = 27 #RaspberryPi GPIO BCM-Pin

Project resources
=================

- `Source code <https://github.com/KreMat/mopidy-rotaryencoder>`_
- `Issue tracker <https://github.com/KreMat/mopidy-rotaryencoder/issues>`_


Credits
=======

- Original author: `Matthias Kreuzriegler <https://github.com/KreMat`
- Current maintainer: `Matthias Kreuzriegler <https://github.com/KreMat`
- `Contributors <https://github.com/KreMat/mopidy-rotaryencoder/graphs/contributors>`


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.
