import PySimpleGUI as sg 
from tkinter import font
from datetime import datetime
import os

sg.ChangeLookAndFeel('Dark')
themes = sg.ListOfLookAndFeelValues()
filename = None

menu_layout = [['File',['New','Open','Save','Save As','---','Exit']],
               ['Edit',['Undo','---','Cut','Copy','Paste','Delete','---','Find...','Find Next','Replace...','Go To','---','Select All','Time/Date']],
               ['Format',['Font','Theme',themes]],
               ['Run',['Python Shell','Run Module']],
               ['Help',['View Help','---','About Izzypad 1.0']]]

window_layout = [[sg.Menu(menu_layout)],
          [sg.Text('> New File <', key='_INFO_',font=('Consolas',11), text_color='light gray', size=(150,1))],
          [sg.Multiline(font=('Consolas', 12), key='_BODY_', auto_size_text=True, size=(150,20))],
          [sg.Output(size=(150,12), font=('consolas',12))]]

window = sg.Window('Text//Code Editor', window_layout, resizable=True, margins=(0,0), return_keyboard_events=True).finalize()

#----------FILE OPEN & SAVE FUNCTIONS----------#

def save_file(filename):
    ''' save file instantly if already open; otherwise use `save-as` popup '''
    if filename not in (None,''):
        with open(filename,'w') as f:
            f.write(values['_BODY_'])
        window['_INFO_'].update(value=filename.replace('/',' > '))
    else:
        save_file_as()

def save_file_as():
    ''' save new file or save existing file with another name '''
    filename = sg.popup_get_file('Save File', save_as=True, no_window=True)
    if filename not in (None,''):
        with open(filename,'w') as f:
            f.write(values['_BODY_'])
        window['_INFO_'].update(value=filename.replace('/',' > '))

def new_file():
    ''' return info bar to default settings '''
    window['_BODY_'].update(value='')
    window['_INFO_'].update(value='> New File <')

def open_file():
    '''open a new file'''
    filename = sg.popup_get_file('File Name:', title='Open', no_window=True)
    if filename not in (None,''):
        with open(filename,'r') as f:
            file_text = f.read()
        window['_BODY_'].update(value=file_text)
        window['_INFO_'].update(value=filename.replace('/',' > '))

#----------FORMAT FUNCTIONS----------#

def timestamp():
    ''' add the timestamp to the end of the body text '''
    timestamp = datetime.now().strftime("%T %D")
    new_body = values['_BODY_'] + timestamp
    window['_BODY_'].update(value=new_body)    

font_list = sorted([f for f in font.families() if f[0]!='@'])
font_sizes = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]
font_name = 'Consolas'
font_size = 12

def change_font():
    '''Change the font in the main multiline element'''
    global font_name, font_size
    font_layout = [[sg.Combo(font_list, key='_FONT_', default_value=font_name), 
                    sg.Combo(font_sizes, key='_SIZE_', default_value=font_size)],[sg.OK(), sg.Cancel()]]
    font_window = sg.Window('Font', font_layout, size=(350,80))
    font_event, font_values = font_window.read()
    if font_event not in (None,'Exit'):
        font_name, font_size = (font_values['_FONT_'], font_values['_SIZE_'])
        window['_BODY_'].update(font=(font_name, font_size))
    font_window.close()

#------------RUN FUNCTIONS-----------#    

def run_module(filename):
    '''the open script'''
    print(f'Running Session >> {filename}')
    print('-'*80)
    try:
        exec(open(filename).read())
    except:
        exec(values['_BODY_']) # need to fix for invalid python code
 
#---------MAIN EVENT LOOP----------#

while True:
    event, values = window.read()
    if event in (None,'Exit'):
        break
    if event == 'Open':
        open_file()
    if event in('Save',):
        save_file(filename)
    if event == 'Save As':
        save_file_as()
    if event == 'New':
        new_file()        
    if event in ('Run Module','F5:116'):
        run_module(filename)
    if event in themes:
        sg.change_look_and_feel(event)
    if event == 'Font':
        change_font()
    if event == 'Time/Date':
        timestamp()