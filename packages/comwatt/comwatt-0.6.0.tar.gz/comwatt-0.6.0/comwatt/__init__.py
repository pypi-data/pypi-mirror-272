import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait


DEVICES_TYPES = [
    "injection",
    "withdrawal",
    "sun",
    "hotwatertank",
    "plug"
]


URL_LOGIN = "https://energy.comwatt.com/#/login/"


class LoginError(Exception):
    pass


class Zone(object):

    def __init__(self, title):

        self.title = title
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)
        device.zone = self

    def __repr__(self):
        return str({"title" : self.title})


class Device(object):

    def __init__(self, type):
        
        self.type = type
        self.zone = None
        self.value_instant = 0
        self.initialized = False


class PowerGEN4(webdriver.Firefox):

    def __init__(self, email, password, debug = False):

        options = Options()

        if not debug:
            options.add_argument("-headless")

        super().__init__(options=options)
    
        self.zones = []

        self.default_site = None

        self.email = email
        self.password = password

        self.login()

        self.last_refresh_time = 0

    def login(self):

        # Get the login page
        super().get('https://energy.comwatt.com/#/login/')

        WebDriverWait(self, timeout=20).until(lambda d: d.find_element(By.NAME, 'email'))

        # Enter email and password
        elem = self.find_element(By.NAME, 'email')  # Find the search box
        elem.send_keys(self.email + Keys.RETURN)

        elem = self.find_element(By.NAME, 'password')  # Find the search box
        elem.send_keys(self.password + Keys.RETURN)

        # Wait for next page
        for i in range(20):
            if self.current_url != URL_LOGIN:
               break
            time.sleep(1)

        # Still on the login page -> login error
        if self.current_url == URL_LOGIN:
            raise LoginError

        # Wait home page
        WebDriverWait(self, timeout=20).until(lambda d: d.find_element(By.CLASS_NAME, 'css-3kduam'))

        m = re.match("https://energy.comwatt.com/#/sites/([abcdef0123456789]+)/home", self.current_url)
        
        self.default_site = m.group(1)

    def get(self, url, title=None):
        
        # First try
        super().get(url)

        # Back to login page -> retry logins
        if self.current_url == URL_LOGIN:
            self.login()

            # Second try
            super().get(url)

    def meter(self, site=None):

        if not site:
            site = self.default_site

        self.get('https://energy.comwatt.com/#/sites/%s/meter/' % site)
        WebDriverWait(self, timeout=20).until(lambda d: d.find_element(By.CLASS_NAME, 'css-3kduam'))

        elem = self.find_element(By.CLASS_NAME, 'css-3kduam')

        data = elem.text
        assert data[-1] == "%"
        assert data[:-1].isdigit()
        return int(data[:-1])

    def refresh(self, site=None):

        if not site:
            site = self.default_site

        self.zones = []

        self.get('https://energy.comwatt.com/#/sites/%s/devices/' % site)
        WebDriverWait(self, timeout=20).until(lambda d: d.find_element(By.CLASS_NAME, 'ZoneDevices-item'))

        for elt_zone in self.find_elements(By.CLASS_NAME, 'ZoneDevices-item'): 

            elem_title = elt_zone.find_element(By.CLASS_NAME, 'css-2bb7pl')
            zone = Zone(elem_title.text)
            
            self.zones.append(zone)

            for elm_device in elt_zone.find_elements(By.CLASS_NAME, 'css-1aq3xkd'):
                
                elm_icon = elm_device.find_element(By.TAG_NAME, 'span')
                
                text_type = elm_icon.get_dom_attribute("class")

                device_type = None
                
                for type in DEVICES_TYPES:
                    
                    if text_type.count(type):
                        device_type = type
                        break

                device = None

                if device_type:
                    device = Device(device_type)
                    zone.add_device(device)

                elt_instant = elm_device.find_element(By.CLASS_NAME, 'css-11twb10')
                data = elt_instant.text
                
                if data == "N/A":
                    device.initialized = False
                    device.value_instant = 0.0
                else:
                    text_value, unit = data.split()
                    value = float(text_value)
                    
                    if unit == "kW":
                        value *= 1000

                    device.initialized = True
                    device.value_instant = value

    def get_devices(self, device_type):

        now = time.time()

        if self.last_refresh_time + 1 < now:
            self.refresh()
            self.last_refresh_time = now

        list_devices = []

        for zone in self.zones:
            for device in zone.devices:
                if device.type == device_type:
                    list_devices.append(device)

        return list_devices

    def __del__(self):
        # Close all browser windows
        self.quit()
