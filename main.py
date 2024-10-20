import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import messagebox
import platform
import subprocess
from plyer import notification

# Function to show system notification for posture reminder (cross-platform)
def show_posture_reminder():
    system = platform.system()
    
    if system == "Darwin":  # macOS
        message = "Please adjust your posture!"
        title = "Posture Reminder"
        # Use AppleScript to show notification on macOS
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script])
    elif system == "Windows":  # Windows
        notification.notify(
            title="Posture Reminder",
            message="Please adjust your posture!",
            timeout=2.5  # The notification will disappear after 2.5 seconds
        )

def get_avg_head_height(faces):
    """ Returns the average head height from the detected faces. """
    head_heights = [h for (x, y, w, h) in faces if h > 50]  # Filter out small noise
    if len(head_heights) > 0:
        return int(np.mean(head_heights))
    return None

def start_posture_reminder():
    # Load the pre-trained face detection model (Haar cascade)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Try opening the webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot access webcam.")
        messagebox.showerror("Error", "Cannot access webcam. Make sure it is not in use by another application and has permission.")
        return

    # Variables to store baseline head height and position
    baseline_head_height = None
    baseline_head_position = None
    last_reminder_time = 0  # To track the time of the last reminder
    cooldown_period = 10  # Cooldown period between reminders in seconds

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) > 0:
            avg_head_height = get_avg_head_height(faces)

            if baseline_head_height is None:
                # If baseline not set, encourage the user to set it
                cv2.putText(frame, 'Baseline not set', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                # Draw rectangle around detected face
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    current_head_position = y

                # Only check posture if the baseline is set
                if baseline_head_height is not None and baseline_head_position is not None:
                    # Check if the user is slouching or leaning too close
                    current_time = time.time()  # Get the current time
                    if (avg_head_height is not None and 
                        avg_head_height < baseline_head_height - 60 or 
                        current_head_position > baseline_head_position + 60) and \
                        (current_time - last_reminder_time > cooldown_period):
                        # Show reminder to fix posture if the cooldown period has passed
                        print("Warning: Please adjust your posture!")
                        show_posture_reminder()  # Trigger system notification
                        last_reminder_time = current_time  # Update the last reminder time

        # Add the quit message overlay
        cv2.putText(frame, 'Press "Q" to quit', (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, 'Press "b" to set baseline posture', (10, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Posture Reminder', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('b'):
            if len(faces) > 0:
                baseline_head_height = avg_head_height
                baseline_head_position = faces[0][1]  # y coordinate of the first detected face
                print(f"Baseline set: Height = {baseline_head_height}, Position = {baseline_head_position}")

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

def start_posture_reminder_gui():
    """ Starts the posture reminder system (in the main thread, no extra threading). """
    start_posture_reminder()  # Run the posture reminder directly in the main thread

def show_how_to_use():
    # Display a message with instructions on how to use the app
    messagebox.showinfo("How to Use", "1. Press 'Use' to start posture reminder.\n2. Follow the instructions to set your ideal posture.\n3. The program will remind you to adjust your posture when needed.")

def exit_program():
    root.quit()

# Create the main application window using tkinter
root = tk.Tk()
root.title("Posture Reminder Application")
root.geometry("300x200")

use_button = tk.Button(root, text="Use", command=start_posture_reminder_gui, height=2, width=15)
use_button.pack(pady=10)

how_to_use_button = tk.Button(root, text="How to Use", command=show_how_to_use, height=2, width=15)
how_to_use_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_program, height=2, width=15)
exit_button.pack(pady=10)

root.mainloop()
