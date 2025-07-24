# Object Tracker

A Python-based object tracking application using OpenCV to track objects in real-time via a webcam (Iriun Webcam over USB or laptop camera). The application combines the CSRT tracker with continuous template matching to robustly track objects, automatically reacquiring them if they leave and reenter the frame.

## Features

- Real-time object tracking using the CSRT (Channel and Spatial Reliability Tracking) algorithm.
- Continuous template matching to reacquire objects that exit and reenter the camera frame.
- Region of Interest selection for specifying the object to track.
- Displays tracking status ("Tracking (Tracker)", "Tracking (Reacquired)", or "Lost, searching...") and FPS.
- Supports Iriun Webcam (USB mode) or any standard webcam (e.g., laptop camera).

## Requirements

- Python 3.6+
- Dependencies:
    - opencv-python: For computer vision and tracking.
    - numpy: For numerical operations.
    - Iriun Webcam (if using a phone as a webcam):
        - Iriun Webcam app on Android/iOS.
        - Iriun Webcam client on your computer.
- Hardware:
    - USB-connected phone (for Iriun Webcam) or built-in/external webcam.

## Installation

- Install Python Dependencies:
```
pip install opencv-python numpy
```
- Install Iriun Webcam (Optional, for USB Phone Camera):
    - On Phone: Download the Iriun Webcam app from Google Play Store (Android) or App Store (iOS).
    - On Ubuntu:
      Download the Iriun Webcam client from https://iriun.com/.
    Install the .deb package (replace <version> with the downloaded version):

```
sudo apt install -f <your iriunwebcam-<version>.deb path>
```
-  List available video devices to find the Iriun Webcam index:
```
ls /dev/video*
```


## Usage

1) Connect Iriun Webcam (if used):
  - Enable USB debugging on Android (Settings > Developer Options > USB Debugging).
  - Connect your phone to your computer via USB.
  - Open the Iriun Webcam app on your phone and select USB mode.
  - Launch the Iriun Webcam client on your computer to activate the virtual webcam.

2) Run the Script:
  - Clone or download this repository.
  - Update the camera index in object_tracker.py if needed (default is 2 for Iriun Webcam; use 0 for laptop camera):
```
cap = cv2.VideoCapture(2)  # Adjust to 0, 1, or other index
```
 - Run the script:

```
python3 object_tracker.py
```

3) Track an Object:
  - A window will open showing the camera feed.
  - Drag a rectangle around the object to track and press Enter.
  - The script tracks the object, displaying a green bounding box and status:

    - "Tracking (Tracker)": Using the CSRT tracker.
    - "Tracking (Reacquired)": Reinitialized via template matching.
    - "Lost, searching...": Object not detected.
  - Press 'q' to quit.

## Flow chart
The following flowchart illustrates the object tracking process:
<img width="1421" height="620" alt="diagram-export-2025-07-24-4_45_18-p m" src="https://github.com/user-attachments/assets/4805a3e1-aa2a-44bf-b9d3-84e2290254f2" />





