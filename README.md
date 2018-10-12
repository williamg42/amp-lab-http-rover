# amp-lab-http-rover
HTTP rover for AMP lab.

In `main.py`, select either `MotorController` (for the actual Onion motor controller) or `MockMotorController` (for testing on a non-Onion machine) by commenting out the one you don't want.

## Installation

Please view the [Getting Started](https://docs.onion.io/omega2-docs/first-time-setup.html) documentation from Onion to learn how to initially configure your device.

There is an [easy guide](https://docs.onion.io/omega2-docs/connecting-to-wifi-networks-command-line.html) for configuring your network connection provided by Onion.

One that is done, follow the following procedure.

- Connect to your Onion device over WiFi.


- Download the repository
```
wget --no-check-certificate https://github.com/williamg42/amp-lab-http-rover/archive/master.tar.gz
tar -xvzf master.tar.gz
```

- Navigate into the directory
 ```
cd amp-lab-http-rover
```

- Run the install script
```
sh ./install.sh
```

- start the webserver:
```
sh ./run_server.sh
```
The server also automatically starts on boot

## Usage
On a Laptop:

- Connect to omega's wifi: `OMEGA-XXXX`

- Open a web browser

- go to `www.rover.control`


On a Phone/Tablet:

- Connect to omega's wifi: `OMEGA-XXXX`

- Open a web browser

- go to `http://192.168.3.1:8000`


If the web page loads, you are good to go!

Please create an Issue on this repository if you encounter any issues.
