import os, pathlib
from colorama import init, Fore, Style
from datetime import datetime

class Logger:
  def __init__(self, file, loglevel):
    init()
    self.file = os.path.join(pathlib.Path(__file__).absolute().parent, file)
    self.level = loglevel # 0 - x ; 1 - v ; 2 - vv ; 3- vvv
    
  def log(self, message):
    det = f'[+] {datetime.now()} Message: {message}\n'
    
    if self.level > 2:
      print(det)
      
    with open(self.file, 'a') as f:
      f.write(det)
      
  def warn(self, message):
    det = f'[!] {datetime.now()} Warning: {message}\n'
    
    if self.level > 1:
      print(Fore.YELLOW + det + Style.RESET_ALL)
    
    with open(self.file, 'a') as f:
      f.write(det)
      
  def error(self, message):
    det = f'[×] {datetime.now()} Error: {message}\n'
    
    if self.level > 0:
      print(Fore.RED + det + Style.RESET_ALL)
    
    with open(self.file, 'a') as f:
      f.write(det)