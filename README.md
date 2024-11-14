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

1. **Must have Python**
   * Download Python at python.org/downloads.
   
<img src="media/DownloadingPy.gif" alt="Downloading Python" width="250">



      * During installation, check "Add Python to PATH."

      ![Downloading Python](media/pythontopath.gif)


2. **Webcam**
   * Make sure you have a Webcam (built-in or external).

## Installation (macOS)

### Steps

1. **Open Terminal app**
   * Find Terminal in Applications > Utilities or use `Cmd + Space` to search

2. **Go to Desktop**
   ```bash
   cd ~/Desktop
   ```

3. **Verify Python Installation**
   ```bash
   python3 --version
   ```

4. **Clone the Repository**
   ```bash
   git clone https://github.com/username/SitRight.git
   cd SitRight
   ```

5. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

6. **Run the App**
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