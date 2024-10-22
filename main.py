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
    global use_button  # Declare use_button as a global variable
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

        # Always display the baseline message
        cv2.putText(frame, 'Set baseline at ideal posture', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        if len(faces) > 0:
            avg_head_height = get_avg_head_height(faces)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                current_head_position = y

            if baseline_head_height is not None and baseline_head_position is not None:
                current_time = time.time()
                if (avg_head_height is not None and 
                    avg_head_height < baseline_head_height - 30 or 
                    current_head_position > baseline_head_position + 30) and \
                    (current_time - last_reminder_time > cooldown_period):
                    print("Warning: Please adjust your posture!")
                    show_posture_reminder()
                    last_reminder_time = current_time

        # Always show instructions for quitting and setting baseline
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

def clear_frame():
    """Clear all widgets from the frame."""
    for widget in frame.winfo_children():
        widget.destroy()

def show_how_to_use():
    """Display detailed 'How to Use' information and resize window."""
    root.geometry("800x600")  # Resize window to fit the content
    frame.pack_propagate(False)  # Prevent frame from resizing based on content
    clear_frame()

    how_to_use_title = ctk.CTkLabel(frame, text="How to Use", font=("Arial", 20))
    how_to_use_title.pack(pady=10)

    # Add a large text box with detailed usage instructions
    how_to_use_text = ctk.CTkTextbox(frame, width=600, height=300)
    how_to_use_text.pack(pady=10, expand=True, fill="both")  # Allow text box to expand with the window
    
    # Add detailed instructions to the textbox
    how_to_use_text.insert("1.0", 
    "Step 1: Start the Program\n"
    "- Press the 'Use' button to begin.\n"
    "- The camera will turn on.\n\n"
    
    "Step 2: Set Your Baseline Posture\n"
    "- Sit in a comfortable, upright position.\n"
    "- Press the 'b' key to save this posture as your baseline.\n\n"

    "Step 3: Let the Program Monitor Your Posture\n"
    "- After setting your baseline, the program will start monitoring your posture.\n"
    "- You can continue working, and the program will alert you if you move out of your baseline posture.\n\n"

    "Step 4: End the Session\n"
    "- To stop the session, press the 'q' key in the camera window.\n\n"

    "Uses:\n"
    "This tool can be used for any task that involves sitting and using your computer.\n" 
    "It can run in the background and will notify you when your posture needs adjustment.\n\n"

    "Note:\n"
    "Make sure your webcam or camera is positioned directly in front of your face for the best posture tracking results."
)

    how_to_use_text.configure(state="disabled")  # Make the text read-only

    # Add a button to return to the main menu
    back_button = ctk.CTkButton(frame, text="Back", command=load_main_menu)
    back_button.pack(pady=10)

def show_about_project():
    """Display detailed 'About the Project' information."""
    root.geometry("800x600")  # Resize window to fit the content
    frame.pack_propagate(False)  # Prevent frame from resizing based on content
    clear_frame()

    about_title = ctk.CTkLabel(frame, text="About the Project", font=("Arial", 20))
    about_title.pack(pady=10)

    # Add a large text box with project details
    about_text = ctk.CTkTextbox(frame, width=600, height=300)
    about_text.pack(pady=10, expand=True, fill="both")  # Allow text box to expand with the window

    # Add detailed project description to the textbox
    about_text.insert("1.0", 
    "### Addressing a Modern-Day Problem\n\n"
    "In today’s digital age, maintaining good posture has become increasingly difficult. With most people spending countless hours in front of computers, poor posture has become a widespread issue, leading to back pain, discomfort, and long-term health problems. \n\n"
    
    "### Personal Motivation\n\n"
    "I faced this challenge personally, often struggling to keep my posture in check during long work or study sessions. After searching for a free, simple solution and finding none that met my needs, I decided to create my own. This posture reminder tool was born out of necessity.\n\n"
    
    "### How the Tool Works\n\n"
    "Built using advanced technologies like OpenCV, customtkinter, and plyer for cross-platform notifications, the application uses a webcam to monitor head position in real-time. It gently reminds users when their posture needs correction, helping them maintain healthier habits while using their computers.\n\n"
    
    "### Simple, Accessible, and Free\n\n"
    "What sets this tool apart is its simplicity and accessibility. Many posture tools on the market come with complex features or expensive subscriptions. I wanted to create something that is not only effective but also free and accessible to everyone. The goal was to create an intuitive, lightweight, and non-intrusive solution that could easily fit into anyone’s daily routine.\n\n"
    
    "### Designed to Make an Impact\n\n"
    "With over 80% of people experiencing back pain due to poor posture, this tool is designed to make a significant impact. It provides consistent reminders to help users develop better posture habits over time, preventing the long-term effects of poor posture.\n\n"
    
    "### Technical Highlights\n\n"
    "This project demonstrates my ability to identify a common problem, design a user-friendly solution, and implement it using cutting-edge technologies. The tool is cross-platform and lightweight, ensuring it runs seamlessly in the background, allowing users to continue working or studying without interruption.\n\n"
    
    "### My Passion for Problem-Solving\n\n"
    "This project reflects my passion for solving real-world problems through innovative and accessible technology. It showcases my dedication to developing practical applications that can improve everyday life, making it easier for people to maintain healthy habits in a digital world.\n\n"
    
    "### A Tool for Everyone\n\n"
    "Ultimately, this posture reminder tool is not just for individuals concerned about their posture—it’s for anyone who spends time working or studying on their computer and wants a simple, effective solution to protect their long-term health. I hope this tool helps users not only improve their posture but also enjoy a healthier, more comfortable life."
)


    about_text.configure(state="disabled")  # Make the text read-only

    # Add a button to return to the main menu
    back_button = ctk.CTkButton(frame, text="Back", command=load_main_menu)
    back_button.pack(pady=10)

def load_main_menu():
    """Load the main menu with buttons and restore window size."""
    root.geometry("600x400")  # Restore original window size
    frame.pack_propagate(True)  # Allow frame to resize automatically
    clear_frame()

    title_label = ctk.CTkLabel(frame, text="Posture Reminder", font=("Arial", 20))
    title_label.pack(pady=10)

    # Add buttons back to the frame
    global use_button
    use_button = ctk.CTkButton(frame, text="Use", command=start_posture_reminder_gui, height=40, width=200)
    use_button.pack(pady=10)

    how_to_use_button = ctk.CTkButton(frame, text="How to Use", command=show_how_to_use, height=40, width=200)
    how_to_use_button.pack(pady=10)

    about_button = ctk.CTkButton(frame, text="About Project", command=show_about_project, height=40, width=200)
    about_button.pack(pady=10)

    exit_button = ctk.CTkButton(frame, text="Exit", command=exit_program, height=40, width=200)
    exit_button.pack(pady=10)

def exit_program():
    root.quit()

# Create the main application window using customtkinter
root = ctk.CTk()
root.title("Posture Reminder Application")
root.geometry("600x400")  # Initial window size

# Add a frame to organize buttons
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Load the main menu when the app starts
load_main_menu()

root.mainloop()
