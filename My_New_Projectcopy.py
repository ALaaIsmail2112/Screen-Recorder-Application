import tkinter
import numpy as np
import cv2
import PIL
import pyautogui
import pyscreeze

from win32api import GetSystemMetrics  # To get the screen resolution # screen dimension
import time
import threading
import os


# Start using Tkinter
window = tkinter.Tk()
window.title('My First Project')

# Make GUI responsive through frames
frame = tkinter.Frame(window)
frame.pack()

### Starting of APPLICATION ###
recording = False  # Default value of recording


## Make First Frame ##
my_list_Frame = tkinter.LabelFrame(frame, text="Screen Recorder")
my_list_Frame.grid(row=0, column=0, padx=30, pady=30, columnspan=2)

# Label
name_of_record_label = tkinter.Label(my_list_Frame, text="Name of Record")
name_of_record_label.grid(row=0, column=0)

# Input
name_of_record_entry = tkinter.Entry(my_list_Frame, width=30)
name_of_record_entry.grid(row=1, column=0, padx=5, pady=7)


### MY Functions

def play_recording(filename):
    os.startfile(filename)  # Startfile function to open the specified file


def generate_unique_filename(record_name):
    """Generates a unique filename based on the record name."""
    count = 1
    while os.path.exists(f"D:\\PythonPogram\\{record_name}({count}).mp4"):
        count += 1
    return f"{record_name}({count}).mp4"


def start_recording():
    global recording, out, prev, filename

    if recording:  # Prevent multiple recordings
        return

    recording = True
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)

    record_name = name_of_record_entry.get().strip()
    if not record_name:
        record_name = "New Record"

    # Generate a unique filename if needed
    filename = generate_unique_filename(record_name)

    out = cv2.VideoWriter(
        filename, cv2.VideoWriter_fourcc(*"mp4v"), 20.0, (width, height)
    )
    prev = 0
    fps = 80

    def record_task():
      global recording
      prev = 0
      while recording:
        try:
            time_elapsed = time.time() - prev
            img = pyautogui.screenshot()
            if time_elapsed > 1.0 / fps:
                prev = time.time()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)

            cv2.waitKey(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            break


    recording_thread = threading.Thread(target=record_task)
    recording_thread.start()

    # Enable the "Start" button and disable the "Stop" button after stopping recording
    submit_btn.config(state=tkinter.DISABLED)
    submit_btn2.config(state=tkinter.NORMAL)


def stop_recording():
    global recording

    if not recording:
        return

    recording = False

    # Enable the "Start" button and disable the "Stop" button after stopping recording
    submit_btn.config(state=tkinter.NORMAL)
    submit_btn2.config(state=tkinter.DISABLED)

    out.release()
    cv2.destroyAllWindows()
    update_record_labels()


def open_folder():
    folder_path = r"D:\PythonPogram"
    os.startfile(folder_path)


def update_record_labels():
    # Clear all elements in the listbox before updating
    records_labels.delete(0, tkinter.END)
    folder_path = r"D:\PythonPogram"
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            records_labels.insert(tkinter.END, os.path.join(folder_path, filename))


##### TKinter


submit_btn = tkinter.Button(my_list_Frame, text="Start", command=start_recording)
submit_btn.grid(row=5, column=0, padx=10, ipadx=40, ipady=10)

submit_btn2 = tkinter.Button(my_list_Frame, text="Stop", command=stop_recording, state=tkinter.DISABLED)
submit_btn2.grid(row=5, column=1, columnspan=2, pady=10, padx=10, ipadx=40, ipady=10)


for widget in my_list_Frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)


my_list_Frame2 = tkinter.LabelFrame(frame , text ="Go To Your Folder")
my_list_Frame2.grid(row =1 , column= 0 , sticky="new" , padx=20 )

submit_btn3 = tkinter.Button(my_list_Frame2 , text = "Open Folder" , command= open_folder)
submit_btn3.grid(row =0, column =0, columnspan=2 , pady =10,padx =10, ipadx=30, ipady = 10)



my_list_Frame3 = tkinter.LabelFrame(frame , text="Your Screen Records" )
my_list_Frame3.grid(row =2 , column= 0 , sticky="new" , padx=20 )


records_labels = tkinter.Listbox(my_list_Frame3 , width=60)
records_labels.grid(row=0, column=0, padx=20, pady=10)

play_button = tkinter.Button(my_list_Frame3, text="Play", command=lambda: play_recording(records_labels.get(tkinter.ACTIVE)))
play_button.grid(row=1, column=0, padx=10, pady=10)

# to print name of files on gui in gui
update_record_labels()

for widget in my_list_Frame3.winfo_children():
    widget.grid_configure(padx=10, pady=10)
#### TKinter

window.mainloop()