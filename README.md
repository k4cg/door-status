
# K4CG door-status

This program submits the k4cg space door status to "heimat". It is intended to run on an ESP8266 controller with micropython firmware.
[Link: Miropython ESP8266 Docs](http://docs.micropython.org/en/latest/esp8266/)

## Status Transmission

The data transfer is periodically performed by the ESP (~ 5 minute intervals) to http://heimat:8000 via PUT request.

It contains a JSON formatted structure like:
    {"humidity": 35, "door": "open", "date": "2017-08-21 19:11:50", "tempDoor": 27}

## Code Upload

First time upload: Connect via serial port with mpfshell:
    # mpfshell -c "open ttyUSB0"
    mpfs [/]> put boot.py
    mpfs [/]> put service.py
    ...

Update code:
    # mpfshell -c "open ws:192.168.178.9,PASSWORD"
    mpfs [/]> put boot.py
    mpfs [/]> put service.py
    ...
    mpfs [/]> repl
    >>> reboot()
