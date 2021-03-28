from yeelight import discover_bulbs, Bulb
import PySimpleGUI as sg

sg.theme('system default for real')

bulb_list = []
bulb_list_addr = []
currently_selected = ''

value_r = '1'
value_g = '1'
value_b = '1'


# clear and refresh (list)bulb_list
def refresh():
    global bulb_list, bulb_list_addr

    bulb_list.clear()
    bulb_list_addr.clear()

    for bulb in discover_bulbs():
        addr = bulb['ip']
        bulb_list.append(Bulb(addr))
        bulb_list_addr.append(addr)


# control all devices
def control_all(mode):
    global bulb_list

    for bulb in bulb_list:
        if mode == 'on':
            bulb.turn_on()

        if mode == 'off':
            bulb.turn_off()


# left column layout
bulb_list_column = [
    [
        sg.Button('All On', enable_events=True, key='-ALL ON-'),
        sg.Button('All Off', enable_events=True, key='-ALL OFF-')
    ],
    [
        sg.Listbox(values=bulb_list_addr, enable_events=True, size=(20, 15), key="-BULB LIST-")
    ],
    [
        sg.Button('Refresh', enable_events=True, key='-REF-'),
        sg.Button('Exit', enable_events=True, key='-EXIT-')
    ]
]

# right column layout
bulb_control_column = \
    [
        [sg.Button('On', enable_events=True, key='-SEL ON-'), sg.Button('Off', enable_events=True, key='-SEL OFF-')],

        [sg.HSeparator()],

        [sg.Text('RGB:')],
        [
            sg.Input(size=(5, 15), enable_events=True, key='-SLIDER R-'),
            sg.Input(size=(5, 15), enable_events=True, key='-SLIDER G-'),
            sg.Input(size=(5, 15), enable_events=True, key='-SLIDER B-')
        ],

        [
            sg.Button('Send RGB', enable_events=True, key='-SEND RGB-')
        ],

        [sg.HSeparator()],

        [sg.Text('Brightness:')],
        [
            sg.Slider(range=(1, 100), orientation='h', disable_number_display=True, size=(15, 20), default_value=1,
                      enable_events=True, key='-BRIGHT-')
        ],

        [
            sg.Button('Send Brightness', enable_events=True, key='-SEND BRIGHT-')
        ],

        [sg.HSeparator()],

        [sg.Text('White temperature:')],
        [
            sg.Slider(range=(2700, 4700), orientation='h', disable_number_display=True, size=(15, 20),
                      default_value=2700,
                      enable_events=True, key='-TEMP-')
        ],

        [
            sg.Button('Send Temp', enable_events=True, key='-SEND TEMP-')
        ]
    ]

# combined
layout = \
    [
        [
            sg.Column(bulb_list_column),
            sg.VSeperator(),
            sg.Column(bulb_control_column)
        ]
    ]

# update (list)bulb_list and create window instance
refresh()
window = sg.Window("py_Yeelight_interface v0.2", layout, margins=(10, 10))

# main loop
while True:
    event, values = window.read()

    # closing window
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break

    # non device specific event handling
    elif event == '-BULB LIST-':
        currently_selected = values['-BULB LIST-'][0]

    elif event == '-REF-':
        refresh()
        window['-BULB LIST-'].update(bulb_list_addr)

    elif event == '-ALL ON-':
        control_all('on')

    elif event == '-ALL OFF-':
        control_all('off')

    # device specific events
    if currently_selected != '':

        temp_bulb_obj = Bulb(currently_selected)

        if event == '-SEL ON-':
            temp_bulb_obj.turn_on()

        elif event == '-SEL OFF-':
            temp_bulb_obj.turn_off()

        elif event == '-SLIDER R-':
            value_r = values['-SLIDER R-']

        elif event == '-SLIDER G-':
            value_g = values['-SLIDER G-']

        elif event == '-SLIDER B-':
            value_b = values['-SLIDER B-']

        elif event == '-SEND RGB-' and value_r.isnumeric() and value_g.isnumeric() and value_b.isnumeric():

            value_r_i = int(value_r)
            value_g_i = int(value_g)
            value_b_i = int(value_b)

            zero_list = [0, 0, 0]
            value_rgb_list = [value_r_i, value_g_i, value_b_i]

            if value_rgb_list != zero_list:
                temp_bulb_obj.set_rgb(value_r_i, value_g_i, value_b_i)

        elif event == '-SEND BRIGHT-':
            slider = window[event]
            slider_brightness = int(values['-BRIGHT-'])

            temp_bulb_obj.set_brightness(slider_brightness)

        elif event == '-SEND TEMP-':
            slider = window[event]
            slider_temp = int(values['-TEMP-'])

            temp_bulb_obj.set_color_temp(slider_temp)

    temp_bulb_obj = None
