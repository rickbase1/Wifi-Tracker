import time
from tkinter import *
import config


class App:
    #while True:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        pitch_scale = Scale(frame, from_=0, to=10, orient=HORIZONTAL, command=self.update_pitch)
        pitch_scale.grid(row=0)
        heading_scale = Scale(frame, from_=0, to=360, orient=HORIZONTAL, command=self.update_heading)
        heading_scale.grid(row=1)


    def update_pitch(self, pitch_sp):
        
        config.pitch_sp = pitch_sp
        
    def update_heading(self, heading_sp):
        
        config.heading_sp = heading_sp        
        

root = Tk()
root.wm_title('Antenna1-Tracker Control')
app = App(root)
root.geometry("400x200+0+0")
root.mainloop()
