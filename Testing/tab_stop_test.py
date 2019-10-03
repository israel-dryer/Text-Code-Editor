import PySimpleGUI as sg 
import tkinter.font as tkfont

window = sg.Window('win', layout=[[sg.Multiline(key='msg', size=(25,5)),sg.Button('Run Code',key='run')]], finalize=True)
font = tkfont.Font(font=window['msg'].Font[0])
tab_width = font.measure(' '*4)
window['msg'].Widget.configure(tabs=(tab_width,))

while True:
    event, values = window.read()
    if event is None:
        break
    else:
        msg = values['msg']
        print(msg, len(msg))
        exec(msg)
        with open('result.txt','w') as f:
            f.write(values['msg'])        
