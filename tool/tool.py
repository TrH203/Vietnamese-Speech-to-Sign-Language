import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
from bone_detect import bone_detect as BD


def windown_setting(root):
    # Set the window size (width x height)
    window_width = 960
    window_height = 720
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position to center the window
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Set the window size and position
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    
    return root
def update_frame():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Resize the frame to the desired dimensions
        frame = cv2.resize(frame, (camera_width, camera_height))
        
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        frame = bd.detect(frame)
        
        
        img = Image.fromarray(frame)
        
        
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Update the label with the new frame
        camera_label.imgtk = imgtk
        camera_label.config(image=imgtk)
    
    # Call update_frame again after N milliseconds
    camera_label.after(10, update_frame)
    return frame

def update_listBox():
    pass
    
    pass
def add_to_history(item):
    pass
    update_listBox()
    
def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)
    
def remove_selected_item():
    pass
# Function to reset the counter
def reset():
    global counter
    counter = 0
    counter_label.config(text=str(counter))  

def submit_text(entry,popup):
        # Function to handle the text submission
        text = entry.get()
        if text:
            main_label.config(text=text)
        popup.destroy()# Close the popup window
        start_countdown(3)
        

def open_popup():
    # Function to open the popup window
    popup = tk.Toplevel(root)
    popup.title("Input Text")

    label = tk.Label(popup, text="Enter your text:")
    label.pack(padx=10, pady=10)

    entry = tk.Entry(popup)
    entry.pack(padx=10, pady=10)
    

    submit_button = tk.Button(popup, text="Submit", command=lambda:submit_text(entry,popup))
    submit_button.pack(pady=10)
    
# def recording():
#     pass

def start_record():
    open_popup()


def start_countdown(count):
    if count >= 0:
        counter_label.config(text=f"Countdown: {count}",font=25)
        root.after(1000, start_countdown, count - 1)
    else:
        counter_label.config(text="")
def stop_record():
    pass
    
# Create Bone detect class
bd = BD()

# Create the main application window
root = tk.Tk()

# Initialize counter variable
counter = 0
# Initialize recording
recording = False

root.title("My Tkinter App")

# > Setting windown
root = windown_setting(root)

# > Create menu bar
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)

# Create a label widget
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

# Set desired width and height for the camera feed
camera_width = 500
camera_height = 360

# Create a label widget to display the camera feed
camera_label = Label(root,width=camera_width,height=camera_height)
camera_label.pack(padx=10,pady=10)

# Create and place the label for displaying the counter value
counter_label = tk.Label(root, text="", font=("Helvetica", 15))
counter_label.pack(pady=10)

# Create a frame to hold the buttons
button_frame = Frame(root)
button_frame.pack(pady=10)

# Create the buttons and pack them side by side
button1 = Button(button_frame, text="Start Record", command=start_record)
button1.pack(side=tk.LEFT, padx=5)

button2 = Button(button_frame, text="Stop Record", command=stop_record)
button2.pack(side=tk.LEFT, padx=5)


main_label = tk.Label(root, text="Waiting for input...")
main_label.pack(pady=10)


# Create a context menu
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Remove", command=remove_selected_item)
context_menu.add_command(label="Edit", command=remove_selected_item)

history = []
history_listbox = Listbox(root,width=700)
history_listbox.pack(padx=10, pady=10)

# Bind the right-click event to the Listbox
history_listbox.bind("<Button-2>", show_context_menu) # > Right click

# Initialize the video capture
cap = cv2.VideoCapture(0)


result = update_frame()


# Run the application
root.mainloop()

cap.release()
cv2.destroyAllWindows()