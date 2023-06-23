import time
import usb_hid
import board
import digitalio
import adafruit_ssd1306
import busio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Init Components
display_width = 128
display_high = 64
i2c = busio.I2C(board.GP17, board.GP16)
display = adafruit_ssd1306.SSD1306_I2C(display_width, display_high, i2c)

kbd = Keyboard(usb_hid.devices)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

action_button = digitalio.DigitalInOut(board.GP5)
action_button.switch_to_input(pull=digitalio.Pull.DOWN)
action_button.pull = digitalio.Pull.DOWN

#Define Main Context Global Vars
MENU_SELECT = 1
MENU_SECTIONS = ['Option1','Option2','Option3','Option4']

def DrawBorder():
    display.line(0,63,127,63,1)
    display.line(0,0,127,0,1)
    display.line(0,0,0,63,1)
    display.line(127,0,127,63,1)

def DrawTexBackRect(text,x,y):
    #each caractere uses 6 pixels in screen (font says 5 but for some reason we need do calc using 6)
    #adding 0.26 makes backRect 1 pixel bigger than text
    display.fill_rect(x-1, y-1,len(text)*6.26, 10, 1)
    display.text(text, x, y, 0)

def DrawTextCenterScreen(text,y):
    # center screen - half pixels of each caractere
    x = 64 - len(text)*3
    display.text(text, x, y, 1)

def MenuDraw():
    display.fill(0)
    DrawBorder()
    DrawTextCenterScreen('Menu',3) #header always in y = 3
    for index in range(len(MENU_SECTIONS)):
        text = MENU_SECTIONS[index]
        if index is MENU_SELECT:
            DrawTexBackRect(MENU_SECTIONS[index],6,index*12+15)
        else:
            display.text(MENU_SECTIONS[index], 6, index*12+15, 1)
    display.show()

#Main loop
while True:
    MenuDraw()
    led.value = not led.value
