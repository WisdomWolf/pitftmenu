#!/usr/bin/env python

import sys, pygame, socket
from signal import alarm, signal, SIGALRM, SIGKILL
from pygame.locals import *
import time
import subprocess
import os
import RPi.GPIO
from subprocess import *
from Menu_Button import Menu_Button
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

# wtf
class Color():
    # colors    R    G    B
    white   = (255, 255, 255)
    red     = (255,   0,   0)
    green   = (  0, 255,   0)
    blue    = (  0,   0, 255)
    black   = (  0,   0,   0)
    cyan    = ( 50, 255, 255)
    magenta = (255,   0, 255)
    yellow  = (255, 255,   0)
    orange  = (255, 127,   0)


# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(text, xpo, ypo, height, width, color, action, action_text, args=None):
    b = Menu_Button(text, xpo, ypo, height, width, color, action, action_text, argv=args)
    font=pygame.font.Font(None,30)
    label=font.render(str(text), 1, (color))
    screen.blit(label,(xpo, ypo + Y_PADDING))
    pygame.draw.rect(screen, color, (xpo - b.padding, ypo - b.padding, width, height), Menu_Button.RECT_FRAME_WIDTH)
    print('added {0} button with padding:{1}'.format(text, b.padding))
    button_list.append(b)

# define function for printing text in a specific place with a specific colour
def make_label(text, xpo, ypo, fontsize, color):
    font=pygame.font.Font(None,fontsize)
    label=font.render(str(text), 1, (color))
    screen.blit(label,(xpo,ypo))

# define function that checks for touch location
def on_touch():
    # get the position that was touched
    #  x_min                 x_max   y_min                y_max
    # button 3 event
    for button in button_list:
        if button.matches_touch(pygame.mouse.get_pos()):
            do_run(button)
            break

# Get Your External IP Address
def get_ip():
    ip_msg = "Not connected"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        ip_msg="IP:" + s.getsockname()[0]
    except Exception:
        pass
    return ip_msg

# Restart Raspberry Pi
def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    sys.exit()

# Shutdown Raspberry Pi
def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    sys.exit()

def run_cmd(cmd):
    process = Popen(cmd.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

def do_run(button):
        print(button.action_text)
        screen.fill(Color.black)
        font = pygame.font.Font(None, 48)
        label = font.render(button.action_text, 1, (Color.white))
        screen.blit(label,(10, 110))
        pygame.display.flip()
        pygame.quit()
        button.call_action()

# Set up the base menu you can customize your menu with the colors above

# Set brightness to ~40%
run_cmd("gpio -g mode 18 pwm")
run_cmd("gpio -g pwm 18 400")
print('Set brightness to 400')

#set size of the screen
size = SCREEN_WIDTH, SCREEN_HEIGHT = 320, 240

# Solution from StackOverflow user BBUK
# https://stackoverflow.com/questions/17035699/pygame-requires-keyboard-interrupt-to-init-display
def init_pygame():
    class Alarm(Exception):
        pass
    def alarm_handler(signum, frame):
        raise Alarm
    signal(SIGALRM, alarm_handler)
    alarm(3)
    print('initializing pygame screen')
    try:
        pygame.init()
        DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        alarm(0)
    except Alarm:
        raise KeyboardInterrupt

init_pygame()
print('screen initialized')
screen = pygame.display.get_surface()
print('screen mode set')

# Initialize pygame and hide mouse
pygame.mouse.set_visible(False)
button_list = []
Y_PADDING = 8

print('initialization complete')

# Background Color
screen.fill(Color.black)
print('screen fill completed')

# Outer Border
pygame.draw.rect(screen, Color.blue, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)
pi_hostname = (run_cmd("hostname"))[:-1]
print('outer border and pi_hostname retrieval completed')

# Buttons and labels

# First Row Label
time_rect = pygame.Rect(20, 10, 290, 79)
make_label(pi_hostname + " - " +  get_ip(), 20, SCREEN_HEIGHT - 20, 24, Color.blue)
print('first row label creation completed')

# Third Row buttons 5 and 6
make_button("      Terminal", 15, 105, 50, 145, Color.blue, sys.exit, "Exiting to Terminal")
make_button("  WiFi Setup", 170, 105, 50, 145, Color.blue, os.system, "WiFi Settings. .", "sudo python /home/pi/pifi.py/pifi.py --gui")

# Fourth Row Buttons
make_button("      Reboot", 15, 165, 50, 145, Color.blue, restart, "Rebooting. .")
make_button("   Shutdown", 170, 165, 50, 145, Color.blue, shutdown, "Shutting Down. .")
print('button creation completed')

def refresh_screen():
    
    date_string = time.strftime('%a %b %d, %Y')
    time_string = time.strftime('%I:%M%p')
    
    screen.fill(Color.black, time_rect)
    make_label(date_string, 20, 10, 36, Color.blue)
    make_label(time_string, 20, 25, 100, Color.blue)
    
    

print('beginning primary loop')
#While loop to manage touch screen inputs
while 1:
    try:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
                on_touch()

            #ensure there is always a safe way to end the program if the touch screen fails
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()

        refresh_screen()            
        pygame.display.flip()
    except KeyboardInterrupt:
        print('Ctrl+C received. Exiting')
        sys.exit()
