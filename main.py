import customtkinter as ctk
import cv2
import numpy as np
import time
import platform
import subprocess
from tkinter import messagebox
from plyer import notification

# Function to show system notification for posture reminder (cross-platform)
def show_posture_reminder():
    system = platform.system()
    
    if system == "Darwin":  # macOS
        message = "Please adjust your posture!"
        title = "Posture Reminder"
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script])
    elif system == "Windows":  # Windows
        notification.notify(
            title="Posture Reminder",
            message="Please adjust your posture!",
            timeout=2.5
        )

def get_avg_head_height(faces):
    """ Returns the average head height from the detected faces. """
    head_heights = [h for (x, y, w, h) in faces if h > 50]  # Filter out small noise
    if len(head_heights) > 0:
        return int(np.mean(head_heights))
    return None

def start_posture_reminder_gui():
    use_button.configure(text="Loading...", state="disabled")
    root.update()

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    time.sleep(2)

    if not cap.isOpened():
        use_button.configure(text="Use", state="normal")
        messagebox.showerror("Error", "Cannot access webcam. Make sure it is not in use by another application and has permission.")
        return

    root.withdraw()
    start_posture_reminder(cap, face_cascade)
    root.deiconify()
    use_button.configure(text="Use", state="normal")

def start_posture_reminder(cap, face_cascade):
    baseline_head_height = None
    baseline_head_position = None
    last_reminder_time = 0
    cooldown_period = 10

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) > 0:
            avg_head_height = get_avg_head_height(faces)
            if baseline_head_height is None:
                cv2.putText(frame, 'Set baseline at ideal posture', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    current_head_position = y

                if baseline_head_height is not None and baseline_head_position is not None:
                    current_time = time.time()
                    if (avg_head_height is not None and 
                        avg_head_height < baseline_head_height - 60 or 
                        current_head_position > baseline_head_position + 60) and \
                        (current_time - last_reminder_time > cooldown_period):
                        print("Warning: Please adjust your posture!")
                        show_posture_reminder()
                        last_reminder_time = current_time

        cv2.putText(frame, 'Press "Q" to quit', (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, 'Press "b" to set baseline posture', (10, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow('Posture Reminder', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('b'):
            if len(faces) > 0:
                baseline_head_height = avg_head_height
                baseline_head_position = faces[0][1]
                print(f"Baseline set: Height = {baseline_head_height}, Position = {baseline_head_position}")

    cap.release()
    cv2.destroyAllWindows()

def show_how_to_use():
    messagebox.showinfo("How to Use", "1. Press 'Use' to start posture reminder.\n2. Follow the instructions to set your ideal posture.\n3. The program will remind you to adjust your posture when needed.")

def show_about_project():
    messagebox.showinfo("About Project", "This project is a posture reminder tool that uses a webcam to detect head position and posture to help users maintain a healthy posture.")

def exit_program():
    root.quit()

# Create the main application window using customtkinter
root = ctk.CTk()
root.title("Posture Reminder Application")
root.geometry("600x400")

# Add a frame to organize buttons
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Add a title label at the top of the frame
title_label = ctk.CTkLabel(frame, text="Posture Reminder", font=("Arial", 20))
title_label.pack(pady=10)

# Add buttons in the frame
use_button = ctk.CTkButton(frame, text="Use", command=start_posture_reminder_gui, height=40, width=200)
use_button.pack(pady=10)

how_to_use_button = ctk.CTkButton(frame, text="How to Use", command=show_how_to_use, height=40, width=200)
how_to_use_button.pack(pady=10)

about_button = ctk.CTkButton(frame, text="About Project", command=show_about_project, height=40, width=200)
about_button.pack(pady=10)

exit_button = ctk.CTkButton(frame, text="Exit", command=exit_program, height=40, width=200)
exit_button.pack(pady=10)

root.mainloop()
