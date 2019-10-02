import PySimpleGUI as sg 
from tkinter import font
from datetime import datetime
import shelve
import os

sg.change_look_and_feel('Black')

# instantiate shelve
app = shelve.open('settings')
app['filename'] = None

def load_settings(window):
    window['_BODY_'](value=app['body'])

def save_settings(values):
    try: # <---------this is not working correctly upon exit
        app['body'] = values['_BODY_']
    except:
        pass

#---------MAIN WINDOW LOOP----------#
def main_loop():
    menu_layout = [['File',['New','Open','Save','Save As','---','Exit']],
            ['Edit',['Undo','---','Cut','Copy','Paste','Delete','---','Find...','Find Next','Replace...','Go To','---','Select All','Time/Date']],
            ['Format',['Font','Theme', app['themes']]],
            ['Run',['Python Shell','Run Module']],
            ['Help',['View Help','---','About Izzypad 1.0']]]

    col1 = sg.Column([[sg.Multiline(font=app['font'], key='_BODY_', auto_size_text=True, size=(150,30))]])
    col2 = sg.Column([[sg.Output(size=(150,10), font=('Consolas', 12))]])               

    window_layout = [[sg.Menu(menu_layout)],
            [sg.Text('> New File <', key='_INFO_',font=('Consolas',11), size=(100,1))],
            [sg.Pane([col1, col2])]]

    window = sg.Window('TextCode Editor', window_layout, resizable=True, margins=(0,0), size=(1200,800), return_keyboard_events=True, finalize=True)
    load_settings(window)

    # main window loop
    while True:
        event, values = window.read()
        if event in (None,'Exit'):
            save_settings(values)
            break
        if event == 'Open':
            open_file(window, event, values)
        if event in('Save',):
            save_file(window, values, app['filename'])
        if event == 'Save As':
            save_file_as(window, values)
        if event == 'New':
            new_file(window)        
        if event in ('Run Module','F5:116'):
            run_module(app['filename'], values)
#        if event == 'Font':
#            change_font(window)
        if event == 'Time/Date':
            timestamp(window, event, values)
        if event in app['themes']:
            sg.change_look_and_feel(event)
            app['theme'] = event
            save_settings(values)
            window.close()
            break
    return event
        

#----------FILE OPEN & SAVE FUNCTIONS----------#

def save_file(window, values, filename):
    ''' save file instantly if already open; otherwise use `save-as` popup '''
    if filename not in (None,''):
        with open(filename,'w') as f:
            f.write(values['_BODY_'])
        window['_INFO_'](value=filename.replace('/',' > '))
    else:
        save_file_as(window, values)

def save_file_as(window, values):
    ''' save new file or save existing file with another name '''
    app['filename'] = sg.popup_get_file('Save File', save_as=True, no_window=True)
    if app['filename'] not in (None,''):
        with open(app['filename'],'w') as f:
            f.write(values['_BODY_'])
        window['_INFO_'](value=app['filename'].replace('/',' > '))

def new_file(window):
    ''' return info bar to default settings '''
    window['_BODY_'](value='')
    window['_INFO_'](value='> New File <')

def open_file(window, event, values):
    '''open a new file'''
    app['filename'] = sg.popup_get_file('File Name:', title='Open', no_window=True)
    if app['filename'] not in (None,''):
        with open(app['filename'],'r') as f:
            file_text = f.read()
        window['_BODY_'](value=file_text)
        window['_INFO_'](value=app['filename'].replace('/',' > '))

#----------FORMAT FUNCTIONS----------#

def timestamp(window, event, values):
    ''' add the timestamp to the end of the body text '''
    timestamp = datetime.now().strftime("%T %D")
    new_body = values['_BODY_'] + timestamp
    window['_BODY_'](value=new_body)    

#font_list = sorted([f for f in font.families() if f[0]!='@'])
#font_sizes = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]

# def change_font(window):
#     '''Change the font in the main multiline element'''
#     font_layout = [[sg.Combo(font_list, key='_FONT_', default_value=app['font'][0]), 
#                     sg.Combo(font_sizes, key='_SIZE_', default_value=app['font'][1])],[sg.OK(), sg.Cancel()]]
#     font_window = sg.Window('Font', font_layout, size=(350,80), keep_on_top=True)
#     font_event, font_values = font_window.read()
#     if font_event not in (None,'Exit'):
#         font_name, font_size = (font_values['_FONT_'], font_values['_SIZE_'])
#         app['font'] = (font_name, font_size)
#         window['_BODY_'](font=app['font'])
#         window.refresh()
#     font_window.close()

#------------RUN FUNCTIONS-----------#    

def run_module(filename, values):
    '''the open script'''
    print(f'Running Session >> {filename}')
    print('-'*30)
    try:
        exec(open(filename).read())
    except:
        exec(values['_BODY_']) # need to fix for invalid python code
 

while True:
    main_event = main_loop()  
    if main_event is None:
        break
    else:
        continue