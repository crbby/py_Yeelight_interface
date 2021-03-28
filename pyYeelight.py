from yeelight import discover_bulbs, Bulb
import PySimpleGUI as sg


sg.theme('System default 1')
bulb_list = []
bulb_list_addr = []
currently_selected = ''


def refresh():
    global bulb_list

    bulb_list.clear()

    for bulb in discover_bulbs():
        addr = bulb['ip']
        bulb_list.append(Bulb(addr))
        bulb_list_addr.append(addr)


def control_all(mode):
    global bulb_list

    for bulb in bulb_list:
        if mode == 'on':
            bulb.turn_on()

        if mode == 'off':
            bulb.turn_off()


file_list_column = [
    [
        sg.Button('Refresh', enable_events=True, key='-REF-'),
        sg.Button('All On', enable_events=True, key='-ALL ON-'),
        sg.Button('All Off', enable_events=True, key='-ALL OFF-')
    ],
    [
        sg.Listbox(
            values=bulb_list_addr, enable_events=True, size=(40, 20), key="-BULB LIST-"
        )
    ],
]

image_viewer_column = [
    [sg.Button('On', enable_events=True, key='-SEL ON-')],
    [sg.Button('Off', enable_events=True, key='-SEL OFF-')],
    [sg.Button('Exit', enable_events=True, key='-EXIT-')],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

refresh()
window = sg.Window("pyYeelightControl v0.1", layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break

    elif event == '-BULB LIST-':
        currently_selected = values['-BULB LIST-'][0]
        print(currently_selected)

    elif event == '-REF-':
        print('ref')
        refresh()
        window['-BULB LIST-'].update(bulb_list_addr)

    elif event == '-ALL ON-':
        print('all on')
        control_all('on')

    elif event == '-ALL OFF-':
        print('all off')
        control_all('off')

    elif event == '-SEL ON-':
        print(currently_selected, 'on')
        temp = Bulb(currently_selected)
        temp.turn_on()

    elif event == '-SEL OFF-':
        print(currently_selected, 'off')
        temp = Bulb(currently_selected)
        temp.turn_off()