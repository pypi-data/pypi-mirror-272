# File: data_loader.py

import json
import os

class DataLoader:
  """Loads data from JSON files within a provided directory path."""

  def __init__(self, src):
    self.src = src

  def load(self):
    result = {}
    for root, dirs, files in os.walk(self.src):
      for file in files:
        if file.endswith('.json'):
          path = os.path.join(root, file)
          key_path = os.path.relpath(path, self.src).replace('.json', '').replace(os.sep, '/')
          keys = key_path.split('/')
          self._assign_to_dict(result, keys, path)
    return result

  def _assign_to_dict(self, dictionary, keys, file_path):
    for key in keys[:-1]:
      if key not in dictionary:
        dictionary[key] = {}
      dictionary = dictionary[key]
    with open(file_path, 'r') as file:
      dictionary[keys[-1]] = json.load(file)
