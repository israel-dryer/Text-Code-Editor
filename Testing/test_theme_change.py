import PySimpleGUI as sg 

themes = sg.list_of_look_and_feel_values()
selected_theme = 'SystemDefault'
ml_text = 'The quick brown fox jumped over the lazy dog.'

def loop():
    global selected_theme, ml_text
    main_layout = [[sg.Text('PySimpleGUI Theme Sampler', font=('Helvetica', 14))],
                   [sg.Button('Random Button'), sg.Combo(themes, key='theme_cbo', size=(35,10), default_value=selected_theme, enable_events=True)],
                   [sg.Multiline(ml_text, size=(40,10), key='ml_text', font=('Helvetica', 12))]]
    main = sg.Window('Theme Sampler', main_layout, finalize=True)
    event, values = main.read()
    if event not in (None, 'Exit'):
        selected_theme = values['theme_cbo']
        ml_text = values['ml_text']
        sg.change_look_and_feel(selected_theme)
        main.close()
        return event
    else:
        return None

while True:
    event = loop()  
    if event is None:
        break
    else:
        continue