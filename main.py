import os
import openai
import tkinter as tk

# class imports
from controller import Controller
from view import View
from model import Model

def main():
    root = tk.Tk() # create the main application window
    
    model = Model() 
    view = View(root, model)
    controller = Controller(view, model)

    root.mainloop()

if __name__ == "__main__":
    main()
