import os
import json
import pathlib

class Singleton(type):
  _instances = {}

  def __call__(self, *args, **kwargs):
    if self not in self._instances:
      instance = super().__call__(*args, **kwargs)
      self._instances[self] = instance

    return self._instances[self]

class Dialogs(metaclass=Singleton):
  def __init__(self, file="dialogue.json"):
    self.file = os.path.join(pathlib.Path(__file__).absolute().parent, "../"+file)
    
    if pathlib.Path(self.file).is_file():
      with open(self.file, "r", encoding="utf-8") as f:
        self.data = json.load(f)

    else:
      raise FileNotFoundError(f"file {file} not found")
  
  def msg(self, key):
    return self.data["commands"][key] or ""
  
  def hlp(self, key):
    return self.data["prompts"][key] or ""
  
  def err(self, key):
    return self.data["errors"][key] or ""