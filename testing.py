import win32gui
import win32ui
import win32con
import win32api as winapi
from time import time
from PIL import ImageEnhance as IE 
from PIL import Image
import pyautogui
import re
import keyboard


ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."] #Set Characters For Grayscale
hwnd = win32gui.FindWindow(None, 'Genshin Impact')


def pixel_to_ascii(image):  
    pixels = image.getdata()  #Convert RGB To Int
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 25]
    return ascii_str


"""def sendInput():
    while True:
        event = keyboard.read_event('a')
        if event.event_type == keyboard.KEY_DOWN:
            winapi.PostMessage(hwnd, win32con.WM_CHAR, 'a', 0);"""


def to_gray(image):
    return image.convert("L") # Grayscale


#TODO multiprocessing window_capture + getwindowtitle


def window_capture():  #Capture specific Window Function
    #WindowTitle = getWindowTitle()
    w = 660
    h = 528 

    wDC = win32gui.GetWindowDC(hwnd) 
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    bmpinfo = dataBitMap.GetInfo()              
    bmpstr = dataBitMap.GetBitmapBits(True)
    img = Image.frombuffer(                     #Transfer to PIL insd buffer
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    return img


def getWindowTitle(): #Get Title
    windows = pyautogui.getAllWindows()
    for window in windows:
        #if re.search('DOOM Shareware', window.title):
            return window.title
    return None
        

while(True):
    #executing = True #checking fps
    #start = time()
    screenshot = window_capture()
    screenshot = screenshot.resize((500, 400))          #Resize Output
    screenshot = IE.Contrast(screenshot).enhance(15)    # Better quality output
    screenshot = to_gray(screenshot)
    ascii_str = pixel_to_ascii(screenshot)

    ascii_img = ""      #init String to file

    for i in range(0, len(ascii_str), 500):
        ascii_img += ascii_str[i:i + 500] + "\n"
    with open("output.txt", "w") as f:
        f.write(ascii_img)
    #end = time()
    #duration = end - start
    #print(duration)     
    #while(executing == True):
    #    if duration < 0.08:
    #        end = time()
    #        duration = end - start
    #    else:
    #        executing = False         #Cap fr fr fr
        
#A Stupid code made by xt69 or smthg idk f my life
