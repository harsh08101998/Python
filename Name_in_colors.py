import sys
from termcolor import colored, cprint
text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
print(text)


text2 = colored("\033[1;32m This text is Bright Green ", attrs=['reverse', 'blink'],"\U0001f600")
print(text2)