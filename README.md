# SitRight: Posture Reminder Application

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [How It Works](#how-it-works)
6. [Dependencies](#dependencies)
7. [Project Structure](#project-structure)
8. [Known Issues](#known-issues)
9. [Contributing](#contributing)
10. [License](#license)
11. [Contact](#contact)

## Introduction
SitRight is a cross-platform application designed to encourage healthy posture habits while working at a computer. Using a webcam and real-time face detection, the application monitors your posture and provides gentle reminders to sit correctly.

The application is simple, intuitive, and runs seamlessly in the background, ensuring minimal disruption while helping you maintain ergonomic posture.

## Features
* **Posture Monitoring**: Detects user posture in real-time via webcam
* **Cross-Platform Notifications**: Provides reminders on both macOS and Windows
* **User-Friendly GUI**: Simple and intuitive graphical user interface
* **Customizable Reference Posture**: Allows users to set their own baseline posture
* **Visual Feedback**: Displays real-time posture analysis through the webcam feed
* **Splash Screen**: A professional loading screen with animated visuals

## Installation

### Prerequisites:
* Python 3.7 or later
* Webcam (internal or external)

### Steps:
1. Clone this repository:
```bash
git clone https://github.com/username/SitRight.git
cd SitRight
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python sitright.py
```

## Usage
1. Launch the application by running `sitright.py`
2. Set Reference Posture:
   * Sit upright in your preferred posture
   * Press the "B" key in the webcam feed to set this posture as the baseline
3. Posture Monitoring:
   * The application will monitor your posture and notify you when adjustments are needed
4. Ending the Session:
   * Press the "Q" key in the webcam feed to quit monitoring

For a detailed guide, refer to the "How to Use" section in the application.

## How It Works
SitRight utilizes the following technologies:
* MediaPipe for real-time face detection
* OpenCV to process webcam feeds and provide visual feedback
* CustomTkinter for a modern and user-friendly GUI
* Platform-Specific Notifications:
   * macOS: AppleScript-based notifications
   * Windows: plyer library for native notifications

The application calculates head height and position to determine if the user deviates from their baseline posture. If deviations are detected, a notification is triggered.

## Dependencies
### Python Libraries:
* customtkinter
* cv2 (OpenCV)
* mediapipe
* plyer
* Pillow
* numpy

### Platform-Specific Tools:
* macOS: AppleScript for notifications

Install all dependencies using:
```bash
pip install -r requirements.txt
```



## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or suggestions, please reach out to:
* **Author**: Areyan Rastawan
* **GitHub**: https://github.com/AreyanR
* **Email**: areyanrastawan@example.com

Thank you for using SitRight! We hope this tool helps you maintain a healthy and ergonomic posture. 🎉