import PySimpleGUI as sg 
import shelve

app = shelve.open('settings')
app['filename'] = None
app['theme'] = 'Black'
app['themes'] = sg.list_of_look_and_feel_values()
app['info'] = ''
app['body'] = ''
app['font'] = ('Consolas', 12)
app['tabsize'] = 4
app.close()