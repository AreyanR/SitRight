import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk  # To handle GIF images
import sys  # To use sys.exit() to cleanly exit the program

# Global variable to track the after() ID for canceling later
after_id = None

def animate_gif(label, gif_frames, frame_index):
    global after_id
    # Function to loop through GIF frames
    frame = gif_frames[frame_index]
    label.config(image=frame)
    frame_index += 1
    if frame_index == len(gif_frames):
        frame_index = 0  # Loop the GIF back to the first frame
    after_id = label.after(500, animate_gif, label, gif_frames, frame_index)  # Change frame every 500 ms

def animate_loading_text(label, text_variants, index):
    # Update the text of the loading label
    label.config(text=text_variants[index])
    index = (index + 1) % len(text_variants)  # Cycle through text variants
    label.after(500, animate_loading_text, label, text_variants, index)  # Change text every 500 ms

def show_splash_screen(root):
    global after_id
    # Create a temporary splash screen window
    splash_root = tk.Toplevel(root)
    splash_root.overrideredirect(True)  # Remove window decorations (title bar, etc.)
    splash_root.geometry("600x400")  # Set splash screen size
    
    # Set the background color to black
    splash_root.configure(bg="black")

    # Create a "SitRight" label at the top, with white text
    title_label = tk.Label(splash_root, text="S i t R i g h t", font=("Helvetica", 30), bg="black", fg="white")
    title_label.place(relx=0.5, rely=0.2, anchor='center')

    # Load the GIF and store all frames, resizing to fit as a splash screen
    gif_image = Image.open("splashscreen.gif")  # Replace with the path to your GIF
    gif_frames = []
    try:
        while True:
            # Resize each frame to a smaller size for the splash screen
            frame = gif_image.copy().resize((175, 175), Image.LANCZOS)  # Resizing to 175x175
            gif_frames.append(ImageTk.PhotoImage(frame))
            gif_image.seek(len(gif_frames))  # Move to the next frame
    except EOFError:
        pass  # End of frames

    # Display the GIF in the center of the window
    gif_label = tk.Label(splash_root, bg="black")
    gif_label.place(relx=0.5, rely=0.5, anchor='center')

    # Animate the GIF
    animate_gif(gif_label, gif_frames, 0)

    # Add the "Loading..." label just below the GIF
    loading_label = tk.Label(splash_root, text="Loading...", font=("Helvetica", 20), bg="black", fg="white")
    loading_label.place(relx=0.5, rely=0.8, anchor='center')

    # Variants of the loading text for animation
    loading_text_variants = ["Loading", "Loading.", "Loading..", "Loading..."]

    # Start animating the loading text
    animate_loading_text(loading_label, loading_text_variants, 0)

    # Close splash screen after 3 seconds and show the main window
    splash_root.after(3000, lambda: [splash_root.destroy(), root.quit()])

    # Start the event loop to show the splash screen
    root.mainloop()

# Create the main application window
def start_main_application():
    root = ctk.CTk()
    root.title("Main Application")
    root.geometry("600x400")

    label = ctk.CTkLabel(root, text="Welcome to the Main Application", font=("Arial", 20))
    label.pack(pady=50)

    # Define a cleanup function to cancel any pending after() callbacks
    def on_close():
        global after_id
        if after_id is not None:
            root.after_cancel(after_id)  # Cancel the after() if it exists
        root.destroy()  # Properly close the window
        sys.exit()  # Fully exit the program to prevent terminal freeze

    root.protocol("WM_DELETE_WINDOW", on_close)  # Handle the window close event

    root.mainloop()

if __name__ == "__main__":
    # Create the hidden root window for the splash screen
    splash_root = tk.Tk()
    splash_root.withdraw()  # Hide it, since we only need the splash screen
    
    # Show the splash screen
    show_splash_screen(splash_root)
    
    # Once the splash screen is done, show the main window
    start_main_application()
