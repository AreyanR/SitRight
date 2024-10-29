import customtkinter as ctk
import cv2
import numpy as np
import time
import platform
import subprocess
from tkinter import messagebox
from plyer import notification
from PIL import Image, ImageTk  # To handle GIF images
import tkinter as tk

# Function to show system notification for SitRight (cross-platform)
def show_posture_reminder():
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

def get_avg_head_height(faces):
    """ Returns the average head height from the detected faces. """
    head_heights = [h for (x, y, w, h) in faces if h > 50]
    if len(head_heights) > 0:
        return int(np.mean(head_heights))
    return None

def start_posture_reminder_gui():
    global use_button
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
    baseline_head_height, baseline_head_position = None, None
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
                if (avg_head_height is not None and avg_head_height < baseline_head_height - 30 or 
                    current_head_position > baseline_head_position + 30) and \
                    (current_time - last_reminder_time > cooldown_period):
                    print("Warning: Please adjust your posture!")
                    show_posture_reminder()
                    last_reminder_time = current_time

        # Always show instructions for quitting and setting baseline
        cv2.putText(frame, 'Press "Q" to quit', (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, 'Press "b" to set baseline posture', (10, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow('SitRight', frame)

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
    root.geometry("600x500")
    frame.pack_propagate(False)
    clear_frame()

    how_to_use_title = ctk.CTkLabel(frame, text="How to Use", font=("Helvetica", 30, "bold"))
    how_to_use_title.pack(pady=10)

    how_to_use_text = ctk.CTkTextbox(frame, width=600, height=300)
    how_to_use_text.pack(pady=10, expand=True, fill="both")

    how_to_use_text.insert("1.0", 
    "Step 1: Start the Program\n"
    )

    how_to_use_text.configure(state="disabled")

    back_button = ctk.CTkButton(frame, text="Back", command=load_main_menu, fg_color="#FF8C00", hover_color="#CC7000", font=bold_font)
    back_button.pack(pady=10)

def show_about_project():
    root.geometry("600x500")
    frame.pack_propagate(False)
    clear_frame()

    about_title = ctk.CTkLabel(frame, text="About the Project", font=("Helvetica", 30, "bold"))
    about_title.pack(pady=10)

    about_text = ctk.CTkTextbox(frame, width=600, height=300)
    about_text.pack(pady=10, expand=True, fill="both")

    about_text.insert("1.0", 
    "### Addressing a Modern-Day Problem\n\n"
    )

    about_text.configure(state="disabled")

    back_button = ctk.CTkButton(frame, text="Back", command=load_main_menu, fg_color="#FF8C00", hover_color="#CC7000", font=bold_font)
    back_button.pack(pady=10)

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

    title_label = ctk.CTkLabel(frame, text="SitRight ", font=("Helvetica", 36, "bold" , "italic"))
    title_label.pack(pady=10)

    global use_button
    use_button = ctk.CTkButton(frame, text="Use", command=start_posture_reminder_gui, height=40, width=200, fg_color="#FF8C00", hover_color="#CC7000", font=bold_font)
    use_button.pack(pady=10)

    how_to_use_button = ctk.CTkButton(frame, text="How to Use", command=show_how_to_use, height=40, width=200, fg_color="#FF8C00", hover_color="#CC7000", font=bold_font)
    how_to_use_button.pack(pady=10)

    about_button = ctk.CTkButton(frame, text="About Project", command=show_about_project, height=40, width=200, fg_color="#FF8C00", hover_color="#CC7000", font=bold_font)
    about_button.pack(pady=10)

    exit_button = ctk.CTkButton(frame, text="Exit", command=exit_program, height=40, width=200, fg_color="#FF8C00", hover_color="#CC7000", font=bold_font)
    exit_button.pack(pady=10)

def exit_program():
    root.quit()

# Splash Screen Function
def show_splash_screen():
    splash_root = tk.Toplevel(root)
    splash_root.overrideredirect(True)
    splash_root.geometry(f"600x400+{(splash_root.winfo_screenwidth() - 600) // 2}+{(splash_root.winfo_screenheight() - 400) // 2}")
    splash_root.configure(bg="#2b2b2a")  # Set splash screen background to grey

    # Load and resize the GIF image
    gif_image = Image.open("splashscreen1.gif")
    gif_frames = []
    try:
        while True:
            gif_frames.append(ImageTk.PhotoImage(gif_image.copy().resize((200, 175), Image.Resampling.LANCZOS)))
            gif_image.seek(len(gif_frames))
    except EOFError:
        pass

    # Display GIF animation
    gif_label = tk.Label(splash_root, bg="#2b2b2a")  # Set background to grey
    gif_label.place(relx=0.5, rely=0.5, anchor='center')
    animate_gif(gif_label, gif_frames, 0)

    # Loading label for animated text
    loading_label = tk.Label(splash_root, text="Loading", font=("Helvetica", 20, "bold"), bg="#2b2b2a", fg="white")
    loading_label.place(relx=0.5, rely=0.8, anchor='center')

    # Function to animate loading text
    def animate_loading_text(label, count=0):
        dots = "." * (count % 4)  # Cycle between no dots, 1 dot, 2 dots, and 3 dots
        label.config(text=f"Loading{dots}")
        label.after(500, animate_loading_text, label, count + 1)

    # Start the loading text animation
    animate_loading_text(loading_label)

    # Destroy splash screen and load main menu after 4 seconds
    splash_root.after(4000, lambda: [splash_root.destroy(), load_main_menu()])

# Splash Screen Function
def show_splash_screen():
    splash_root = tk.Toplevel(root)
    splash_root.overrideredirect(True)
    splash_root.geometry(f"600x400+{(splash_root.winfo_screenwidth() - 600) // 2}+{(splash_root.winfo_screenheight() - 400) // 2}")
    splash_root.configure(bg="#2b2b2a")  # Set splash screen background to grey

    # Load and resize the GIF image
    gif_image = Image.open("splashscreen1.gif")
    gif_frames = []
    try:
        while True:
            gif_frames.append(ImageTk.PhotoImage(gif_image.copy().resize((200, 175), Image.Resampling.LANCZOS)))
            gif_image.seek(len(gif_frames))
    except EOFError:
        pass

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

# Set bold font for buttons
bold_font = ("Arial", 15, "bold")

# Add a frame to organize buttons
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Show splash screen and load main menu
show_splash_screen()

root.mainloop()
