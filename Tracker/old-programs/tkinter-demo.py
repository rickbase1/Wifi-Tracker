#!/user/bin/python3
# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, BOTH

class Example(Frame):

    def __init__(self,parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def initUI(self):
    
        self.parent.title("PID Loop Tuner")
        self.pack(fill=BOTH, expand=1)


def main():

    root = Tk()
    root.geometry("450x450+400+200")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
        
