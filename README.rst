Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-mcp9600/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/mcp9600/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_MCP9600/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_MCP9600/actions/
    :alt: Build Status

This is a CircuitPython driver for the MCP9600 thermocouple I2C amplifier.
In addition to the MCP9600 breakout, you will also need a thermocouple, which
can be found in the Adafruit store.
The MCP9600 supports several thermocouple types for different temperature
ranges. The "K" type is the default, with a range of -200C to +1372C.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-mcp9600/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-mcp9600

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-mcp9600

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-mcp9600

Usage Example
=============

This is a simple example showing the hot junction temperature (the
temperature at the tip of the thermocouple). You may need to adjust the
I2C frequency if you receive input/output errors.

.. code-block:: shell

    import board
    import busio
    from adafruit_bus_device.i2c_device import I2CDevice
    from adafruit_mcp9600 import MCP9600

    i2c = busio.I2C(board.SCL, board.SDA,frequency=200000)
    try:
        # using default I2C register and "K" thermocouple
        device = MCP9600(i2c)
        print("temperature(C):",device.temperature)
    except ValueError:
        print("MCP9600 sensor not detected")

This example displays the ambient/room and hot junction temperatures at
1 second intervals. Turn on the Mu editor's plotter option to view the
temperatures in a real-time graph.

.. code-block:: shell

    import board
    import busio
    import time
    from adafruit_bus_device.i2c_device import I2CDevice
    from adafruit_mcp9600 import MCP9600

    i2c = busio.I2C(board.SCL, board.SDA, frequency=200000)

    try:
        device = MCP9600(i2c)
        print("version:", device.version)
        while True:
            print((
                device.ambient_temperature,
                device.temperature
            ))
            time.sleep(1)
    except ValueError:
        print("MCP9600 sensor not detected")


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/mcp9600/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_MCP9600/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
