# import Tkinter as tk
from Tkinter import *
import numpy as np

import subprocess
import signal
import struct
import numpy as np

import threading
import os

import cv2
import cv_bridge

import rospy

import actionlib

global t2

from control_msgs.msg import (
    FollowJointTrajectoryAction,
    FollowJointTrajectoryGoal,
)
from trajectory_msgs.msg import (
    JointTrajectoryPoint,
)

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)

from std_msgs.msg import (
    Header,
    Empty,
)

from sensor_msgs.msg import (
    Image,
)

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

import baxter_interface

from baxter_interface import CHECK_VERSION

LARGE_FONT = ("Verdana", 12)

def send_image():
    """
    Send the image located at the specified path to the head
    display on Baxter.

    @param path: path to the image file to load and send
    """
    path = e1.get()
    img = cv2.imread(path)
    msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
    pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
    pub.publish(msg)
    # Sleep to allow for image to be published.
    rospy.sleep(1)

def worker1():
    os.system('rosrun baxter_interface joint_trajectory_action_server.py --mode velocity')

def record_thread(file_name):
   pass

def record_movment():
   global t2
   file_name = e2.get()
   t2 = subprocess.Popen(['rosrun', 'baxter_examples', 'joint_recorder.py', '-f', file_name])

def play_movment():
   file_name = e2.get()
   subprocess.call(['rosrun', 'baxter_examples', 'joint_trajectory_file_playback.py', '-f', file_name])
   pass

def tuck_arms():
    subprocess.call(['rosrun', 'baxter_tools', 'tuck_arms.py', '-t'])

def untuck_arms():
    subprocess.call(['rosrun', 'baxter_tools', 'tuck_arms.py', '-u'])

def ctrlC():
   global t2
   # process = subprocess.Popen(args = cmd, shell=True,stdout = buff, universal_newlines = True,preexec_fn=os.setsid)
   # process.send_signal(signal.SIGINT)
   # os.kill(os.getpid(), signal.SIGINT)
   try:
      sig = signal.CTRL_C_EVENT
   except AttributeError:
      sig = signal.SIGINT
   t2.send_signal(sig)

print("Initializing node... ")
rospy.init_node("rsdk_joint_trajectory_client" )

subprocess.call(['rosrun', 'baxter_tools', 'tuck_arms.py', '-u'])

t1 = threading.Thread(target=worker1)
t1.start()
threading._sleep(2)

master = Tk()
Label(master, text="Image 2 display").grid(row=0)
Label(master, text="Name of file 2 record/play").grid(row=1)


et = StringVar()
e1 = Entry(master, textvariable = et)
et.set('Face_normal.png')
e2 = Entry(master)

send_image()

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

# Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Show Image', command=send_image).grid(row=0, column=2, sticky=W, pady=4)
Button(master, text='Tuck Arms', command=tuck_arms).grid(row=0, column=3, sticky=W, pady=4)
Button(master, text='Untuck Arms', command=untuck_arms).grid(row=0, column=4, sticky=W, pady=4)
Button(master, text='Play', command=play_movment).grid(row=1, column=4, sticky=W, pady=4)
Button(master, text='Record', command=record_movment).grid(row=1, column=2, sticky=W, pady=4)
Button(master, text='Stop Recording', command=ctrlC).grid(row=1, column=3, sticky=W, pady=4)

mainloop( )