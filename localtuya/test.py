"""
Simple platform to control LOCALLY Tuya switch devices.

Sample config yaml

switch:
  - platform: localtuya
    host: 192.168.0.1
    local_key: 1234567891234567
    device_id: 12345678912345671234
    name: tuya_01
    protocol_version: 3.3
"""
import pytuya
from time import time, sleep
from threading import Lock

REQUIREMENTS = ['pytuya==7.0.4']

CONF_DEVICE_ID = 'device_id'
CONF_LOCAL_KEY = 'local_key'
CONF_PROTOCOL_VERSION = 'protocol_version'

DEFAULT_ID = '1'
DEFAULT_PROTOCOL_VERSION = 3.3

class TuyaCache:
    """Cache wrapper for pytuya.BulbDevice"""

    def __init__(self, device):
        """Initialize the cache."""
        self._cached_status = ''
        self._cached_status_time = 0
        self._device = device
        self._lock = Lock()

    def __get_status(self, bulbid):
        for i in range(20):
            try:
                status = self._device.status()###['dps'][bulbid]
                return status
            except ConnectionError:
                if i+1 == 5:
                    raise ConnectionError("Failed to update status.")

    def set_status(self, state, bulbid):
        """Change the Tuya switch status and clear the cache."""
        self._cached_status = ''
        self._cached_status_time = 0
        for i in range(20):
            try:
                return self._device.set_status(state, bulbid)
            except ConnectionError:
                if i+1 == 5:
                    raise ConnectionError("Failed to set status.")

    def status(self, bulbid):
        """Get state of Tuya switch and cache the results."""
        self._lock.acquire()
        try:
            now = time()
            if not self._cached_status or now - self._cached_status_time > 30:
                sleep(0.5)
                self._cached_status = self.__get_status(bulbid)
                self._cached_status_time = time()
            return self._cached_status
        finally:
            self._lock.release()

    def support_color(self):
        return self._device.support_color()

    def support_color_temp(self):
        return self._device.support_color_temp()

    def brightness(self):
        return self._device.brightness()
 
    def color_temp(self):
        return self._device.colourtemp()

    def set_brightness(self, brightness):
        self._device.set_brightness(brightness)

    def set_color_temp(self, color_temp):
        self._device.set_colourtemp(color_temp)
    def state(self):
        self._device.state();
 
    def turn_on(self):
        self._device.turn_on();

    def turn_off(self):
        self._device.turn_off();


def main():
#    host: 192.168.86.88
#    local_key: 8e46c6403fb73d29
#    device_id: 17607013ecfabc48667b
    print("Started")
#   kogan 4
#   pytuyadevice = pytuya.BulbDevice('17607013ecfabc48667b','192.168.86.88','8e46c6403fb73d29')
#   kogan 1
#    pytuyadevice = pytuya.BulbDevice('17607013840d8ebb24c8','192.168.86.45','4f1b5d561aa4ec0f')
#   kogan 2
    pytuyadevice = pytuya.BulbDevice('17607013840d8ebb2438','192.168.86.52','d3c391f1abb9dbe1')
    pytuyadevice.set_version(3.3)
    bulb_device = TuyaCache(pytuyadevice)
    bulb_device.turn_on()
    bulb_device.set_brightness(1000)
    bulb_device.set_color_temp(1000)
    print("state " + str(bulb_device.state()))
    print("brightness " + str(bulb_device.brightness()))
    print("colour_temp " + str(bulb_device.color_temp()))
    bulb_device.set_brightness(1000)
    bulb_device.set_color_temp(0)
    print("state " + str(bulb_device.state()))
    print("brightness " + str(bulb_device.brightness()))
    print("colour_temp " + str(bulb_device.color_temp()))
#    bulb_device.turn_off()

if __name__ == "__main__":
    main()

