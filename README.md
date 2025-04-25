# Steering Wheel App

The Steering Wheel App is a Python-based desktop application that allows users to simulate a driving controller using a DIY colour-coded cardboard steering wheel and their computer's webcam. Designed for casual and novice gamers, this software offers an accessible and engaging way to experience driving games with no expensive hardware required.

Many unique game experiences are locked behind costly peripherals like racing wheels and joysticks. This project democratises these experiences by letting users interact with racing games through basic hardware: a webcam and a colourful homemade steering wheel.

## Features
* **Colour-based steering input**: Track 4 colours on a physical wheel to detect direction, acceleration and braking.
* **Calibration wizard**: Choose between WASD or arrow key mappings.
* **Live camera feed**: Real-time feedback with masked image overlays.
* **Minimal setup**: No external hardware needed other than a webcam and a homemade wheel.

## Requirements
### Hardware
* Desktop or laptop with a webcam
* DIY steering wheel with 4 distinct colour markers

### Software
* Python 3
* OpenCV
* NumPy
* Imutils
* Pynput
* Tkinter
* PIL (Python Imaging Library)

## How to use this software
1. **Make your wheel**: Create a steering wheel using cardboard or paper and divide it into four colour-coded quadrants (e.g. red, green, blue and yellow).
2. **Calibrate**: Run the app and calibrate HSV ranges for each colour using live webcam feedback.
3. **Play**: Launch your favourite driving game and use the wheel to steer, accelerate and brake. The app sends simulated key presses based on your wheel's orientation and colour visibility.

## User interface
* **Main menu**: Begin calibration, set keyboard preferences, start playing or learn about the app.
* **Calibration windiw**: Adjust HSV sliders for each colour and preview the mask in real-time.
* **Play window**: Shows masked live feed and sends input to games.
* **About section**: Guides on software usage, wheel creation and gesture recognition.
