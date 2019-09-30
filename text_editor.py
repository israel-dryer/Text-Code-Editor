import PySimpleGUI as sg 
from tkinter import font
import os

sg.ChangeLookAndFeel('Dark')
themes = sg.ListOfLookAndFeelValues()
filename = None

menu_layout = [['File',['New','Open','Save','Save As','---','Page Setup','Print','---','Exit']],
               ['Edit',['Undo','---','Cut','Copy','Paste','Delete','---','Find...','Find Next','Replace...','Go To','---','Select All','Time/Date']],
               ['Format',['Word Wrap','Font','Theme',themes]],
               ['View',['Status Bar']],
               ['Run',['Python Shell','Run Module']],
               ['Help',['View Help','---','About Izzypad 1.0']]]

window_layout = [[sg.Menu(menu_layout,)],
          [sg.Text('/New File/', key='_INFO_',font=('Consolas',10), text_color='light gray', size=(100,1))],
          [sg.Multiline(font=('Consolas', 12), key='_BODY_', auto_size_text=True, size=(450,20))],
          [sg.Output(size=(500,12), font=('consolas',12))]]


window = sg.Window('Text//Code Editor', layout=window_layout, resizable=True, margins=(0,0), size=(1000,600), return_keyboard_events=True).finalize()

#----------FONT ELEMENTS AND FUNCTION----------#
font_list = sorted([f for f in font.families() if f[0]!='@'])
font_sizes = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]
font_name = 'Consolas'
font_size = 12

def change_font():
    '''Change the font in the main multiline element'''
    global font_name, font_size
    font_layout = [[sg.Combo(font_list, key='_FONT_', default_value=font_name), 
                    sg.Combo(font_sizes, key='_SIZE_', default_value=font_size)],[sg.OK(), sg.Cancel()]]
    font_window = sg.Window('Font', layout=font_layout, size=(350,80))
    font_event, font_values = font_window.read()
    if font_event is None or font_event == 'Exit':
        font_window.close()
    else:
        font_name = font_values.get('_FONT_')
        font_size = font_values.get('_SIZE_')
        window['_BODY_'].update(font=(font_name, font_size))
        font_window.close()

def save_file(filename):
    ''' save file instantly if already open; otherwise use `save-as` popup '''
    if filename is None:
        save_file_as()
    else:
        with open(filename,'w') as f:
            f.write(values.get('_BODY_'))
        window['_INFO_'].update(value=filename)

def save_file_as():
    ''' save new file or save existing file with another name '''
    filename = sg.popup_get_file('Save File', save_as=True, no_window=True)
    if filename is None:
        return
    else:
        with open(filename,'w') as f:
            f.write(values.get('_BODY_'))
        window['_INFO_'].update(value=filename)

def new_file():
    ''' return info bar to default settings '''
    filename = '/New File/'
    window['_INFO_'].update(value=filename)

def open_file():
    '''open a new file'''
    filename = sg.popup_get_file('File Name:', title='Open', no_window=True)
    if filename is None:
        return 
    else:
        with open(filename,'r') as f:
            file_text = f.read()
        window['_BODY_'].update(value=file_text)
        window['_INFO_'].update(value=filename)

def run_module(filename):
    '''the open script'''
    print(f'Running Session >> {filename}')
    print('-'*80)
    try:
        exec(open(filename).read())
    except:
        exec(values.get('_BODY_'))

while True:
    event, values = window.read()
    if event is None or event =='Exit':
        break
    if event == 'Open':
        open_file()
    if event in(['Save']):
        save_file(filename)
    if event == 'Save As':
        save_file_as()
    if event == 'New':
        new_file()        
    if event in['Run Module','F5:116']:
        run_module(filename)
    if event in themes:
        sg.change_look_and_feel(event)
    if event == 'Print':
        pass
    if event == 'Font':
        change_font()