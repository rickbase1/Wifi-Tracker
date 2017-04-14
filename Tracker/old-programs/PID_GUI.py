import tkinter
from tkinter import *


root = Tk()
root.title('PID Tuning')
Label(text='PID Input Values').pack(side=TOP,padx=10,pady=10)

entry = Entry(root, width=10)
entry.pack(side=TOP,padx=10,pady=10)

def PID_parameters():
    P = entry.get()
    I = entry.get()
    D = entry.get()
    '''for row in range(int(y)):
        for col in range(int(x)):
    '''
    print((P, I, D))
    
Button(root, text='Update', command=PID_parameters).pack(side=LEFT)
Button(root, text='CLOSE').pack(side= RIGHT)

Button(root, command=startDemo).grid(row=0, column=0)
Label(root, textvariable = var1).grid(row=1, column=0)
root.mainloop()
