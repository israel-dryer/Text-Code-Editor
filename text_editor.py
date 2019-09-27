import PySimpleGUI as sg 
from tkinter import font
import os
from copy import deepcopy

cwd = os.getcwd().replace('\\','/') + '/'
title = 'Izzypad 1.0'
filename = 'untitled.txt'
filepath_name = cwd + filename
infobar = filepath_name.replace('/',' > ')

themes = sg.ListOfLookAndFeelValues()
font_active_window = False

sg.ChangeLookAndFeel('Dark')
menu_layout = [['File',['New','Open','Save','Save As','---','Page Setup','Print','---','Exit']],
               ['Edit',['Undo','---','Cut','Copy','Paste','Delete','---','Find...','Find Next','Replace...','Go To','---','Select All','Time/Date']],
               ['Format',['Word Wrap','Font','Theme',themes]],
               ['View',['Status Bar']],
               ['Run',['Python Shell','Run Module']],
               ['Help',['View Help','---','About Izzypad 1.0']]]

window_layout = [[sg.Menu(menu_layout,)],
          [sg.Text(infobar, key='info',font=('Consolas',12), text_color='light gray', size=(100,1))],
          [sg.Multiline(font=('Consolas', 14), key='BODY', auto_size_text=True, size=(450,20))],
          [sg.Output(size=(500,1), font=('consolas',12))]]

window = sg.Window(title, layout=window_layout, resizable=True, margins=(0,0), size=(1000,600), return_keyboard_events=True).finalize()

#----------FONT ELEMENTS AND FUNCTION----------#
font_list = sorted([f for f in font.families() if f[0]!='@'])
font_sizes = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]

def change_font(font_name, font_size):
    '''Change the font in the main multiline element'''
    font_layout = [[sg.Combo(font_list, key='FONT_NAME', default_value=font_name), 
                    sg.Combo(font_sizes, key='FONT_SIZE', default_value=font_size)],[sg.OK(), sg.Cancel()]]
    font_window = sg.Window('Font', layout=font_layout, size=(350,80))
    font_event, font_values = font_window.read()
    if font_event is None or font_event == 'Exit':
        font_window.close()
    else:
        font_name = font_values.get('FONT_NAME')
        font_size = font_values.get('FONT_SIZE')
        window['BODY'].update(font=(font_name, font_size))
        font_window.close()

def update_infobar():
    '''Update the filepath_name in the infobar'''
    global infobar
    infobar = filepath_name.replace('/',' > ')    
    window['info'].update(value=infobar)  

def save_file_as(window, values):
    '''save file as another file'''
    global filename, filepath_name
    filepath_name = sg.popup_get_file('File Name:', title='Save As', save_as=True, default_extension='txt', default_path=cwd, no_window=True)
    filename = filepath_name.split('/').pop()
    if filepath_name is None or filepath_name == '':
        return
    else:
        with open(filepath_name,'w') as f:
            file_text = values.get('BODY')
            f.write(file_text)
        update_infobar()

def save_file(window, values):
    '''save file if file already exists'''
    if filename == 'untitled.txt':
        save_file_as(window, values)
    else:
        with open(filepath_name,'w') as f:
            f.write(values.get('BODY'))
    update_infobar()

def new_file(window):
    global filename, filepath_name
    filename = 'untitled.txt'
    filepath_name = cwd + filename
    update_infobar()

def open_file(window):
    '''open a new file'''
    global filename, filepath_name
    filepath_name = sg.popup_get_file('File Name:', title='Open', default_path=cwd, initial_folder=cwd, no_window=True)
    filename = filepath_name.split('/').pop()
    if filename is None or filename == '':
        return 
    else:
        with open(filepath_name,'r') as f:
            file_text = f.read()
        window['BODY'].update(value=file_text)
        update_infobar()

def run_module():
    '''the open script'''
    print(f'Running Session >> {filename}')
    print('-'*80)
    try:
        exec(open(filepath_name).read())
    except:
        exec(values.get('BODY'))

while True:
    event, values = window.read()
    if event is None or event =='Exit':
        break
    if event == 'Open':
        open_file(window)
    if event in(['Save','Control_L:17']):
        save_file(window, values)
    if event == 'Save As':
        save_file_as(window, values)
    if event == 'New':
        new_file(window)        
    if event in['Run Module','F5:116']:
        run_module()
    if event in themes:
        pass
    if event == 'Font':
        font_name, font_size = window['BODY'].Font
        change_font(font_name, font_size)

