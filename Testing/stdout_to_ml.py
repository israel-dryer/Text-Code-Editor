import PySimpleGUI as sg 
import sys 
from tkinter import END as tkEND

window = sg.Window('app', [[sg.Multiline(key='OUT'), sg.Button('Push')]])


class RedirectText:
    def __init__(self, window):
        ''' constructor '''
        self.window = window
        self.saveout = sys.stdout

    def write(self, string):
        self.window['OUT'].Widget.insert(tkEND, string)

    def flush(self):
        sys.stdout = self.saveout
        sys.stdout.flush()

# save output
saveout = sys.stdout
redir = RedirectText(window)
sys.stdout = redir


while True:
    event, values = window.read()
    if event is None:
        break
    else:
        print(event, values)
