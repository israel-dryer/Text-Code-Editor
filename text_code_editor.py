import PySimpleGUI as sg 
from tkinter import font as tkfont
from datetime import datetime
import shelve

##-----SETUP DEFAULT USER SETTINGS-----------------------##

application_active = False
settings = shelve.open('app_settings')

# test for existing shelf and create if not exist
if len(settings.keys())==0:
    settings['theme'] = 'Reddit'
    settings['themes'] = sg.list_of_look_and_feel_values()
    settings['font']=('Consolas', 12)
    settings['tabsize']=4
    settings['filename'] = None
    settings['body'] = ''
    settings['info'] = '> New File <'
    settings['out'] = ''

# default theme or user saved theme
sg.change_look_and_feel(settings['theme'])

def close_settings():
    settings.update(filename=None, body='', info='> New File <')
    settings.close()

##----SETUP GUI WINDOW-----------------------------------##
def main_window(settings):
    menu_layout = [
        ['File',['New','Open','Save','Save As','---','Exit']],
        ['Edit',['Undo','---','Cut','Copy','Paste','Delete','---','Find...','Replace...','---','Select All','Date/Time']],
        ['Format',['Theme', settings['themes'],'Font','Tab Size','Show Settings']],
        ['Run',['Run Module']],
        ['Help',['View Help','---','About Izzypad 1.0']]]

    col1 = sg.Column([[sg.Multiline(default_text=settings['body'], font=settings['font'], key='_BODY_', auto_size_text=True, size=(150,20))]])
    col2 = sg.Column([[sg.Output(size=(150,8), font=('Consolas', 10), key='_OUT_')]])               

    window_layout = [
        [sg.Menu(menu_layout)],
        [sg.Text(settings['info'], key='_INFO_', font=('Consolas',11), size=(100,1))],
        [sg.Pane([col1, col2])]]

    window = sg.Window('Text-Code Editor', window_layout, resizable=True, margins=(0,0), size=(1000,600), return_keyboard_events=True)
    return window

##----FILE MENU FUNCTIONS--------------------------------##

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

##----EDIT MENU FUNCTIONS--------------------------------##

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

def fetch_datetime(window, values):
    ''' append the current date and time into the body '''
    datetime_stamp = datetime.now().strftime("%T %D")
    new_body = values['_BODY_'] + datetime_stamp
    window['_BODY_'].update(value=new_body)    
    settings.update(body=new_body)    

##----FORMAT MENU FUNCTIONS------------------------------##

def change_theme(window, event, values):
    settings.update(theme=event, body=values['_BODY_'])
    sg.change_look_and_feel(event)
    window.close()

def change_font(window):
    ''' change default font on body element and save app settings '''
    # get the default font from user settings
    font_name, font_size = settings.get('font')
    # get available fonts from active window session for combo box
    font_list = sorted([f for f in tkfont.families() if f[0]!='@'])
    # available sizes to use for combo box (restricted to practical sizes)
    font_sizes = [8,9,10,11,12,14]
    # setup the font gui window
    font_layout = [
        [sg.Combo(font_list, key='_FONT_', default_value=font_name), 
         sg.Combo(font_sizes, key='_SIZE_', default_value=font_size)],[sg.OK(), sg.Cancel()]]
    font_window = sg.Window('Font', font_layout, size=(350,80), keep_on_top=True)
    # listen for font selection events
    font_event, font_values = font_window.read()
    if font_event not in (None,'Exit'):
        font_selection = (font_values['_FONT_'], font_values['_SIZE_'])
        # check to see if the font changed
        if font_selection != settings['font']:
            settings.update(font=font_selection)
            window['_BODY_'].update(font=font_selection)
            print(f"Font........... {(font_name, font_size)} => {font_selection}\n")
    font_window.close()

def change_tabsize(window):
    ''' user interface for the set_tabsize function '''
    tab_layout = [[sg.Slider(range=(1,8), default_value=settings['tabsize'], orientation='horizontal', key='_SIZE_'), sg.OK(size=(5,2))]]
    tab_window = sg.Window('Tab Size', tab_layout, keep_on_top=True)
    tab_event, tab_values = tab_window.read()
    if tab_event not in (None, 'Exit'):
        old_tab_size = settings['tabsize']
        new_tab_size = int(tab_values['_SIZE_'])
        # check to see if tab size changed
        if new_tab_size != old_tab_size:
            settings.update(tabsize=new_tab_size)
            set_tabsize(window, new_tab_size)
            print(f"Tab size....... {old_tab_size} => {new_tab_size}\n")

    tab_window.close()

def set_tabsize(window, size=4): # load upon opening after 'finalize=True' is fixed
    ''' adjust the tab size in the body; default is 4 '''
    font = tkfont.Font(font=settings.get('font')[0])
    tab_width = font.measure(' '*size)
    window['_BODY_'].Widget.configure(tabs=(tab_width,)) 
    settings.update(tabsize=size) 

def show_settings():
    print(f"Theme.......... {settings['theme']}")
    print(f"Tab size....... {settings['tabsize']}")
    print( "Font........... {}, {}".format(*settings['font']))
    print(f"Open file...... {settings['filename']}\n")

##----RUN MENU FUNCTIONS---------------------------------##

def run_module(values): # F5 shortcut key
    print('.'*50)
    print(f"Running session :: {settings['info']}\n")
    try:
        exec(values['_BODY_'])
    except:
        print('ERROR!......... Invalid Python Code')
    print('.'*50)

##----MAIN EVENT LOOP------------------------------------##
window = main_window(settings)

while True:
    event, values = window.read(timeout=1)

    # adjust window when application is activated
    if not application_active:
        application_active = True
        show_settings()
        set_tabsize(window)
   
    # listen for window events
    if event in (None, 'Exit'):
        close_settings()
        break
    if event in ('New','n:78'):
        new_file(window)
    if event in ('Open','o:79'):
        open_file(window)
    if event in ('Save','s:83'):
        save_file(window, values)
    if event in ('Save As',):
        save_file_as(window, values)
    if event in ('Date/Time',):
        fetch_datetime(window, values)
    if event in ('Font',):
        change_font(window)
    if event in ('Tab Size',):
        change_tabsize(window)
    if event in ('Show Settings',):
        show_settings()
    if event in ('Run Module', 'F5:116' ):
        run_module(values)
    if event in settings['themes']:
        application_active = False
        change_theme(window, event, values)
        window = main_window(settings)