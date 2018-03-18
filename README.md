# amp-lab-http-rover
HTTP rover for AMP lab.

In `main.py`, select either `MotorController` (for the actual Onion motor controller) or `MockMotorController` (for testing on a non-Onion machine) by commenting out the one you don't want.

## Installation

Please view the [Getting Started](https://docs.onion.io/omega2-docs/first-time-setup.html) documentation from Onion to learn how to initially configure your device.

There is an [easy guide](https://docs.onion.io/omega2-docs/connecting-to-wifi-networks-command-line.html) for configuring your network connection provided by Onion.

One that is done, follow the following procedure.

- Connect to your Onion device over WiFi.
- Set up python-light and bottle:
```
vi /etc/opkg.conf
```
— delete line ‘option check_signature 1'
```
opkg update
mkdir -p /home/bottle
cd /home/bottle
wget --no-check-certificate https://github.com/defnull/bottle/raw/master/bottle.py
opkg install python-light
opkg install python-email
opkg install python-codecs
opkg install python-logging
opkg install python-openssl
opkg install pyOnionGpio

wget --no-check-certificate https://github.com/williamg42/amp-lab-http-rover/archive/master.tar.gz
tar -xvzf master.tar.gz
```
-Copy bottle.py into the new directory
- Navigate into the directory and start Python:
```
cd amp-lab-http-rover
python main.py [left_motor_pin] [right_motor_pin]
```
Where `left_motor_pin` and `right_motor_pin` are substituted with the correct values.

## Usage

Navigate to port 80 of the IP address of the Onion device in a web browser. Your URL should resemble the follwoing: `http://192.168.0.1:8000`.

If the web page loads, you are good to go!

Please create an Issue on this repository if you encounter any issues.
