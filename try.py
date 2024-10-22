import customtkinter as ctk
import time
import threading

def simulate_loading():
    progress_bar.start()  # Start the progress bar animation
    time.sleep(3)  # Simulate loading for 3 seconds
    progress_bar.stop()  # Stop the progress bar animation
    progress_bar.pack_forget()  # Hide the progress bar after loading
    use_button.configure(text="Use", state="normal")  # Reset button text and state

def start_loading():
    use_button.configure(text="Loading...", state="disabled")  # Disable the button
    progress_bar.pack(pady=10)  # Show the progress bar
    threading.Thread(target=simulate_loading).start()  # Run loading in a separate thread

# Create the main application window
root = ctk.CTk()
root.geometry("400x200")

# Create a button that starts the loading
use_button = ctk.CTkButton(root, text="Use", command=start_loading)
use_button.pack(pady=20)

# Create a progress bar (initially hidden)
progress_bar = ctk.CTkProgressBar(root)
progress_bar.pack_forget()  # Hide it until needed

root.mainloop()
