## Commwatt Gen4 Python client

This module allow you to retrieve data from your Comwatt PowerGen4 box.
It connects to the Commwatt website using Selenium webdriver and firefox and reads teh data.

# Installation 

Prerequisites:
- Install Firefox 
- Download geckodriver form https://github.com/mozilla/geckodriver/releases

Install using pip:

```
$ python -m pip install comwatt
```

# Usage

```
import comwatt
c = comwatt.PowerGEN4(<username>, <password>)
s = c.get_devices("sun")
print(s[0].value_instant)
```

Available device types are:
- injection
- withdrawal
- sun
- hotwatertank
- plug
