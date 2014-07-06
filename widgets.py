#!/usr/bin/env python
import Tkinter as tk


#Application class must inherit from Tkinters Frame class
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
    
    def createWidgets(self):
        
        self.quitButton = tk.Button(self, text='Quit',command=self.quit)
        self.quitButton.grid(row=1, column=2)

        self.canvas = tk.Canvas(bg='blue')
        self.canvas.grid(row=0,column=3)


app = Application()
app.master.title('Sample application')
app.mainloop()