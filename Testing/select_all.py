import PySimpleGUI as sg 
from tkinter import INSERT

window = sg.Window('paste', [[sg.Multiline(key='OUT'), sg.Button('Select All')]], finalize=True)

def select_all(window):
    window['OUT'].Widget.tag_add("sel","1.0","end")

while True:
    event, values = window.read()
    if event is None:
        break
    if event == 'Select All':
        select_all(window)
