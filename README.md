 <h4 align="center">PiVision is an IoT system that seamlessly digitises handwritten notes using OCR technology for instant access and sharing.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#setting-up-the-raspberry-pi">Setting up the Raspberry PI</a> •
  <a href="#setting-up-the-web-application">Setting up the web application</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## Key Features

* Advanced OCR technology for reading text in an image using the Google Cloud Vision API
* Transmission of image text detection data to the web app
* Zoom-in functionality for focusing on text
* Light sensors to check that the lighting is good enough before taking a picture
* Useful status update messages on the LCD Backlight display

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) installed on your computer.

## Setting up the Raspberry PI

```bash
# Clone this repository
$ git clone https://git.cardiff.ac.uk/c22085374/group-project-iot.git

# Go into the repository
$ cd iot-project

# Configure the following environment variables using a .env file
$ touch .env
$ echo "API_KEY=ENTER_YOUR_GOOGLE_CLOUD_VISION_API_KEY_HERE" > .env
$ echo "SERIAL_PORT=ENTER_YOUR_ARDUINO_SERIAL_PORT_HERE" >> .env

# Create a new virtual environment and activate it
$ python -m venv venv
$ source ./venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Run the script
$ sudo -E ./venv/bin/python3 ./src/main.py
```

## Setting up the web application

After you have successfully executed the script, open a web browser and enter the following URL: http://localhost:5000.

## Credits

This software uses the following open source packages and APIs:

- [Socket.IO](https://socket.io/)
- [grovepi](https://pypi.org/project/grovepi/)
- [picamera](https://picamera.readthedocs.io/en/release-1.13/)
- [Google Cloud Vision API (for OCR)](https://cloud.google.com/vision/docs)

## The team

* Tarrin Curtis (Team lead and IoT developer)
* Lubomir Zelinsky (Web app designer and IoT developer)
* Ethan Patalano (IoT developer)
* Yusef Nazzal (IoT developer)