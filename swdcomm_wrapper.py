#!/usr/bin/python3
# This is a simple wrapper around swd2 with the goal of enabling these
#features.
#
# 1. Sane kill of swd2
# 2. Constant substitution (because they take up needless space on 
#    mecrisp-stellaris
# 3. Possible word name substitution
# 4. File send similar to ctrl+$ function
import subprocess
import threading
from pynput import keyboard
from pynput.keyboard import Key

process = subprocess.Popen(['./swd2'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
last_send = ''
exit_out = 0

# install pynput (sudo apt install python3-pynput)
def on_key_release(key):
    if key == Key.right:
        print("\b\b\b\bRight key clicked")
    elif key == Key.left:
        print("Left key clicked")
    elif key == Key.up:
        print("Up key clicked")
    elif key == Key.down:
        print("Down key clicked")
    elif key == Key.f2:
        exit_out = 1

# Task to read from swd2
def read_swd ():
    global process
    global last_send
    for line in process.stdout:
        line = line.decode()
        #print (line.replace(last_send, ''), end='')
        print (line, end='')

# Task to read lines from terminal and send to swd2
def write_swd():
    global process
    global last_send
    while (True):
        line = input().strip()
        last_send = line
        line = line + "\n"
        line = bytes(line, 'utf-8')
        process.stdin.write(line)
        process.stdin.flush()
        if (exit_out == 1):
            exit()

#process.stdin.write(b'words\n')

t1 = threading.Thread(target=read_swd)
t2 = threading.Thread(target=write_swd)
t1.start()
t2.start()
#with keyboard.Listener(on_release=on_key_release) as listener:
#   listener.join()
listener = keyboard.Listener(on_release=on_key_release) 
listener.start()
