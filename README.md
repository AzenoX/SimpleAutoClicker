# Simple AutoClicker

This is a very simple autoclicker which allows you to automatically control your mouse.


## Features

For every action, you can choose the **left** or the **right** click of the mouse. You can repeat a click, or hold a click for a specific time, or for an unlimited time.

## Usage

### Run with Python

First, you need to install all the dependencies:

```
pip install -r requirements.txt
```

Then run the file

```
python autoclick.py
```

### Run with Executable

You can run the dist/autoclick.exe to run the autoclicker.

### How to build

To build the .exe file, simply execute:

```
pyinstaller -F autoclick.py
```

### In Depth

![screenshot](https://i.imgur.com/fCTBnoa.png "Screenshot")

**Key**: Select the mouse key (left or right).

**Delay before running**: This represents the delay (in seconds) between the click on the "Run" button and the moment where is autoclick is starting. 

**Type of Click**: Select if you want the autoclicker to repeat a click or if you want to hold a button.

**Clicks Interval**: In the case you want a click to repeat, this is the interval between clicks.

**Duration**: Select if you want to autoclicker to work during a specific amount of time or if you want to run indefinitely.

**Duration Time**: If you want the autoclicker to run during a specific amount of time, this represents this time (in seconds).

**Stop Key**: If you run the autoclicker indefinitely, this key is used to stop it. <br>
_Refer to: [https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key)_


## License

[LICENSE.md](LICENSE.md)