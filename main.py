import cv2
import numpy as np
from plyer import notification
import time
import tkinter as tk
from tkinter import messagebox
import threading

# Function to show system notification for posture reminder
def show_posture_reminder():
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

    # Open webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)

    # Variables to store baseline head height and position
    baseline_head_height = None
    baseline_head_position = None
    warning_displayed = False
    last_reminder_time = 0  # To track the time of the last reminder
    cooldown_period = 10  # Cooldown period between reminders in seconds

    # Set the button text to "Running" once the system starts
    use_button.config(text="Running")

    while True:
        ret, frame = cap.read()

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) > 0:
            avg_head_height = get_avg_head_height(faces)
            
            if baseline_head_height is None:
                # If baseline not set, encourage the user to set it
                cv2.putText(frame, 'baseline not set', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                # Draw rectangle around detected face
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    current_head_position = y

                # Check if the user is slouching or leaning too close
                current_time = time.time()  # Get the current time
                if (avg_head_height < baseline_head_height - 60 or 
                    current_head_position > baseline_head_position + 60) and \
                    (current_time - last_reminder_time > cooldown_period):
                    # Show reminder to fix posture if the cooldown period has passed
                    print("Warning: Please adjust your posture!")
                    show_posture_reminder()  # Trigger system notification
                    last_reminder_time = current_time  # Update the last reminder time

        # Add the quit message overlay
        cv2.putText(frame, 'Press "Q" to quit', (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        # Add the baseline setting message overlay (always there even after baseline is set)
        cv2.putText(frame, 'Press "b" to while in your ideal posture', (10, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Posture Reminder', frame)

        # Key handling
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            # Quit if 'q' is pressed
            break
        elif key == ord('b'):
            # Set baseline when 'b' is pressed
            if len(faces) > 0:
                baseline_head_height = avg_head_height
                baseline_head_position = faces[0][1]  # y coordinate of the first detected face
                print(f"Baseline set: Height = {baseline_head_height}, Position = {baseline_head_position}")

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

    # Reset the button to "Use" after quitting
    use_button.config(text="Use", state=tk.NORMAL)

def start_posture_reminder_thread():
    """ Runs the posture reminder in a separate thread and updates the button text. """
    use_button.config(text="Loading...", state=tk.DISABLED)  # Change text to "Loading..." and disable the button
    threading.Thread(target=start_posture_reminder).start()  # Start posture reminder in a separate thread

def show_how_to_use():
    # Display a message with instructions on how to use the app
    messagebox.showinfo("How to Use", "1. Press 'Use' to start posture reminder.\n2. Follow the instructions to set your ideal posture.\n3. The program will remind you to adjust your posture when needed.")

def exit_program():
    # Exit the program
    root.quit()

# Create the main application window using tkinter
root = tk.Tk()
root.title("Posture Reminder Application")
root.geometry("300x200")

# Create buttons for the main hub
use_button = tk.Button(root, text="Use", command=start_posture_reminder_thread, height=2, width=15)
use_button.pack(pady=10)

how_to_use_button = tk.Button(root, text="How to Use", command=show_how_to_use, height=2, width=15)
how_to_use_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_program, height=2, width=15)
exit_button.pack(pady=10)

# Start the tkinter main loop
root.mainloop()
