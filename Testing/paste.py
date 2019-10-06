import PySimpleGUI as sg 

window = sg.Window('paste', [[sg.Multiline(key='OUT'), sg.Button('Paste')]], finalize=True)

def paste(window, values):
    new = window.TKroot.clipboard_get()
    old = values['OUT']
    window['OUT'].update(value=new + old)

while True:
    event, values = window.read()
    if event is None:
        break
    if event == 'Paste':
        try:
            paste(window, values)
        except:
            continue
