import tkinter as tk
import json

from model import Model

class View:
    def __init__(self, root, model):
        self.root = root
        self.model = model

        self.root.title("Personal Chef")

        self.chat_history = tk.Text(root, state='disabled')
        self.chat_history.pack()

        self.user_input = tk.Entry(root)
        self.user_input.pack()

        self.send_button = tk.Button(root, text="Send", command = self.send_message)
        self.send_button.pack()

        self.conversation = []


        '''self.label = tk.Label(root, text="Enter ingredients or cooking time: ")
        self.label.pack()
        self.entry = tk.Entry(root)
        self.entry.pack()
        self.button = tk.Button(root, text="Get Recipe", command=self.get_recipe)
        self.button.pack()'''

    def send_message(self):
        user_message = self.user_input.get()
        self.user_input.delete(0,'end')

        #display user message in chat history
        self.display_message("Sous Chef: " + user_message)

        #process of generating a response
        output = self.model.generate_response(user_message)
        print(output)
        content = self.model.make_object(output)
        print(content)
        final_response = self.model.generate_response2(output, content, user_message)
        print(final_response)


        # should get the response from controller and model
        self.display_message("Head Chef: " + final_response)


    def display_message(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert('end', message + '\n')
        self.chat_history.config(state='disabled')
        self.chat_history.see('end')


    def get_recipe(self):
        user_input = self.entry.get()
        # pass user input to the controller for processing
