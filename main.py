import threading
from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.ttk as ttk
from PIL import Image, ImageTk, ImageSequence
import matplotlib.pyplot as plt
import time
from tkinter import filedialog
import cv2
import mediapipe as mp
import numpy as np
# import pygame
import math

# Setting up the main window
win = Tk()
win.title("Intelligent Trainer")
win.geometry("1000x600") # width x height

# Initialising the mediapipe pose detector
mp_pose = mp.solutions.pose
pose_video = mp_pose.Pose(static_image_mode = False, model_complexity = 1, enable_segmentation = True, smooth_segmentation = True, smooth_landmarks = True, min_detection_confidence = 0.5, min_tracking_confidence = 0.5)

# switching variables
colors = (0, 0, 255)
exercise = 0

# Initial values of repitions and flags
reps = 0
flag_1 = 0
flag_2 = 0
bar_1 = 0
bar_2 = 0
right_shoulder_per_1 = 0
right_shoulder_per_2 = 0
update_reps = 1

# Initializing the values for Timer
hours = 0
minutes = 0
seconds = 0
flag_3 = 0
flag_4 = 0 # for resume / play
first_time = 0
good = 0
sg = 0
vari = 0
waitt = 0 # for wait after resume

def startmenu(): # Home Page
    pre_im = PhotoImage(file="mmenu1.png")

    can = Canvas(win, width=1000, height=600, bg="light blue")
    can.place(x=0, y=0)
    can.create_image(0, 0, image=pre_im, anchor="nw")

    can.create_text(500, 30, text="Nice to see you again!", fill="white", font=("Comic Sans MS", 20))

    can.create_text(500, 90, text="Intelligent Trainer", fill="white", font=("Comic Sans MS", 30))

    startbutton = Button(win, text="Start Exercise", font=("Tahoma", 20), bg="black", fg="light grey", command = startexercise)
    # place button at centre
    startbutton.place(x=411, y=200)

    dietbutton = Button(win, text="Diet Plans", font=("Tahoma", 20), bg="black", fg="light grey",command = dietplans)
    # place button at centre
    dietbutton.place(x=433, y= 280)

    abutton = Button(win, text="About Us", font=("Tahoma", 20), bg="black", fg="light grey", command = aboutus)
    # place button at centre
    abutton.place(x=437, y= 360)

    qbutton = Button(win, text="Quit", font=("Tahoma", 20), bg="black", fg="light grey", width=5, command = win.destroy)
    # place button at centre
    qbutton.place(x=461, y= 440)

    win.mainloop()

def aboutus():
    about = Tk()
    about.geometry('960x300')
    about.title('About Us')

    about.configure(background='black')

    description = Label(about, fg='snow', bg="black", font='tahoma 12', text="Intelligent Trainer is a CV/ML based application which helps to perform the exercises precisely without any injury.")
    description.place(x=5, y=5)

    about.mainloop()

def dietplans():
    diet = Tk()
    diet.geometry('960x300')
    diet.title('Diet Plans')

    diet.configure(background='black')

    description = Label(diet, fg='snow', bg="black", font='tahoma 12', text="Hello, For customized diet plans, you can contact us at: hashirdev2.0@gmail.com")
    description.place(x=5, y=5)

    diet.mainloop()

def startexercise(): # Select Exercise
    pre_im = PhotoImage(file="mmenu1.png")

    can = Canvas(win, width=1000, height=600, bg="light blue")
    can.place(x=0, y=0)
    can.create_image(0, 0, image=pre_im, anchor="nw")

    # can.create_text(500, 30, text="Nice to see you again!", fill="white", font=("Comic Sans MS", 20))

    can.create_text(500, 90, text="Select Your Exercise", fill="white", font=("Comic Sans MS", 30))

    e1 = Button(win, text="Shoulder Press", font=("Tahoma", 20), bg="black", fg="light grey", command = selectmode1)
    # place button at centre
    e1.place(x=411, y=200)

    e2 = Button(win, text="Bench Press", font=("Tahoma", 20), bg="black", fg="light grey", command = selectmode2)
    # place button at centre
    e2.place(x=428, y= 280)

    e3 = Button(win, text="Push Ups", font=("Tahoma", 20), bg="black", fg="light grey",command = selectmode3)
    # place button at centre
    e3.place(x=445, y= 360)

    b = Button(win, text = 'Back', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 3, command=startmenu)
    b.place(x = 30, y = 20, width=100, height=35)

    win.mainloop()

def selectmode1(): # Shoulder Press
    global win
    global show_result
    global reps 
    global hours 
    global minutes 
    global seconds
    global flag_3
    global good
    global exercise

    show_result = 0
    reps = 0
    hours = 0
    minutes = 0
    seconds = 0
    flag_3 = 0
    good = 0
    exercise = 1

    pre_im = PhotoImage(file="mmenu1.png")

    can = Canvas(win, width=1000, height=600, bg="light blue")
    can.place(x=0, y=0)
    can.create_image(0, 0, image=pre_im, anchor="nw")

    # can.create_text(500, 30, text="Nice to see you again!", fill="white", font=("Comic Sans MS", 20))

    can.create_text(500, 90, text="Select Exercise Mode", fill="white", font=("Comic Sans MS", 30))

    m1 = Button(win, text="Recorded Video", font=("Tahoma", 20), bg="black", fg="light grey", command = m1record)
    # place button at centre
    m1.place(x=411, y=200)

    m2 = Button(win, text="Live Analysis", font=("Tahoma", 20), bg="black", fg="light grey",command = m1live)
    # place button at centre
    m2.place(x=434, y= 280)

    m3 = Button(win, text="Set Goals", font=("Tahoma", 20), bg="black", fg="light grey", command = m1goals)
    # place button at centre
    m3.place(x=453, y= 360)

    b = Button(win, text = 'Back', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 3, command=startexercise)
    b.place(x = 30, y = 20, width=100, height=35)

    win.mainloop()

def m1live():

    # Widgets
    global start_btn
    global reps
    global cap
    global w
    global h
    global hours
    global minutes
    global seconds
    global label1
    global se

    pre_im = PhotoImage(file="mmenu1.png")

    can = Canvas(win, width=1000, height=600, bg="light blue")
    can.place(x=0, y=0)
    can.create_image(0, 0, image=pre_im, anchor="nw")

    frame_1 = Frame(win, width=600, height=400).place(x=170, y=90)

    cap = cv2.VideoCapture(0)

    w = 600
    h = 400

    label1 = Label(frame_1, width=w, height=h)
    label1.place(x=170, y=90)

    start_btn = Button(win, text = 'Start', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 5, command=start1)
    start_btn.place(x = 400, y = 520, width=160, height=55) 

    b = Button(win, text = 'Back', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 3, command=back1)
    b.place(x = 30, y = 20, width=100, height=35)


    threading.Thread(target=live_stream).start()
    # live_stream()

    win.mainloop()

def start1():
    # Setting as Global variables to retain the value of timer
    global reps
    global show_result
    global flag_3
    global good
    global se
    
    timer()
    
    start_btn.configure(text='Pause', font=("Tahoma 14"), command=pause_resume)

    reset_btn = Button(win, text = 'Reset', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 5, command=reset)
    reset_btn.place(x = 210, y = 520, width=160, height=55)


    if show_result == 1:
        results_btn = Button(win, text = 'See Results', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 5, command=results)
        results_btn.place(x = 590, y = 520, width=160, height=55)

def pause_resume():
    global vari
    global win
    global update_reps
    global flag_4
    global waitt

    vari+=1

    if vari % 2 != 0:

        flag_4=1
        start_btn.configure(text="Resume", font=("Tahoma", 14))
        update_reps = 0

    if vari % 2 == 0:

        flag_4=0
        start_btn.configure(text="Pause", font=("Tahoma", 14))
        update_reps = 1 # for resuming from pause
        waitt = 1

    timer()

def reset():
    # Setting global variables to initialize them
    global reps
    global win
    global hours
    global minutes
    global seconds
    global clock

    # Giving the initial value of reps and time
    reps = 0
    hours=0
    minutes=0
    seconds=0

def back1():
    cap.release()
    global win
    win.destroy()

    reb()
    selectmode1()

def reb():
    global win
    global pre_im
    global can
    win = Tk()
    win.title("Intelligent Trainer")
    win.geometry("1000x600") # width x height

    pre_im = PhotoImage(file="mmenu1.png")
    can = Canvas(win, width=1000, height=600)
    can.place(x=0, y=0)
    can.create_image(0, 0, image=pre_im, anchor="nw")

def live_stream():
    # cap = cv2.VideoCapture(0)

    _, frame = cap.read()

    frame = cv2.flip(frame, 1)

    frame, landmarks = detectPose(frame, pose_video, display=False)

    if landmarks:
        frame, _ = classifyPose(landmarks, frame, display=False)
    else:
        win.after(1, live_stream)

    # frame, _ = classifyPose(landmarks, frame, display=False)

    pos = Label(win, text = 'Posture:', bg = "black", fg = "white", font = "Tahoma 20")
    pos.place(x = 800, y = 150, width=160, height=35) 

    lab = Label(win, text = f'{label}', bg = "black", fg = color, font = "Tahoma 20")
    lab.place(x = 800, y = 200, width=160, height=30)  

    rect = Progressbar(win, orient=VERTICAL, length=200, mode="determinate")
    rect.place(x = 60, y = 130, width=40, height=400)
    rect['value'] = bar_2

    per = Label(win, text=f'{int(right_shoulder_per_2)}%',bg = "black", fg = "white", font = "Tahoma 18")
    per.place(x = 42, y = 110, width=78, height=40) 

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(rgb)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage

    win.after(1, live_stream)

def m1record():
    global win
    pre_im = PhotoImage(file="mmenu1.png")

    can = Canvas(win, width=1000, height=600, bg="light blue")
    can.place(x=0, y=0)
    can.create_image(0, 0, image=pre_im, anchor="nw")

    # Setting global variables
    global browse_btn
    global can2
    # global bro

    browse_photo = PhotoImage(file="browse.png")

    Label(image=browse_photo)

    browse_btn = Button(win, image=browse_photo, width=120, height=110, borderwidth = 0, relief="groove", command = browse1)
    browse_btn.place(x=451,y=245)
    # can2.create_window(420, 450, anchor="nw", window=browse_btn)

    bro = Label(win, text = 'Browse Video', bg="black", fg = "white", font = "Tahoma 20")
    bro.place(x = 420, y = 370, width=180, height=60)

    b = Button(win, text = 'Back', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 3, command=selectmode1)
    b.place(x = 30, y = 20, width=100, height=35)

    win.mainloop()

def browse1():  
    global win
    global vid
    global reps
    reps = 0

    win.filename = filedialog.askopenfilename(initialdir="/D:/DL/Tkinter",
    title="Select a Video", filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))
    vid = win.filename
    if (vid != ''):
        play_video1()

def play_video1():

    global win
    global cap
    global w
    global h
    global label1

    frame_1 = Frame(win, width=400, height=400).place(x=300, y=30)

    cap = cv2.VideoCapture(vid)

    bro = Button(win, text="Switch Video", font = "Tahoma 20", bg="black", fg = "white", command=change_video)
    bro.place(x = 420, y = 450)

    w = 400
    h = 400

    label1 = Label(frame_1, width=w, height=h)
    label1.place(x=300, y=30)

    select_img1()

    b = Button(win, text = 'Back', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 3, command=back_browse1)
    b.place(x = 30, y = 20, width=100, height=35)

def select_img1():

    _, frame = cap.read()

    frame = cv2.flip(frame, 0)

    frame, landmarks = detectPose(frame, pose_video, display=False)

    if landmarks:

        # Perform the Pose Classification.
        frame, _ = classifyPose(landmarks, frame, display=False)

    rep = Label(win, text = f'Reps:\n{int(reps):02}', bg="black", fg = "white", font = "Tahoma 20")
    rep.place(x = 100, y = 140, width=170, height=70)

    pos = Label(win, text = 'Posture:', bg="black", fg = "white", font = "Tahoma 20")
    pos.place(x = 100, y = 250, width=160, height=35) 

    lab = Label(win, text = f'{label}', bg="black", fg = color, font = "Tahoma 20")
    lab.place(x = 100, y = 300, width=160, height=30)  

    rect = Progressbar(win, orient=VERTICAL, length=200, mode="determinate")
    rect.place(x = 830, y = 80, width=50, height=450)
    rect['value'] = bar_1

    per = Label(win, text=f'{int(right_shoulder_per_1)}%', bg="black", fg = "white", font = "Tahoma 20")
    per.place(x = 820, y = 30, width=80, height=40) 

    frame = cv2.resize(frame, (w, h))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(rgb)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage

    win.after(1, select_img1)

def back_browse1():
    reps=0
    global win
    win.destroy()

    reb()
    m1record()

def change_video():
    reps=0
    global win
    win.destroy()

    reb()
    browse1()

def m1goals(): # Set your target

    global duration
    global name
    global repitions
    global sets
    global weight
    global show_result
    global sg
    global win
    global pre_im
    global can

    pre_im = PhotoImage(file="mmenu1.png")

    can = Canvas(win, width=1000, height=600, bg="light blue")
    can.place(x=0, y=0)
    can.create_image(0, 0, image=pre_im, anchor="nw")

    can.create_text(500, 90, text="Set Your Target", fill="white", font=("Comic Sans MS", 30))

    name = Entry(win, width=30, bg="light grey", fg="black", relief='groove')
    can.create_text(407, 183, text="Name :", font=("Tahoma", 13), fill="white")
    can.create_window(441, 175, anchor="nw", window = name)
    name.insert(0, "Your_name") # Initial Content
    name.bind("<Button-1>", clearname) # Clearing the content on Single Click

    duration = Entry(win, width=30, bg="light grey", fg="black", relief='groove')
    can.create_text(407, 223, text="Timer :", font=("Tahoma", 13), fill="white")
    can.create_window(441, 215, anchor="nw", window=duration)
    duration.insert(0, "Hours : Minutes : Seconds") # Initial Content
    duration.bind("<Button-1>", cleartime) # Clearing the content on Single Click

    sets = Entry(win, width=30, bg="light grey", fg="black", relief='groove')
    can.create_text(407, 263, text="Sets :", font=("Tahoma", 13), fill="white")
    can.create_window(441, 255, anchor="nw", window=sets)
    sets.insert(0, "Number of sets") # Initial Content
    sets.bind("<Button-1>", clearsets) # Clearing the content on Single Click

    repitions = Entry(win, width=30, bg="light grey", fg="black", relief='groove')
    can.create_text(407, 303, text="Reps :", font=("Tahoma", 13), fill="white")
    can.create_window(441, 295, anchor="nw", window=repitions)
    repitions.insert(0, "Repitions per set") # Initial Content
    repitions.bind("<Button-1>", clearreps) # Clearing the content on Single Click

    weight = Entry(win, width=30, bg="light grey", fg="black", relief='groove')
    can.create_text(407, 343, text="Weight :", font=("Tahoma", 13), fill="white")
    can.create_window(441, 335, anchor="nw", window=weight)
    weight.insert(0, "Weight (KG)") # Initial Content
    weight.bind("<Button-1>", clearweight) # Clearing the content on Single Click

    done = Button(win, text = 'Confirm', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 5, command=confirm)
    done.place(x = 432, y = 390, width=160, height=55)

    reset_btn = Button(win, text = 'Reset', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 5, command=resetgoal1)
    reset_btn.place(x = 432, y = 465, width=160, height=55)
    
    b = Button(win, text = 'Back', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 3, command=selectmode1)
    b.place(x = 30, y = 20, width=100, height=35)

    show_result = 1
    sg = 1

    win.mainloop()

def confirm():

    # global settings
    global temp_name
    global temp_weight
    global temp_repitions
    global temp_sets
    global duration
    global hours
    global minutes
    global seconds

    temp_name = str(name.get())
    temp_weight = int(weight.get())
    temp_repitions = int(repitions.get())
    temp_sets = int(sets.get())
    temp = duration.get()

    temp_2=temp.split(":")
  
    hours = int(temp_2[0])
    minutes = int(temp_2[1])
    seconds = int(temp_2[2])

    m1live()

def clearname(event):
    
    if name.get() == 'Your_name':
        name.delete(0, END)

def cleartime(event):
    
    if duration.get() == 'Hours : Minutes : Seconds':
        duration.delete(0, END)

def clearreps(event):
        
        if repitions.get() == 'Repitions per set':
            repitions.delete(0, END)

def clearsets(event):
        
        if sets.get() == 'Number of sets':
            sets.delete(0, END)

def clearweight(event):
        
        if weight.get() == "Weight (KG)":
            weight.delete(0, END)

def resetgoal1():
    global win
    win.destroy()

    reb()
    m1goals()

def results(): # Show Results

    global hours
    global minutes
    global seconds
    global reps
    global good
    global se
    global clock
    global win
    global pre_im
    global can

    global temp_name
    global temp_weight
    global temp_repitions
    global temp_sets

    total_time = (((hours_2 - hours) * 60) + (minutes_2 - minutes) + int((seconds_2 - seconds) / 60 )) # Total time in minutes
    burnt_calories = int(total_time * temp_weight * 3.6)

    cap.release()

    if good == 1:
        can.create_text(500, 90, text="Target Achieved", fill="white", font=("Comic Sans MS", 30))
        can.create_text(500, 150, text = f"Well done, Mr. {temp_name}!", fill="white", font=("Tahoma", 18))

    elif good == 0:
        can.create_text(500, 90, text="Target Not Achieved", fill="white", font=("Comic Sans MS", 30))
        can.create_text(500, 150, text = f"Try Again, Mr. {temp_name}!", fill="white", font=("Tahoma", 18))

    can.create_text(500, 240, text = f"Your Results are as follows:", fill="white", font=("Tahoma bold", 16))

    can.create_text(500, 300, text = f"Workout Duration : {hours_2-hours:02}:{minutes_2-minutes:02}:{(seconds_2-seconds)-1:02}", fill="white", font=("Tahoma bold", 14))

    can.create_text(500, 335, text = f"Sets Completed : {se}/{temp_sets}", fill="white", font=("Tahoma bold", 14))

    can.create_text(500, 370, text = f"Total Repitions : {int(se * temp_repitions + reps):02}", fill="white", font=("Tahoma bold", 14))

    can.create_text(500, 405, text = f"Weights Lifted : {temp_weight} KG", fill="white", font=("Tahoma bold", 14))

    can.create_text(500, 440, text = f"Calories Burnt : {burnt_calories} Kcal", fill="white", font=("Tahoma bold", 14))

    b = Button(win, text = 'Back', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 3, command=back_results)
    b.place(x = 30, y = 20, width=100, height=35)

    hours=0
    minutes=0
    seconds=0

    win.mainloop()

def back_results():
    global win
    win.destroy()

    reb()
    startmenu()

def selectmode2(): # Bench Press
    global win
    global show_result
    global reps 
    global hours 
    global minutes 
    global seconds
    global flag_3
    global good
    global exercise

    show_result = 0
    reps = 0
    hours = 0
    minutes = 0
    seconds = 0
    flag_3 = 0
    good = 0
    exercise = 2

    pre_im = PhotoImage(file="mmenu1.png")

    can = Canvas(win, width=1000, height=600, bg="light blue")
    can.place(x=0, y=0)
    can.create_image(0, 0, image=pre_im, anchor="nw")

    # can.create_text(500, 30, text="Nice to see you again!", fill="white", font=("Comic Sans MS", 20))

    can.create_text(500, 90, text="Select Exercise Mode", fill="white", font=("Comic Sans MS", 30))

    m1 = Button(win, text="Recorded Video", font=("Tahoma", 20), bg="black", fg="light grey", command = m1record)
    # place button at centre
    m1.place(x=411, y=200)

    m2 = Button(win, text="Live Analysis", font=("Tahoma", 20), bg="black", fg="light grey",command = m1live)
    # place button at centre
    m2.place(x=434, y= 280)

    m3 = Button(win, text="Set Goals", font=("Tahoma", 20), bg="black", fg="light grey", command = m1goals)
    # place button at centre
    m3.place(x=453, y= 360)

    b = Button(win, text = 'Back', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 3, command=startexercise)
    b.place(x = 30, y = 20, width=100, height=35)

    win.mainloop()

def selectmode3(): # Push Ups
    global win
    global show_result
    global reps 
    global hours 
    global minutes 
    global seconds
    global flag_3
    global good
    global exercise

    show_result = 0
    reps = 0
    hours = 0
    minutes = 0
    seconds = 0
    flag_3 = 0
    good = 0
    exercise = 3

    pre_im = PhotoImage(file="mmenu1.png")

    can = Canvas(win, width=1000, height=600, bg="light blue")
    can.place(x=0, y=0)
    can.create_image(0, 0, image=pre_im, anchor="nw")

    # can.create_text(500, 30, text="Nice to see you again!", fill="white", font=("Comic Sans MS", 20))

    can.create_text(500, 90, text="Select Exercise Mode", fill="white", font=("Comic Sans MS", 30))

    m1 = Button(win, text="Recorded Video", font=("Tahoma", 20), bg="black", fg="light grey", command = m1record)
    # place button at centre
    m1.place(x=411, y=200)

    m2 = Button(win, text="Live Analysis", font=("Tahoma", 20), bg="black", fg="light grey",command = m1live)
    # place button at centre
    m2.place(x=434, y= 280)

    m3 = Button(win, text="Set Goals", font=("Tahoma", 20), bg="black", fg="light grey", command = m1goals)
    # place button at centre
    m3.place(x=453, y= 360)

    b = Button(win, text = 'Back', bg = "black", fg = "white", font = "Tahoma 14", relief = "groove", borderwidth = 3, command=startexercise)
    b.place(x = 30, y = 20, width=100, height=35)

    win.mainloop()

    pass

def detectPose(image, pose, display=True):

    image.flags.writeable = False # make the image read-only
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Convert the image from BGR to RGB.
    results = pose.process(imageRGB) # Make pose detection.
    height, width, _ = image.shape

    if results.pose_landmarks: # If pose landmarks are detected.

        landmarks = [(int(landmark.x * width), int(landmark.y * height), (landmark.z * width)) for landmark in results.pose_landmarks.landmark]
    
        return image, landmarks # Return the image and the landmarks (list of tuples).

def calculateAngle(landmark1, landmark2, landmark3):

    # Unpacking the landmarks into x and y coordinates.
    x1, y1, _ = landmark1 
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)) # Angle between the 3 landmarks.

    if angle < 0:
        angle += 360
    
    return angle

def classifyPose(landmarks, output_image, display=False):

    # Initialising the labels
    global colors
    global color
    global label
    label = 'WRONG'
    color = "red"
    global reps
    global flag_1
    global flag_2
    global bar_1
    global bar_2
    global right_shoulder_per_1
    global right_shoulder_per_2

    if exercise == 1:

        # Calculation of the required angles
        # Get the angle between the left shoulder, elbow and wrist points
        left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value], landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
        
        # Get the angle between the right shoulder, elbow and wrist points
        right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value], landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value], landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])   
        
        # Get the angle between the left elbow, shoulder and hip points
        left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value], landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

        # Get the angle between the right hip, shoulder and elbow points
        right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value], landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

        # Defining rules for the correct posture
        if (80 < (right_shoulder_angle) < 195):

            bar_1 = np.interp((right_shoulder_angle), (105, 160), (0, 100)) # Progress bar
            right_shoulder_per_1 = np.interp(right_shoulder_angle, (90, 160), (0, 100)) # Percentage

            bar_2 = np.interp((right_shoulder_angle), (105, 160), (0, 100))
            right_shoulder_per_2 = np.interp(right_shoulder_angle, (90, 160), (0, 100))

        elif(80 < (360-right_shoulder_angle) < 195):

            bar_1 = np.interp((360-right_shoulder_angle), (105, 160), (0, 100))
            right_shoulder_per_1 = np.interp((360-right_shoulder_angle), (90, 160), (0, 100))

            bar_2 = np.interp((right_shoulder_angle), (105, 160), (0, 100))
            right_shoulder_per_2 = np.interp(right_shoulder_angle, (90, 160), (0, 100))

        # If the both side arms are at 90 degrees
        if (((80 < left_shoulder_angle < 110) and (80 < right_shoulder_angle < 110)) or ((80 < (360-left_shoulder_angle) < 110) and (80 < (360-right_shoulder_angle) < 110))):

            # If shoulders are at the required angle.
            if (((50 < left_elbow_angle < 110) and (50 < right_elbow_angle < 110)) or ((50 < (360-left_elbow_angle) < 110) and (50 < (360-right_elbow_angle) < 110))):

                label='CORRECT'
                flag_1 = 1

        elif (((110 < left_shoulder_angle < 195) and (110 < right_shoulder_angle < 195)) or ((110 < (360-left_shoulder_angle) < 195) and (110 < (360-right_shoulder_angle) < 195))):

            # If shoulders are at the required angle.
            if (((40 < left_elbow_angle < 195) and (40 < right_elbow_angle < 195)) or ((40 < (360-left_elbow_angle) < 195) and (40 < (360-right_elbow_angle) < 195))):

                label='CORRECT'
                flag_2 = 1

    elif exercise == 2:

        # Calculation of the required angles
        # Get the angle between the left shoulder, elbow and wrist points
        left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value], landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
        
        # Get the angle between the right shoulder, elbow and wrist points
        right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value], landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value], landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])  

        # Defining rules for the correct posture
        if (70 < (right_elbow_angle) < 195):

            bar_1 = np.interp((right_elbow_angle), (70, 160), (0, 100))
            right_shoulder_per_1 = np.interp(right_elbow_angle, (70, 160), (0, 100))

            bar_2 = np.interp((right_elbow_angle), (70, 160), (0, 100))
            right_shoulder_per_2 = np.interp(right_elbow_angle, (70, 160), (0, 100))

        elif(70 < (360 - right_elbow_angle) < 195):

            bar_1 = np.interp((360-right_elbow_angle), (70, 160), (0, 100))
            right_shoulder_per_1 = np.interp((360-right_elbow_angle), (70, 160), (0, 100))

            bar_2 = np.interp((right_elbow_angle), (70, 160), (0, 100))
            right_shoulder_per_2 = np.interp(right_elbow_angle, (70, 160), (0, 100))

        if((70 < left_elbow_angle < 195 and 70 < right_elbow_angle < 195)) or ((70 < (360-left_elbow_angle) < 195 and 70 < (360-right_elbow_angle) < 195)):

            if(((abs(right_elbow_angle - left_elbow_angle)) <= 20)): # If the difference between the angles is less than 20 degrees

                if((left_elbow_angle < 100 and  right_elbow_angle < 100)):       

                    label='CORRECT'
                    flag_1 = 1

                if((left_elbow_angle > 140 and  right_elbow_angle > 140)):

                    label='CORRECT'
                    flag_2 = 1

    elif exercise == 3:

        # Calculation of the required angles
        # Get the angle between the left shoulder, elbow and wrist points
        left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value], landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
        
        # Get the angle between the right shoulder, elbow and wrist points
        right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value], landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value], landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])   

        # Get the angle between the left elbow, shoulder and right shoulder points
        left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value], landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])

        # Get the angle between the right elbow, shoulder and left shoulder points
        right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

        # Defining rules for the correct posture
        if (100 < (right_shoulder_angle) < 220):

            bar_1 = np.interp((right_shoulder_angle), (115, 205), (0, 100)) # Progress bar
            right_shoulder_per_1 = np.interp(right_shoulder_angle, (115, 205), (0, 100)) # Percentage

            bar_2 = np.interp((right_shoulder_angle), (115, 205), (0, 100))
            right_shoulder_per_2 = np.interp(right_shoulder_angle, (115, 205), (0, 100))

        elif(100 < (360 - right_shoulder_angle) < 220):

            bar_1 = np.interp((360-right_shoulder_angle), (115, 205), (0, 100))
            right_shoulder_per_1 = np.interp((360-right_shoulder_angle), (115, 205), (0, 100))

            bar_2 = np.interp((right_shoulder_angle), (115, 205), (0, 100))
            right_shoulder_per_2 = np.interp(right_shoulder_angle, (115, 205), (0, 100))


        # If elbows are at the required angle.
        if (((180 < left_elbow_angle < 305) and (180 < right_elbow_angle < 305)) or ((180 < (360-left_elbow_angle) < 305) and (180 < (360-right_elbow_angle) < 305))):

            if(((abs(right_elbow_angle - left_elbow_angle)) <= 15)) and (((abs(right_shoulder_angle - left_shoulder_angle)) <= 15)):

                if((left_elbow_angle < 285 and  right_elbow_angle < 285)):     

                    label='CORRECT'
                    flag_1 = 1

                elif((left_elbow_angle > 295 and  right_elbow_angle > 295)):

                    label='CORRECT'
                    flag_2 = 1

    if exercise == 3:
        if flag_1 == 1 and flag_2 == 1 and update_reps == 1 and bar_1 > 95:

            reps += 1
            flag_1 = 0
            flag_2 = 0

    else:
        if flag_1 == 1 and flag_2 == 1 and update_reps == 1 and bar_1 > 80:

            reps += 1
            flag_1 = 0
            flag_2 = 0

    if label != 'WRONG': # if the pose is classified successfully
        color = "green" # change the color of the text to green for correct posture
        colors = (0, 255, 255)
    else:
        color = "red" # change the color of the text to green for correct posture
        colors = (0, 0, 255)

    # Draw the lines between the landmarks and circles on the landmarks
    cv2.line(output_image, (landmarks[16][0], landmarks[16][1]), (landmarks[14][0], landmarks[14][1]), colors, 3) # Between Right Wrist and Right Elbow
    cv2.line(output_image, (landmarks[12][0], landmarks[12][1]), (landmarks[14][0], landmarks[14][1]), colors, 3) # Between Right Shoulder and Right Elbow

    cv2.line(output_image, (landmarks[15][0], landmarks[15][1]), (landmarks[13][0], landmarks[13][1]), colors, 3)
    cv2.line(output_image, (landmarks[13][0], landmarks[13][1]), (landmarks[11][0], landmarks[11][1]), colors, 3)

    cv2.circle(output_image, (landmarks[12][0], landmarks[12][1]), 10, (0, 0, 0), cv2.FILLED) # Right Shoulder
    cv2.circle(output_image, (landmarks[12][0], landmarks[12][1]), 15, (0, 0, 0), 2)

    cv2.circle(output_image, (landmarks[14][0], landmarks[14][1]), 10, (0, 0, 0), cv2.FILLED) # Right Elbow
    cv2.circle(output_image, (landmarks[14][0], landmarks[14][1]), 15, (0, 0, 0), 2)

    cv2.circle(output_image, (landmarks[16][0], landmarks[16][1]), 10, (0, 0, 0), cv2.FILLED) # Right Wrist
    cv2.circle(output_image, (landmarks[16][0], landmarks[16][1]), 15, (0, 0, 0), 2)

    cv2.circle(output_image, (landmarks[11][0], landmarks[11][1]), 10, (0, 0, 0), cv2.FILLED) # Left Shoulder
    cv2.circle(output_image, (landmarks[11][0], landmarks[11][1]), 15, (0, 0, 0), 2)

    cv2.circle(output_image, (landmarks[13][0], landmarks[13][1]), 10, (0, 0, 0), cv2.FILLED) # Left Elbow
    cv2.circle(output_image, (landmarks[13][0], landmarks[13][1]), 15, (0, 0, 0), 2)

    cv2.circle(output_image, (landmarks[15][0], landmarks[15][1]), 10, (0, 0, 0), cv2.FILLED) # Left Wrist
    cv2.circle(output_image, (landmarks[15][0], landmarks[15][1]), 15, (0, 0, 0), 2)

    return output_image, label

def timer():

    global reps
    global update_reps
    global hours
    global minutes
    global seconds
    global hours_2
    global minutes_2
    global seconds_2
    global clock
    global flag_3
    global flag_4
    global first_time
    global clock
    global good
    global temp_sets
    global se
    global sg
    global waitt

    se = 0

    # Widgets
    if first_time == 0:

        seconds_2 = seconds
        hours_2 = hours
        minutes_2 = minutes


    w9 = Label(win, text = 'Time:', bg = "black", fg = "white", font = "Tahoma 20")
    w9.place(x = 790, y = 40, width=170, height=30)

    clock = Label(win, text='00:00:00', height=2, bg='black', fg='white', font='Tahoma 20')

    clock.place(x=790, y=80, width=170, height=30)        
    clock.config(text=f'{hours:02}:{minutes:02}:{int(seconds):02}')

    if flag_4==0: # when resume button is pressed

        if flag_3 == 0: # if seconds, minutes and hours are not equal to zero
            if seconds == 00: # for set goals timer
                if minutes != 00:
                    minutes -= 1
                    seconds = 59

            if minutes == 00 and seconds == 00:
                if hours != 00:
                    hours -= 1
                    minutes = 59
                    seconds = 59
   
        if seconds == 00 and minutes == 00 and hours == 00: # at start
            flag_3 = 1

        if flag_3 == 1: # when timer is running
            if seconds == 59:
                minutes += 1
                seconds = 00

            if minutes == 59 and seconds == 59:
                hours += 1
                minutes = 00
                seconds = 00

        if flag_3 == 0: # for set goals timer
            if ( seconds != 00 or minutes != 00 or hours != 00):
                if waitt == 1:
                    seconds -= 0.34
                else:
                    seconds-=1

        if flag_3 == 1:
            if waitt == 1:
                seconds += 0.34
            else:
                seconds+=1

        first_time+=1    

    # for targeted exercise
    if sg == 1:
        if reps == temp_repitions:
            se  += 1
            reps = 0

        if se == temp_sets:
            good = 1
            results()

        shw_g = Label(win, text = f'Sets:  {se}/{temp_sets}', bg = "black", fg = "white", font = "Tahoma 20")
        shw_g.place(x = 200, y = 22, width=123, height=30)

    rep = Label(win, text = f'Reps: {int(reps):02}', bg = "black", fg = "white", font = "Tahoma 20")
    rep.place(x = 790, y = 300, width=170, height=30)

    win.after(1000, timer)

startmenu() # Calling the startmenu function







