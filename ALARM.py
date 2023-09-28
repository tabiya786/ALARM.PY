import tkinter as tk
import time
import pygame
import threading

# Global variables
alarms = []  # Store alarm data as tuples (hour, minute, am_pm, label)
stopwatch_running = False
stopwatch_start_time = 0
stopwatch_elapsed_time = 0  # Initialize stopwatch_elapsed_time

def set_alarm():
    alarm_hour = hour_var.get()
    alarm_minute = minute_var.get()
    alarm_am_pm = time_format_var.get()
    label_text = label_var.get()
    
    if alarm_am_pm == "PM":
        alarm_hour += 12
    
    alarm_time = f"{alarm_hour:02d}:{alarm_minute:02d} {alarm_am_pm}"
    
    if alarm_time in alarms:
        alarm_label.config(text="Alarm already set for this time")
    else:
        alarms.append((alarm_hour, alarm_minute, alarm_am_pm, label_text))
        update_alarm_list()
        label_label.config(text=f"Label: {label_text}")
        alarm_label.config(text=f"Alarm set for {alarm_time}")
        set_alarm_button.config(state=tk.DISABLED)
        # Clear the label entry field
        label_entry.delete(0, tk.END)
        # Re-enable the "Set Alarm" button
        set_alarm_button.config(state=tk.NORMAL)

def delete_alarm():
    global alarms
    alarms = []  # Clear the alarms list
    update_alarm_list()
    alarm_label.config(text="")  # Clear the alarm label text
    # Reset placeholders
    hour_var.set(0)  # Reset the hour input field to 0
    minute_var.set(0)  # Reset the minute input field to 0
    time_format_var.set("AM")  # Reset the time format to AM
    label_var.set("")  # Reset the label text
    # Re-enable the "Set Alarm" button
    set_alarm_button.config(state=tk.NORMAL)

def update_alarm_list():
    alarm_listbox.delete(0, tk.END)
    for i, alarm in enumerate(alarms):
        hour, minute, am_pm, label_text = alarm
        alarm_time = f"{hour:02d}:{minute:02d} {am_pm}"
        alarm_listbox.insert(tk.END, f"{i + 1}. {alarm_time} -  {label_text or 'No Label'}")

def start_stop_stopwatch():
    global stopwatch_running, stopwatch_start_time, stopwatch_elapsed_time
    if not stopwatch_running:
        stopwatch_running = True
        if stopwatch_start_time == 0:
            stopwatch_start_time = time.time() - stopwatch_elapsed_time
        update_stopwatch()
        start_stopwatch_button.config(text="Stop")
    else:
        stopwatch_running = False
        start_stopwatch_button.config(text="Start")

def reset_stopwatch():
    global stopwatch_running, stopwatch_start_time, stopwatch_elapsed_time
    stopwatch_running = False
    start_stopwatch_button.config(text="Start")
    stopwatch_start_time = time.time()
    stopwatch_elapsed_time = 0
    stopwatch_label.config(text="00:00:00")  # Reset the stopwatch display

def update_stopwatch():
    if stopwatch_running:
        current_time = time.time()
        elapsed_time = current_time - stopwatch_start_time
        stopwatch_display = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        stopwatch_label.config(text=stopwatch_display)
        stopwatch_label.after(1000, update_stopwatch)

def check_alarms():
    while True:
        current_time = time.strftime("%I:%M %p")  # Display time in AM/PM format
        for alarm in alarms:
            hour, minute, am_pm, label_text = alarm
            alarm_time = f"{hour:02d}:{minute:02d} {am_pm}"
            if current_time == alarm_time:
                alarm_label.config(text=f"Alarm is ringing! - {label_text or 'No Label'}")
                time.sleep(60)  # Snooze alarm for 1 minute
        time.sleep(1)

app = tk.Tk()
app.title("Alarm Clock")

# Alarm frame
alarm_frame = tk.Frame(app)
alarm_frame.pack()

hour_label = tk.Label(alarm_frame, text="Hour:")
hour_label.grid(row=0, column=0, padx=5, pady=5)

minute_label = tk.Label(alarm_frame, text="Minute:")
minute_label.grid(row=0, column=2, padx=5, pady=5)

hour_var = tk.IntVar()
hour_entry = tk.Entry(alarm_frame, textvariable=hour_var, width=3)
hour_entry.grid(row=0, column=1, padx=5, pady=5)

minute_var = tk.IntVar()
minute_entry = tk.Entry(alarm_frame, textvariable=minute_var, width=3)
minute_entry.grid(row=0, column=3, padx=5, pady=5)

time_format_var = tk.StringVar()
time_format_var.set("AM")  # Default to AM

am_radio = tk.Radiobutton(alarm_frame, text="AM", variable=time_format_var, value="AM")
am_radio.grid(row=0, column=4, padx=5, pady=5)

pm_radio = tk.Radiobutton(alarm_frame, text="PM", variable=time_format_var, value="PM")
pm_radio.grid(row=0, column=5, padx=5, pady=5)

set_alarm_button = tk.Button(alarm_frame, text="Set Alarm", command=set_alarm)
set_alarm_button.grid(row=0, column=6, padx=5, pady=5)

label_label = tk.Label(alarm_frame, text="Label:")
label_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

label_var = tk.StringVar()
label_entry = tk.Entry(alarm_frame, textvariable=label_var, width=30)
label_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=4)

alarm_label = tk.Label(alarm_frame, text="", font=("Helvetica", 12))
alarm_label.grid(row=2, column=0, columnspan=7, padx=5, pady=5)

# Alarm listbox
alarm_listbox = tk.Listbox(alarm_frame, selectmode=tk.SINGLE, width=50, height=5)
alarm_listbox.grid(row=3, column=0, columnspan=7, padx=5, pady=5)
update_alarm_list()

delete_alarm_button = tk.Button(alarm_frame, text="Delete Alarm", command=delete_alarm)
delete_alarm_button.grid(row=4, column=0, columnspan=7, padx=5, pady=5)

# Stopwatch frame
stopwatch_frame = tk.Frame(app)
stopwatch_frame.pack()

stopwatch_label = tk.Label(stopwatch_frame, text="00:00:00", font=("Helvetica", 24))
stopwatch_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

start_stopwatch_button = tk.Button(stopwatch_frame, text="Start", command=start_stop_stopwatch)
start_stopwatch_button.grid(row=1, column=0, padx=5, pady=5)

reset_stopwatch_button = tk.Button(stopwatch_frame, text="Reset", command=reset_stopwatch)
reset_stopwatch_button.grid(row=1, column=1, padx=5, pady=5)

# Start checking the alarms in a separate thread
alarm_thread = threading.Thread(target=check_alarms)
alarm_thread.daemon = True
alarm_thread.start()

app.mainloop()
