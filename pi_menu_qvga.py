#!/usr/bin/env python

import sys, pygame, socket
from pygame.locals import *
import time
import subprocess
import os
import RPi.GPIO
from subprocess import *
from enum import Enum
from Menu_Button import Menu_Button
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

#
class Color(Enum):
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

# Initialize pygame and hide mouse
pygame.init()
pygame.mouse.set_visible(0)
button_list = []

# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(text, xpo, ypo, height, width, color, action, action_text, args=None):
    b = Menu_Button(text, xpo, ypo, height, width, color, action, action_text, argv=args)
    font=pygame.font.Font(None,30)
    label=font.render(str(text), 1, (color))
    screen.blit(label,(xpo, ypo))
    pygame.draw.rect(screen, color, (xpo - b.padding, ypo - b.padding, width, height), Menu_Button.RECT_FRAME_WIDTH)
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
        if button.matches(pygame.mouse.get_pos()):
            button.action(*button.args)
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

def call_action(button):
        screen.fill(Color.black)
        font = pygame.font.Font(None, 48)
        label = font.render(button.action_text, 1, (Color.white))
        screen.blit(label,(10, 110))
        pygame.display.flip()
        pygame.quit()
        button.call_action()
        
# Define each button press action
def button(number):
    print "You pressed button ",number

    if number == 3:
        # exit
        screen.fill(Color.black)
        font=pygame.font.Font(None,48)
        label=font.render("Exiting to Terminal", 1, (Color.white))
        screen.blit(label,(10,110))
        pygame.display.flip()
        pygame.quit()
        sys.exit()

    if number == 4:
        # Wifi Settings
        screen.fill(black)
        font=pygame.font.Font(None,48)
        label=font.render("WiFi Settings. .", 1, (white))
        screen.blit(label,(20,120))
        pygame.display.flip()
        pygame.quit()
        os.system("sudo python /home/pi/pifi.py/pifi.py --gui")
        sys.exit()

    if number == 5:
        # reboot
        screen.fill(black)
        font=pygame.font.Font(None,48)
        label=font.render("Rebooting. .", 1, (white))
        screen.blit(label,(40,110))
        pygame.display.flip()
        pygame.quit()
        restart()
        sys.exit()

    if number == 6:
        # shutdown
        screen.fill(black)
        font=pygame.font.Font(None,48)
        label=font.render("Shutting Down. .", 1, (white))
        screen.blit(label,(20,110))
        pygame.display.flip()
        pygame.quit()
        shutdown()
        sys.exit()

# Set up the base menu you can customize your menu with the colors above

#set size of the screen
size = width, height = 320, 240
screen = pygame.display.set_mode(size)

def build_screen():
    # Background Color
    screen.fill(Color.black)
    
    # Outer Border
    pygame.draw.rect(screen, Color.blue, (0,0,320,240),5)
    pi_hostname = run_cmd("hostname")
    pi_hostname = pi_hostname[:-1]
    time_string = time.strftime('%H:%M:%S')
    date_string = time.strftime('%b %d %y')
    # Buttons and labels
    # First Row Label
    make_label(pi_hostname + " - " +  get_ip(), 20, 20, 24, Color.blue)
    make_label(date_string, 20, 40, 36, Color.blue)
    make_label(time_string, 30, 50, 100, Color.blue)
    # Third Row buttons 5 and 6
    make_button("      Terminal", 15, 125, 50, 145, Color.blue, sys.exit, "Exiting to Terminal")
    make_button("  WiFi Setup", 170, 125, 50, 145, Color.blue, os.system, "WiFi Settings. .", "sudo python /home/pi/pifi.py/pifi.py --gui")
    # Fourth Row Buttons
    make_button("      Reboot", 15, 165, 50, 145, Color.blue, restart, "Rebooting. .")
    make_button("   Shutdown", 170, 165, 50, 145, Color.blue, shutdown, "Shutting Down. .")
    

#While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            on_touch()

        #ensure there is always a safe way to end the program if the touch screen fails
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

    build_screen()            
    pygame.display.flip()