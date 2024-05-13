import logging
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

    def __init__(self, comwatt_email, comwatt_password, headless = True):
        
        self.logger = logging.getLogger(self.__class__.__name__)

        options = Options()

        if headless:
            options.add_argument("-headless")

        super().__init__(options=options)
    
        self.zones = []

        self.default_site = None

        self.comwatt_email = comwatt_email
        self.comwatt_password = comwatt_password

        self.login()

        self.last_update_time = 0
        self.last_display_time = 0
        
        #self.last_data = ""
        #self.last_data_change_time = 0


    def login(self):

        self.logger.info("Login")
        
        # Get the login page
        super().get('https://energy.comwatt.com/#/login/')

        WebDriverWait(self, timeout=20).until(lambda d: d.find_element(By.NAME, 'email'))

        # Enter email and password
        elem = self.find_element(By.NAME, 'email')  # Find the search box
        elem.send_keys(self.comwatt_email + Keys.RETURN)

        elem = self.find_element(By.NAME, 'password')  # Find the search box
        elem.send_keys(self.comwatt_password + Keys.RETURN)

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

        self.logger.info("Login: success")
        self.logger.info("Defaut site is %s" % self.default_site)

    def get(self, url):
        
        self.logger.info("Get %s" % url)

        # First try
        super().get(url)

        # Back to login page -> retry logins
        if self.current_url == URL_LOGIN:
            self.logger.warn("Disconnected: login required")
            self.login()

            # Second try
            super().get(url)

    def meter(self, site=None):

        self.logger.debug("Begin meter %s" % site)

        if not site:
            site = self.default_site

        self.get('https://energy.comwatt.com/#/sites/%s/meter/' % site)
        WebDriverWait(self, timeout=20).until(lambda d: d.find_element(By.CLASS_NAME, 'css-3kduam'))

        elem = self.find_element(By.CLASS_NAME, 'css-3kduam')

        data = elem.text
        assert data[-1] == "%"
        assert data[:-1].isdigit()
        value = int(data[:-1])

        self.logger.debug("Meter = %d%" % value)

        return value


    def display_devices_page(self, site=None):

        if not site:
            site = self.default_site

        if self.current_url != 'https://energy.comwatt.com/#/sites/%s/devices/' % site:
            self.get('https://energy.comwatt.com/#/sites/%s/devices/' % site)
        else:
            self.refresh()

        try:
            WebDriverWait(self, timeout=20).until(lambda d: d.find_element(By.CLASS_NAME, 'ZoneDevices-item'))
        except:
            raise RuntimeError
            # Todo : Add update ?

    def update_devices_data(self, site=None):
        """Analyze the devices page"""

        if not site:
            site = self.default_site

        self.logger.info("Update devices data for %s" % site)

        #TODO : Change this. Don't delete everything before updating
        self.zones = []

        # Reload page every 10 minutes
        now = time.time()
        if self.last_display_time + 600 < now:
            self.logger.warn("Reload devices page")
            self.display_devices_page(site)
            self.last_display_time = now

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

    def get_devices(self, device_type, site=None):

        self.logger.info("Get devices %s" % device_type)

        now = time.time()

        if self.last_update_time + 1 < now:
            self.update_devices_data(site)
            self.last_update_time = now

        list_devices = []

        for zone in self.zones:
            for device in zone.devices:
                if device.type == device_type:
                    list_devices.append(device)

        return list_devices

    def __del__(self):
        # Close all browser windows
        self.quit()
