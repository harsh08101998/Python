import pyautogui
import time
time.sleep(4)
count=0
while count<=200:
    pyautogui.typewrite("Ha Dost")
    pyautogui.press("enter")
    count=count+1