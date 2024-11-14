# SitRight: Posture Reminder Application

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [How It Works](#how-it-works)
6. [Dependencies](#dependencies)
7. [Contact](#contact)

## Introduction

**SitRight** is a cross-platform program that helps you sit better. It uses your webcam to monitor posture and reminds you to sit correctly. Easy to use, runs in the background, and works on macOS and Windows.

## Features


* **Posture Monitoring**: Real-time feedback via webcam.
* **Cross-Platform**: Works on macOS and Windows.
* **Simple Interface**: Easy and modern GUI.


## Prerequisites

1. **Python 3.7 or Later**
   * Download Python: python.org/downloads.
      * During installation, check "Add Python to PATH."

2. **Webcam**
   * Make sure you have a Webcam (built-in or external).

## Installation (macOS)

### Steps

1. **Open Terminal**
   * Find Terminal in Applications > Utilities or use `Cmd + Space` to search.

2. **Go to Desktop**
   ```bash
   cd ~/Desktop
   ```

   * Verify installation:
     ```bash
     python3 --version
     ```

3. **Clone the Repository**
   ```bash
   git clone https://github.com/username/SitRight.git
   
   

   move to the project folder 
   cd SitRight
   ```

4. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run the App**
   ```bash
   python3 sitright.py
   ```

## Usage

1. **Start SitRight**
   * Run this command:
     ```bash
     python3 sitright.py
     ```

2. **Set Your Posture**
   * Sit upright.
   * Press **B** in the webcam feed.

3. **Monitor Posture**
   * SitRight checks if you deviate and reminds you to adjust.

4. **Quit**
   * Press **Q** in the webcam feed to stop.

## How It Works

* **Baseline Posture**: Captures your upright sitting position.
* **Monitoring**: Tracks head height and position for deviations.
* **Notifications**: Alerts you if you need to adjust.

## Dependencies

Install these Python libraries:
* `customtkinter`
* `cv2` (OpenCV)
* `mediapipe`
* `plyer`
* `Pillow`
* `numpy`

why i created sitright 

why use sit right 



## Contact

**Author**: Areyan Rastawan  
**GitHub**: AreyanR  
**Email**: areyanrastawan@example.com

---

Thank you for using SitRight! Stay ergonomic.