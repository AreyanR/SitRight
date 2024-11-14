import customtkinter as ctk
import cv2
import numpy as np
import time
import platform
import subprocess
from tkinter import messagebox
from plyer import notification
from PIL import Image, ImageTk
import tkinter as tk
import mediapipe as mp
import os
import sys

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')


BASE_DIR = os.path.dirname(__file__)

# Construct a path to resources
splashscreen_path = os.path.join(BASE_DIR, "resources", "splashscreen1.gif")
icon_path = os.path.join(BASE_DIR, "resources", "icon.ico")


# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def show_posture_reminder():
    """
    Displays a posture reminder notification to the user based on their operating system. (MacOS and Windows)
    """
    system = platform.system()

    if system == "Darwin":  # macOS
        message = "Please adjust your posture!"
        title = "SitRight"
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script])
    elif system == "Windows":  # Windows
        notification.notify(
            title="SitRight",
            message="Please adjust your posture!",
            timeout=2.5
        )
    else:  # You can add Linux or other OS here
        pass

def get_avg_head_height(faces):
    """ Returns the average head height from the detected faces. """
    head_heights = [h for (x, y, w, h) in faces if h > 50]  # Extract the height (h) from each face tuple
    if len(head_heights) > 0:
        return int(np.mean(head_heights))  # Calculate the average height
    return None


# Function that starts the main functionality of the application
def start_posture_reminder_gui():
    """
    Manages the GUI workflow to start the posture reminder, accessing the webcam and handling errors.
    """
    global use_button

    # Disable the "Use" button and update its text to indicate loading
    use_button.configure(text="Loading...", state="disabled")
    root.update()

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    time.sleep(2)  # Allow time for the webcam to initialize

    # Check if the webcam is accessible
    if not cap.isOpened():
        # Re-enable the "Use" button and show an error message if the webcam cannot be accessed
        use_button.configure(text="Use", state="normal")
        messagebox.showerror("Error", "Cannot access webcam. Make sure it is not in use by another application and has permission.")
        return

    # Hide the main GUI window while posture monitoring is active
    root.withdraw()

    # Start the posture reminder functionality
    start_posture_reminder(cap)

    # Restore the main GUI window after posture monitoring ends
    root.deiconify()
    use_button.configure(text="Use", state="normal")  # Re-enable the Use button

def start_posture_reminder(cap):
    """
    Monitors the user's posture through a webcam feed and provides real-time reminders to maintain proper posture.

    Key Features:
    - Detects faces and calculates head height and position.
    - Allows the user to set a baseline reference posture.
    - Issues reminders when posture deviates significantly from the baseline.
    - Displays visual feedback in the webcam feed, including instructions and posture status.
    - Provides options to quit the program or set the reference posture via keyboard input.

    Parameters:
        cap (cv2.VideoCapture): The webcam feed used for posture detection and monitoring.
    """
    # Initialize baseline posture variables and timing for reminders
    baseline_head_height, baseline_head_position = None, None
    last_reminder_time = 0
    cooldown_period = 5  # seconds between reminders

    # State variables for managing status messages
    baseline_set = False
    message = "Reference posture not set"
    message_time = time.time()
    message_display_duration = 3  # seconds for displaying messages

    # Start face detection using MediaPipe's Face Detection module
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        while True:
            # Read the current frame from the webcam
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to RGB for face detection
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb_frame)

            current_time = time.time()

            # Manage the display of dynamic messages
            if not baseline_set:
                display_message = "Reference posture not set"
                display_color = (0, 0, 255)  # Red for warning
            elif baseline_set and (current_time - message_time) < message_display_duration:
                display_message = "Reference posture set"
                display_color = (0, 255, 0)  # Green for success
            else:
                display_message = ""  # No message

            # Display the message on the video feed
            if display_message:
                cv2.putText(frame, display_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, display_color, 2)

            # Detect faces and extract bounding boxes
            faces = []
            if results.detections:
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    x = int(bbox.xmin * frame.shape[1])
                    y = int(bbox.ymin * frame.shape[0])
                    w = int(bbox.width * frame.shape[1])
                    h = int(bbox.height * frame.shape[0])
                    faces.append((x, y, w, h))

            # Keep only the largest detected face
            if faces:
                faces = [max(faces, key=lambda face: face[2] * face[3])]  # Largest face by area

            # Draw bounding boxes around detected faces
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Calculate the average head height of detected faces
            avg_head_height = get_avg_head_height(faces)

            # Check for posture deviation and trigger reminders
            if baseline_head_height is not None and baseline_head_position is not None:
                if (avg_head_height is not None and avg_head_height < baseline_head_height - 30) or \
                   (faces and faces[0][1] > baseline_head_position + 30):
                    if (current_time - last_reminder_time > cooldown_period):
                        #print("Warning: Please adjust your posture!")
                        show_posture_reminder()
                        last_reminder_time = current_time

            # Display instructions for quitting and setting baseline posture
            cv2.putText(frame, 'Press "Q" to quit', (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(frame, 'Press "B" to set Reference posture',
                        (10, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 0), 2)

            # Show the video feed with annotations
            cv2.imshow('SitRight', frame)

            # Keyboard controls for quitting or setting baseline posture
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                break  # Quit the program
            elif key == ord('b') or key == ord('B'):
                # Set the baseline posture if a face is detected
                if len(faces) > 0:
                    baseline_head_height = avg_head_height
                    baseline_head_position = faces[0][1]
                    baseline_set = True
                    message = "Reference posture set"
                    message_time = current_time  # Update message timestamp
                    #print(f"Baseline set: Height = {baseline_head_height}, Position = {baseline_head_position}")
                else:
                    message = "No face detected. Cannot set baseline."
                    message_time = current_time  # Update message timestamp

    # Release the webcam and close the display window
    cap.release()
    cv2.destroyAllWindows()



    
def clear_frame():
    """Clear all widgets from the frame."""
    for widget in frame.winfo_children():
        widget.destroy()

def show_how_to_use():
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width, height = 650, 800

    # Calculate x and y for centered positioning and move it up by 100 pixels
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2) - 100  # Move up by 200 pixels

    # Set geometry with updated y-coordinate
    root.geometry(f"{width}x{height}+{x}+{y}")
    frame.pack_propagate(False)
    clear_frame()

    # Main title
    how_to_use_title = ctk.CTkLabel(frame, text="How to Use", font=("Helvetica", 24, "bold"))
    how_to_use_title.pack(pady=20)

    # Frame for each section
    instructions = [
        ("Step 1: Start the Program", "Press the 'Use' button to begin."),
        ("Step 2: Set Your Posture", "- Sit in a comfortable, upright position.\n- Press the 'B' key to save this as your refrence posture."),
        ("Step 3: Let the Program Monitor Your Posture", "You can continue working, and the program will alert you if you move out of your set posture."),
        ("Step 4: End the Session", "To stop the session, press the 'Q' key in the camera window."),
        ("Uses", "This tool can be used for any task that involves sitting and using your computer. It can run in the background of any application"),
        ("Note", "- Both external and built-in laptop cameras are supported\n- Make sure your webcam is positioned directly in front of your face for the best results.")
    ]

    for title, content in instructions:
        section_frame = ctk.CTkFrame(frame, corner_radius=10)
        section_frame.pack(pady=10, padx=20, fill="x", expand=False)

        # Section title
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Helvetica", 16, "bold"))
        title_label.pack(anchor="w", pady=(10, 0), padx=10)

        # Section content
        content_label = ctk.CTkLabel(section_frame, text=content, font=("Helvetica", 14), wraplength=550, justify="left")
        content_label.pack(anchor="w", pady=(0, 10), padx=10)

    # Back button
    back_button = ctk.CTkButton(frame, text="Back", command=load_main_menu, fg_color="#e08814", hover_color="#CC7000", font=("Helvetica", 15, "bold"))
    back_button.pack(pady=20)


def show_about_project():
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width, height = 650, 800

    # Calculate x and y for centered positioning and move it up by 200 pixels
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2) - 200  # Move up by 200 pixels

    # Set geometry with updated y-coordinate
    root.geometry(f"{width}x{height}+{x}+{y}")
    frame.pack_propagate(False)
    clear_frame()

    # Main title
    about_title = ctk.CTkLabel(frame, text="About the Project", font=("Helvetica", 24, "bold"))
    about_title.pack(pady=20)

    # Sections within the "About Project" screen
    sections = [
        ("Application Purpose", 
        "SitRight aims to encourage healthy posture habits in an era when many of us spend long hours at desks. "
        "It can be challenging to remember to maintain good posture while using the computer, so why not let it do it for you? "
        "Whether you’re working, gaming, or browsing the web, SitRight is here to prevent poor posture "
        "by providing gentle reminders to maintain an ideal sitting position."),

        ("How It Works", 
        "SitRight uses your webcam to get a refrence of when you’re seated in an optimal posture.\n\n"
        "During your session, it monitors for deviations from this position and alerts you when adjustments are needed. "
        ),

        ("Why I Created SitRight", 
        "As someone passionate about technology, I spend countless hours at the computer. Maintaining good posture has always been a challenge, "
        "it’s too easy to get absorbed in work and forget about sitting properly."
        "I created SitRight to tackle this issue, both for myself and for others struggling to maintain good posture."
        "It’s a simple, accessible, and free solution for anyone who spend long hours seated."),

        ("Why Use SitRight?", 
        "Free: SitRight is completely free to use.\n"
        "Cross-platform: Works on both macOS and Windows.\n"
        "User-friendly: Simple setup and intuitive to use.\n"
        "Convenient: Runs in the background without interruptions.")

    ]

    for title, content in sections:
        section_frame = ctk.CTkFrame(frame, corner_radius=10)
        section_frame.pack(pady=10, padx=20, fill="x", expand=False)

        # Section title
        title_label = ctk.CTkLabel(section_frame, text=title, font=("Helvetica", 16, "bold"))
        title_label.pack(anchor="w", pady=(10, 0), padx=10)

        # Section content
        content_label = ctk.CTkLabel(section_frame, text=content, font=("Helvetica", 14), wraplength=550, justify="left")
        content_label.pack(anchor="w", pady=(0, 10), padx=10)

    # Back button
    back_button = ctk.CTkButton(frame, text="Back", command=load_main_menu, fg_color="#e08814", hover_color="#CC7000", font=("Helvetica", 15, "bold"))
    back_button.pack(pady=20)

def load_main_menu():
    # Set window dimensions
    width, height = 600, 400

    # Calculate x and y coordinates for centering the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the geometry while the window is still hidden
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Show the window in the center without flicker
    root.deiconify()

    frame.pack_propagate(True)
    clear_frame()

    title_label = ctk.CTkLabel(frame, text="SitRight ", font=("Helvetica", 36, "bold", "italic"))
    title_label.pack(pady=10)

    global use_button
    use_button = ctk.CTkButton(
        frame, text="Use", command=start_posture_reminder_gui, height=40, width=200, 
        fg_color="#e08814", hover_color="#CC7000", font=bold_font
    )
    use_button.pack(pady=10)

    how_to_use_button = ctk.CTkButton(
        frame, text="How to Use", command=show_how_to_use, height=40, width=200, 
        fg_color="#e08814", hover_color="#CC7000", font=bold_font
    )
    how_to_use_button.pack(pady=10)

    about_button = ctk.CTkButton(
        frame, text="About Project", command=show_about_project, height=40, width=200, 
        fg_color="#e08814", hover_color="#CC7000", font=bold_font
    )
    about_button.pack(pady=10)

    exit_button = ctk.CTkButton(
        frame, text="Exit", command=exit_program, height=40, width=200, 
        fg_color="#e08814", hover_color="#CC7000", font=bold_font
    )
    exit_button.pack(pady=10)

def exit_program():
    root.quit()

# Splash Screen Function
def show_splash_screen():
    splash_root = tk.Toplevel(root)
    splash_root.overrideredirect(True)
    splash_width, splash_height = 600, 400
    splash_root.geometry(f"{splash_width}x{splash_height}+{(splash_root.winfo_screenwidth() - splash_width) // 2}+{(splash_root.winfo_screenheight() - splash_height) // 2}")
    splash_root.configure(bg="#2b2b2a")  # Set splash screen background to grey

    # Load and resize the GIF image
    try:
        gif_image = Image.open("resources/splashscreen1.gif")
    except FileNotFoundError:
        messagebox.showerror("Error", "Splash screen GIF not found.")
        root.quit()
        return

    gif_frames = []
    try:
        while True:
            frame = gif_image.copy().resize((200, 175), Image.Resampling.LANCZOS)
            gif_frames.append(ImageTk.PhotoImage(frame))
            gif_image.seek(len(gif_frames))  # Move to next frame
    except EOFError:
        pass  # End of GIF frames

    if not gif_frames:
        messagebox.showerror("Error", "No frames found in splash screen GIF.")
        root.quit()
        return

    # Display GIF animation
    gif_label = tk.Label(splash_root, bg="#2b2b2a")  # Set background to grey
    gif_label.place(relx=0.5, rely=0.5, anchor='center')

    # Loading label for animated text
    loading_label = tk.Label(splash_root, text="Loading", font=("Helvetica", 20, "bold"), bg="#2b2b2a", fg="white")
    loading_label.place(relx=0.5, rely=0.8, anchor='center')

    # Function to animate GIF and loading text together
    def animate_gif_and_text(gif_label, gif_frames, loading_label, frame_index=0, count=0):
        # Update GIF frame
        gif_label.config(image=gif_frames[frame_index])
        # Update Loading text
        dots = "." * (count % 4)  # Cycle between no dots, 1 dot, 2 dots, and 3 dots
        loading_label.config(text=f"Loading{dots}")
        # Schedule next update for both GIF and text
        gif_label.after(600, animate_gif_and_text, gif_label, gif_frames, loading_label, (frame_index + 1) % len(gif_frames), count + 1)

    # Start the combined GIF and text animation
    animate_gif_and_text(gif_label, gif_frames, loading_label)

    # Destroy splash screen and load main menu after 4 seconds
    splash_root.after(4000, lambda: [splash_root.destroy(), load_main_menu()])

# Main entry point
root = ctk.CTk()
root.withdraw()  # Hide the main window until the splash screen is done
root.title("SitRight Application")
root.geometry("600x400")

if platform.system() == "Windows":
    try:
        root.iconbitmap("resources/icon.ico")
    except Exception as e:
        print(f"Error setting icon on Windows: {e}")

# Set bold font for buttons
bold_font = ("Arial", 15, "bold")

# Add a frame to organize buttons
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Show splash screen and load main menu
show_splash_screen()

root.mainloop()

