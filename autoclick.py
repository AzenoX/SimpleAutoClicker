import pyautogui
import time
import PySimpleGUI as sg
import threading

from pyautogui import KEYBOARD_KEYS
from pynput import keyboard

keyDict = {
    "Left Mouse": "left",
    "Right Mouse": "right",
}

def is_number(s):
    try:
        float(s)  # Try to convert the string to a float
        return True
    except ValueError:
        return False

def auto_click(key, duration, interval, local_delay):
    """
    Clicks the left mouse button at specified intervals for a certain duration.

    :param key: Desired key to hold.
    :param interval: Time interval between clicks in seconds.
    :param duration: Total duration for which the script will run in seconds.
    :param local_delay: Add an initial delay.
    """

    if local_delay == '':
        local_delay = '0'
    time.sleep(int(local_delay))

    if duration == 'Infinity':
        globals()['hold'] = True
        globals()['holdKey'] = None

        globals()['keyboardThread'] = threading.Thread(target=create_keyboard_listener)
        globals()['keyboardThread'].start()

        while globals()['hold']:
            pyautogui.click(button=keyDict[key])
            time.sleep(interval)
    else:
        end_time = time.time() + duration
        while time.time() < end_time:
            pyautogui.click(button=keyDict[key])
            time.sleep(interval)

def hold_click(key, duration, local_delay):
    """
    Clicks and holds the left mouse button at specified intervals for a certain duration.

    :param key: Desired key to hold.
    :param duration: Total duration for which the script will run in seconds.
    :param local_delay: Add an initial delay.
    """
    # Apply delay
    globals()['hold'] = True

    if local_delay == '':
        local_delay = '0'
    time.sleep(int(local_delay))

    if duration == 'Infinity':
        globals()['holdKey'] = key

        # Start keyboard listener
        globals()['keyboardThread'] = threading.Thread(target=create_keyboard_listener)
        globals()['keyboardThread'].start()

        i = 0
        while globals()['hold']:
            pyautogui.mouseDown(button=keyDict[key])
            # TODO: Add a variable to manage this behavior (sometimes unhold and rehold the button)
            if i >= 60:
                pyautogui.mouseUp(button=keyDict[key])
                time.sleep(0.1)
                pyautogui.mouseDown(button=keyDict[key])
                time.sleep(1)
                i = 0
            i = i + 1
    else:
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            pyautogui.mouseDown(button=keyDict[key])
            if i >= 60:
                pyautogui.mouseUp(button=keyDict[key])
                time.sleep(0.1)
                pyautogui.mouseDown(button=keyDict[key])
                time.sleep(1)
                i = 0
            i = i + 1

def create_keyboard_listener():
    """
    Create a simple listener on the keyboard

    :return:
    """
    keyboard_listener = keyboard.Listener(on_press=handle_keyboard_inputs)
    keyboard_listener.start()

def handle_keyboard_inputs(key):
    """
    This method is used to stop infinite loops (hold click or auto click). And then, stop the keyboard listener.

    :param key: The pressed key.
    :return:
    """
    stop_key = globals().get('stop_key', 'f6').lower()

    try:
        # Check if the pressed key matches the selected stop key
        if key.char == stop_key:
            globals()['hold'] = False
            if globals()['holdKey'] is not None:
                pyautogui.mouseUp(button=keyDict[globals()['holdKey']])
            globals()['keyboardThread'].join()
    except AttributeError:
        if key == keyboard.Key[stop_key]:
            globals()['hold'] = False
            if globals()['holdKey'] is not None:
                pyautogui.mouseUp(button=keyDict[globals()['holdKey']])
            globals()['keyboardThread'].join()


layout = [
    [
        sg.Text('Key:'),
        sg.OptionMenu(['Left Mouse', 'Right Mouse'], default_value='Left Mouse', key='-KEY-')
    ],
    [
        sg.Text('Delay before running:', key="delay_title", visible=True),
        sg.Input(enable_events=True, key="-DELAY-", visible=True)
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Text('Type of Click:'),
        sg.Radio('Single', group_id=1, default=True, enable_events=True, key='-TYPE-'),
        sg.Radio('Hold', group_id=1, enable_events=True, key='-TYPE-'),
    ],
    [
        sg.Text('Clicks Interval:', key="interval_title", visible=True),
        sg.Input(enable_events=True, key="interval_input", visible=True)
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Text('Duration:'),
        sg.Radio('Limited Time', group_id=2, default=True, enable_events=True, key='duration_radio'),
        sg.Radio('Unlimited', group_id=2, enable_events=True, key='duration_radio'),
    ],
    [
        sg.Text('Duration Time:', key='duration_title', visible=True),
        sg.Input(enable_events=True, key='duration_input', visible=True)
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Text('Stop Key (Used when duration is unlimited):'),
        sg.Input(default_text='F6', key='-STOP_KEY-')
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Button('Run'),
        sg.Button('Cancel')
    ]
]

keyboardThread = None
hold = False
holdKey = None
stop_key = 'f6'

window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == 'Run':
        key = values['-KEY-']
        duration = 'Infinity' if values['duration_radio1'] else values['duration_input']
        stop_key = values['-STOP_KEY-'].lower()  # Get the stop key and store it globally
        
        if values['-TYPE-'] == 'Single':
            interval = values['interval_input']
            auto_click(key, duration, interval)
        else:
            delay = values['-DELAY-']
            thread = threading.Thread(target=hold_click, args=(key, duration, delay))
            thread.start()
            thread.join()

    if event == '-DELAY-':
        if not is_number(values['-DELAY-']):
            window['-DELAY-'].update('')

    if event.startswith('-TYPE-'):
        if values['-TYPE-0']: # Hold
            window['interval_title'].update(visible=False)
            window['interval_input'].update(visible=False)
        else:
            window['interval_title'].update(visible=True)
            window['interval_input'].update(visible=True)

    if event == 'interval_input':
        if not is_number(values['interval_input']):
            window['interval_input'].update('')

    if event == 'duration_input':
        if not is_number(values['duration_input']):
            window['duration_input'].update('')

    if event.startswith('duration_radio'):
        if values['duration_radio1']: # Unlimited
            window['duration_title'].update(visible=False)
            window['duration_input'].update(visible=False)
        else:
            window['duration_title'].update(visible=True)
            window['duration_input'].update(visible=True)

window.close()