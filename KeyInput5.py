from pynput import keyboard as _kb_
from pynput.keyboard import Controller as _ctrl_
import tkinter as _tk_
from tkinter import *
import json

class keylog():

    def __init__(self, kbinput, dict_path):
        # keyboard object
        self.input = kbinput
        # stores inputs which is used to match the dictionary json file
        self.input_buffer = ''
        
        #json file used to save key replacements
        with open(dict_path) as f:
            self.load_dict = json.load(f)

    def on_press(self, key):
        # replace is the text string used to check with dictionary
        replace = ''

        if key == _kb_.Key.esc:
        # Stop listener and clear text file
            return False

        if key == _kb_.Key.space:
            # once space is hit, the buffer is matched with a dict key and then
            # next step is to use pynput to simulate key presses
            # print(temp_buffer)
            replace = self.load_dict.get(self.input_buffer, False)
            
            if replace != False:
                for i in range(0, len(self.input_buffer)+1):
                    self.input.press(_kb_.Key.backspace)
                    self.input.release(_kb_.Key.backspace)
                self.input.type(replace)
            
            self.input_buffer = ''
            replace = ''
                        
        if key == _kb_.Key.backspace:
            # remove last key from input buffer
            self.input_buffer = self.input_buffer[:-1]
            
        try:
            #add key to input buffer
            self.input_buffer += key.char

        except AttributeError:
            #if special key such as shift or control then ignore
            pass
    
class GUI():

    def __init__(self, parent, keylog_obj, input_obj):
        self.parent = parent
        self.parent.geometry("650x300")
        
        self.frame = _tk_.Frame(parent)
        self.frame.pack()
        
        self.keylogger = keylog_obj
        self.input = input_obj
        
        #Create grid layout
        self.menuLabel  = _tk_.LabelFrame(self.frame, text="Side bar")
        self.menuLabel.grid(column=0, row=0)
        
        self.captureBox = _tk_.LabelFrame(self.frame, text="Capture box")
        self.captureBox.grid(column=1, row=0)
        
        self.snippetBox = _tk_.LabelFrame(self.captureBox, text="Snippets box")
        self.snippetBox.grid(column=0, row=0)
        
        self.buttonBar  = _tk_.LabelFrame(self.captureBox, text="Button Bar")
        self.buttonBar.grid(column=0, row=1)
        
        #Create snippets
        self.snippets = list()
        for key in self.keylogger.load_dict:
            temp_dict = self.keylogger.load_dict
            self.snippets.append(Snippet(self.snippetBox, key, temp_dict[key]))
        self.snippets[-1].disableInput()
        
        #Create side menu
        self.sideMenu = Menubar(self, self.menuLabel, self.snippets)
        
        #Create Add Snippet button            
        self.addSnippet = _tk_.Button(self.buttonBar, text="Add Snippet", command = self.click_addSnippets)
        self.addSnippet.grid(column=2, row=1)
        
        #Create Start button to begin program
        self.initialize = _tk_.Button(self.buttonBar, text='Start', command = self.click_start)
        self.initialize.grid(column=0, row=1)

        #Create Quit button to end program
        self.end = _tk_.Button(self.buttonBar, text='Close', command = self.click_quit)
        self.end.grid(column=1, row=1)
        
    def click_start(self):
        listener = _kb_.Listener(self.keylogger.on_press)
        listener.start()

    def click_quit(self):
        self.input.press(_kb_.Key.esc)
        self.parent.destroy()
    
    def click_addSnippets(self):
        pass
    
    def click_snippet(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        selected_snippet = self.keylogger.load_dict[value]
        self.snippets[-1].updateLabel(value)
        self.snippets[-1].updateReplacement(selected_snippet)

class Snippet():
    def __init__(self, frame, key, value):
        self.name = key
        self.replace = value
        
        #Add Label box
        self.inbox_label = _tk_.LabelFrame(frame, text="Text Replacement Label")
        self.inbox = _tk_.Text(self.inbox_label, width=30, height=10)
        self.inbox.insert(_tk_.END, self.name)
        
        self.inbox_label.grid(column=0, row=0)
        self.inbox.grid(column=0,row=0)

        
        #Add Replacement box
        self.outbox_label = _tk_.LabelFrame(frame, text="Full Replacement")
        self.outbox = _tk_.Text(self.outbox_label, width=30, height=10)
        self.outbox.insert(_tk_.END, self.replace)
        
        self.outbox_label.grid(column=1, row=0)
        self.outbox.grid(column=0,row=0)
        
    def updateLabel(self, dtext):
        self.enableInput()
        self.inbox.delete('1.0', _tk_.END)
        self.inbox.insert(_tk_.END, dtext)
        self.disableInput()
        
    def updateReplacement(self, dtext):
        self.enableInput()
        self.outbox.delete('1.0', _tk_.END)
        self.outbox.insert(_tk_.END, dtext)
        self.disableInput()
        
    def disableInput(self):
        self.inbox.config(state=DISABLED)
        self.outbox.config(state=DISABLED)
        
    def enableInput(self):
        self.inbox.config(state=NORMAL)
        self.outbox.config(state=NORMAL)
    
    def renameSnippet(self, newName):
        self.name = newName

class Menubar():
    def __init__(self, parent, frame, snippets):
        #Add Label box
        self.menubar_Label = _tk_.LabelFrame(frame, text="Snippets")
        self.menubar = _tk_.Listbox(self.menubar_Label, height=15, width=15)
        
        for item in snippets:
            self.menubar.insert(_tk_.END, item.name)
        
        self.menubar.bind('<Double-1>', parent.click_snippet)
        
        self.menubar_Label.pack()

        #Add Scrollbar
        # SB = _tk_.Scrollbar(self.menubar, orient=VERTICAL)
        # SB.pack(side=RIGHT)
        # SB.configure(command=self.menubar.yview)
        # self.menubar.configure(yscrollcommand=SB.set)
        
        self.menubar.pack(fill="both")
        
        
if __name__ == '__main__':
    dict_path = "./_snippets_.json"
    kb_input  = _ctrl_()
    keylogger = keylog(kb_input, dict_path)
    window    = _tk_.Tk()
    TextRep   = GUI(window, keylogger, kb_input)
    
    window.mainloop()
