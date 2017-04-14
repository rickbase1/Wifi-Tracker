import tkinter, time
from tkinter import *

#declare vars for readability
var1 = StringVar()
velocityOfBall = 0
gravity = 9.8

root = Tk()

def startDemo():
    while True:
        velocityOfBall += gravity
        var1.set("Velocity: " + velocityOfBall)
        time.sleep(1)

button1 = Button(root, command=startDemo).grid(row=0, column=0)
label1 = Label(root, textvariable = var1).grid(row=1, column=0)

root.mainloop()
