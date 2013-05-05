# cuber
arduino/python control of 4x4x4 LED cube

Components:
	- Arduino driver to read LED state from serial stream of bytes.
	- Python code to generate effects and send to Arduino via serial.

## setup
1. Compile and upload `cuber.c` to Arduino. 
1. Install Python
1. Install Python libraries specified in requirements 
     * If you have pip installed, run `pip install -r requirements.txt`.

## usage
1. `python cuber.py` will begin random effect generation
1. Press `Ctrl-C` to be prompted to choose effect.
1. Double-press `Ctrl-C` to exit.