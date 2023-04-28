import PySimpleGUI as sg
sg.theme('DarkAmber')

layout = [
    [sg.Text('Quantas pastas você deseja monitorar?',
             font='Lucida', justification='left'), sg.Text(' '*20)],
    [sg.Combo(['1', '2', '3'], key='button', pad=((10, 0), 0))]
]

layout2 = [
    [sg.Text('Quantas pastas você deseja monitorar?',
             font='Lucida', justification='left'), sg.Text(' '*20)],
    [sg.Combo(['1', '2', '3'], key='button', pad=((10, 0), 0))]
]

teste = [[sg.Column(layout, key='teste')], [sg.Column(layout2, key='teste2')]]

window = sg.Window('Teste', teste, size=(400, 400))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
