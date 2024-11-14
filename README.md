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
* **Background Application**: Does not interfere with work


## Prerequisites

1. **Python Installation Required**
   * Download Python 3.7 or higher for your operating system:
     * [Windows Download](https://www.python.org/downloads/)
     * [Mac Download](https://www.python.org/downloads/macos/)

   ### Windows Python Installation
   <img src="media/downloadpywindows.gif" alt="Installing Python on Windows" width="300">

   ### Mac Python Installation
   <img src="media/downloadpymac.gif" alt="Installing Python on Mac" width="300">

   ### Important Setup Note
   * During Windows installation, make sure to check "Add Python to PATH"
   
   <img src="media/pytopath.gif" alt="Adding Python to PATH" width="300">

2. **Webcam Required**
   * Built-in laptop webcam or external USB webcam


> Note: The application works best when webcam is postioned infront of you.

## macOS Installation Guide

### Steps

1. **Download and Extract**
   * Download the SitRight zip file
   * Move and Extract (unzip) the file to your Desktop
   >Note: The folder is required to in your desktop for the next commaand to work

   <img src="media/gettingrepo.gif" alt="Adding Python to PATH" width="300">



2. **Open Terminal**
   * Find Terminal in Applications > Utilities or use `Cmd + Space` to search
   
   <img src="media/terminal.png" alt="Terminal Icon" width="75">

3.
   **Move to application folder**
   ```bash
   cd Desktop/SitRight-main
   ```

4. **Install Dependencies** (One-time setup)
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Launch the App**
   ```bash
   python3 main.py
   ```

> Note: You only need to install dependencies (Step 4) once. For future use, simply start from Step 1 step 3 and to Step 5.


<img src="media/terminalcmds.gif" alt="Adding Python to PATH" width="300">

## Windows Installation Guide

### Steps

1. **Open Command Prompt**
   * search for "Command Prompt" in the Start menu
   

2. **Download and Extract**
   * Download the SitRight zip file
   * Exact all the ocntencts into the desktop (important)

3. **Navigate to Project**
   * In Command Prompt, first go to your Desktop:
   ```cmd
   cd Desktop/Sitright
   ```

4. **Install Dependencies** (One-time setup)
   ```cmd
   pip install -r requirements.txt
   ```

5. **Launch the App**
   ```cmd
   python sitright.py
   ```

> Note: You only need to install dependencies (Step 4) once. For future use, simply start from Step 1 and jump to Step 5.

> Tip: If you get a "python not found" error, try using `py` instead of `python` in the commands above.

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