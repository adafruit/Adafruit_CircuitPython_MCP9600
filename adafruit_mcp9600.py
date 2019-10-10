# The MIT License (MIT)
#
# Copyright (c) 2019 Dan Cogliano for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_mcp9600`
================================================================================

CircuitPython driver for the MCP9600 thermocouple I2C amplifier


* Author(s): Dan Cogliano

Implementation Notes
--------------------

**Hardware:**

* Adafruit MCP9600 I2C Thermocouple Amplifier:
  https://www.adafruit.com/product/4101

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP9600.git"
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

_DEFAULT_ADDRESS = const(0x67)

_REGISTER_HOT_JUNCTION = const(0x00)
_REGISTER_DELTA_TEMP = const(0x01)
_REGISTER_COLD_JUNCTION = const(0x02)
_REGISTER_THERM_CFG = const(0x05)
_REGISTER_VERSION = const(0x20)

class MCP9600():
    """Interface to the MCP9600 thermocouple amplifier breakout"""

    def __init__(self, i2c, address=_DEFAULT_ADDRESS, tctype="K", tcfilter=0):
        types = ["K", "J", "T", "N", "S", "E", "B", "R"]
        self.buf = bytearray(3)
        self.i2c_device = I2CDevice(i2c, address)
        self.type = tctype
        # is this a valid thermocouple type?
        if tctype not in types:
            raise Exception("invalid thermocouple type ({})".format(tctype))
        # filter is from 0 (none) to 7 (max), can limit spikes in
        # temperature readings
        tcfilter = min(7, max(0, tcfilter))
        ttype = 0  # default is Type K
        if tctype == "J":
            ttype = 0x01
        elif tctype == "T":
            ttype = 0x02
        elif tctype == "N":
            ttype = 0x03
        elif tctype == "S":
            ttype = 0x04
        elif tctype == "E":
            ttype = 0x05
        elif tctype == "B":
            ttype = 0x06
        elif tctype == "R":
            ttype = 0x07

        self.buf[0] = _REGISTER_THERM_CFG
        self.buf[1] = tcfilter | (ttype << 4)
        with self.i2c_device as tci2c:
            tci2c.write(self.buf, end=2)

    @property
    def version(self):
        """ MCP9600 chip version """
        version = self._read_register(_REGISTER_VERSION, 1)
        return version

    @property
    def ambient_temperature(self):
        """ Cold junction/ambient/room temperature in Celsius """
        data = self._read_register(_REGISTER_COLD_JUNCTION, 2)
        if data[0] & 0xf0:
            # negative temperature
            value = data[0]*16.0 + data[1]/16.0 - 4096
        else:
            # positive temperature
            value = data[0]*16.0 + data[1]/16.0
        return value

    @property
    def hot_junction_temperature(self):
        """ Hot junction temperature in Celsius """
        data = self._read_register(_REGISTER_HOT_JUNCTION, 2)
        if data[0] & 0x80:
            # negative temperature
            value = data[0]*16.0 + data[1]/16.0 - 4096
        else:
            # positive temperature
            value = data[0]*16.0 + data[1]/16.0
        return value

    @property
    def delta_temperature(self):
        """ Delta temperature in Celsius """
        data = self._read_register(_REGISTER_DELTA_TEMP, 2)
        if data[0] & 0x80:
            # negative temperature
            value = data[0]*16.0 + data[1]/16.0 - 4096
        else:
            # positive temperature
            value = data[0]*16.0 + data[1]/16.0
        return value

    def _read_register(self, reg, count=1):
        # pylint: disable=no-else-return
        self.buf[0] = reg
        with self.i2c_device as i2c:
            i2c.write_then_readinto(
                self.buf,
                self.buf,
                out_end=count,
                in_start=1
            )
        if count == 1:
            return self.buf[1]
        elif count == 2:
            return self.buf[1], self.buf[2]
        return None
