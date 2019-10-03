import PySimpleGUI as sg 
import shelve
from tkinter import font as tkfont
from datetime import datetime 

settings = shelve.open('settings')
settings.update(filename=None, info=None, body=None)
sg.change_look_and_feel(settings.get('theme'))

def main_window():
    menu_layout = [
        ['File',['New','Open','Save','Save As','---','Exit']],
        ['Edit',['Undo','---','Cut','Copy','Paste','Delete','---','Find...','Replace...','---','Select All','Time/Date']],
        ['Format',['Settings','Font','Theme',[settings['themes']]]],
        ['Run',['Run Module']],
        ['Help',['View Help','---','About Izzypad 1.0']]]

    col1 = sg.Column([[sg.Multiline(font=settings['font'], key='_BODY_', auto_size_text=True, size=(150,20))]])
    col2 = sg.Column([[sg.Output(size=(150,8), font=('Consolas', 12))]])               

    window_layout = [
        [sg.Menu(menu_layout)],
        [sg.Text('> New File <', key='_INFO_',font=('Consolas',11), size=(100,1))],
        [sg.Pane([col1, col2])]]

    window = sg.Window('Text-Code Editor', window_layout, resizable=True, margins=(0,0), size=(1000,600), return_keyboard_events=True, finalize=True)
    
    # load prior settings
    load_settings(window)

    # set the default tabstop to 4 spaces
    change_tabstop(window, settings['tabsize'])

    # main window event loop
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event in ('New','n:78'):
            new_file(window)
        if event in ('Open','o:79'):
            open_file(window)
        if event in ('Save','s:83'):
            save_file(window, values)
        if event in ('Save As',):
            save_file_as(window, values)
        if event in ('Settings',):
            print_settings()
        if event in ('Font',):
            change_font(window)
        if event in settings.get('themes'):
            change_theme(event, values)
            window.close()
            break
        if event in ('Time/Date',):
            timestamp(window, values)
        if event in ('Run Module','F5:116'):
            run_module(values)
    return event

def change_tabstop(window, size): # add ability to change this
    font = tkfont.Font(font=settings.get('font')[0])
    tab_width = font.measure(' '*size)
    window['_BODY_'].Widget.configure(tabs=(tab_width,)) 
    settings.update(tabsize=size)   

def load_settings(window):
    window['_INFO_'].update(value=settings['info'])
    window['_BODY_'].update(value=settings['body'])

def save_settings(values): # might not be needed
    #settings.update(body=values['_BODY_'], info=values['_INFO_'])
    pass

def print_settings():
    print(f"Theme: {settings['theme']}")
    print(f"Font: {settings['font']}\n")

#----------File Menu Functions--------#

def new_file(window): # CTRL+N shortcut key
    window['_BODY_'].update(value='')
    window['_INFO_'].update(value='> New File <')
    settings.update(filename=None, body='', info='> New File <')

def open_file(window): # CTRL+O shortcut key
    filename = sg.popup_get_file('File Name:', title='Open', no_window=True)
    if filename not in (None,''):
        with open(filename,'r') as f:
            file_text = f.read()
        window['_BODY_'].update(value=file_text)
        window['_INFO_'].update(value=filename.replace('/',' > '))
        settings.update(filename=filename, body=file_text, info=filename.replace('/',' > '))

def save_file(window, values): # CTRL+S shortcut key
    filename = settings.get('filename')
    if filename not in (None,''):
        with open(filename,'w') as f:
            f.write(values['_BODY_'])
        window['_INFO_'](value=filename.replace('/',' > '))
        settings.update(filename=filename, info=filename.replace('/',' > '))
    else:
        save_file_as(window, values)

def save_file_as(window, values):
    filename = sg.popup_get_file('Save File', save_as=True, no_window=True)
    if filename not in (None,''):
        with open(filename,'w') as f:
            f.write(values['_BODY_'])
        window['_INFO_'](value=filename.replace('/',' > '))
        settings.update(filename=filename, info=filename.replace('/',' > '))

#----------Edit Menu Functions--------#

def undo(): # CTRL+Z shortcut key
    pass

def cut(): # CTRL+X shortcut key
    pass

def copy(): # CTRL+C shortcut key
    pass

def paste(): # CTRL+V shortcut key
    pass

def delete():
    pass

def find(): # CTRL+F shortcut key
    pass

def replace(): # CTRL+H shortcut key
    pass

def select_all():
    pass

def timestamp(window, values):
    timestamp = datetime.now().strftime("%T %D")
    new_body = values['_BODY_'] + timestamp
    window['_BODY_'](value=new_body)    
    settings.update(body=new_body)

#--------Format Menu Functions--------#
def change_font(window):
    font_list = sorted([f for f in tkfont.families() if f[0]!='@'])
    font_sizes = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]
    font_name, font_size = settings['font']
    font_layout = [
        [sg.Combo(font_list, key='_FONT_', default_value=font_name), 
         sg.Combo(font_sizes, key='_SIZE_', default_value=font_size)],[sg.OK(), sg.Cancel()]]
    font_window = sg.Window('Font', font_layout, size=(350,80), keep_on_top=True)
    font_event, font_values = font_window.read()
    if font_event not in (None,'Exit'):
        font_selection = (font_values['_FONT_'], font_values['_SIZE_'])
        window['_BODY_'].update(font=font_selection)
        settings.update(font=font_selection)
        print(f"Font changed: {(font_name, font_size)} => {font_selection}\n")
    font_window.close()    

def change_theme(event, values):
    settings.update(theme=event, body=values['_BODY_'])
    sg.change_look_and_feel(event)

#-----------Run Menu Functions--------#

def run_module(values): # F5 shortcut key
    print(f"Running session :: {settings['info']}\n")
    try:
        exec(values['_BODY_'])
    except:
        print('Invalid Python Code')

if __name__ == '__main__':
    print('starting program...\n')

    while True:
        main_event = main_window()
        if main_event in (None, 'Exit'):
            break
        else:
            print(main_event)
            continue