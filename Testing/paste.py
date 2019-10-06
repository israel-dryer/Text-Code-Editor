import PySimpleGUI as sg 
from tkinter import INSERT

window = sg.Window('paste', [[sg.Multiline(key='OUT'), sg.Button('Paste')]], finalize=True)

def paste(window):
    try:
        clip = window.TKroot.clipboard_get()
    except:
        return
    else:
        window['OUT'].Widget.insert(INSERT, clip)

while True:
    event, values = window.read()
    if event is None:
        break
    if event == 'Paste':
        try:
            paste(window, values)
        except:
            continue
