# amp-lab-http-rover
HTTP rover for AMP lab.

In `main.py`, select either `MotorController` (for the actual Onion motor controller) or `MockMotorController` (for testing on a non-Onion machine) by commenting out the one you don't want.

## Installation

Please view the [Getting Started](https://docs.onion.io/omega2-docs/first-time-setup.html) documentation from Onion to learn how to initially configure your device.

One that is done, follow the following procedure.

- Connect to your Onion device over WiFi.
- Set up python and pip:
```
opkg update
opkg install python
opkg install python-pip
```
- Use pip to install Flask:
```
pip install flask
```
- Clone this git repostory onto your device:
```
git clone git@github.com:clcain/amp-lab-http-rover.git
```
- Navigate into the repository and start Python:
```
cd amp-lab-http-rover
python main.py [left_motor_pin] [right_motor_pin]
```
Where `left_motor_pin` and `right_motor_pin` are substituted with the correct values.

## Usage

Navigate to port 80 of the IP address of the Onion device in a web browser. Your URL should resemble the follwoing: `http://192.168.0.1:8000`.

If the web page loads, you are good to go!

Please create an Issue on this repository if you encounter any issues.
