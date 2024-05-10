# File: asset_manager.py

import os
import shutil

class AssetManager:
  """Manages the copying of assets from the source directory to the destination directory."""

  def __init__(self, src, dst):
    self.src = src
    self.dst = dst

  def copy_assets(self):
    """Copies all assets from the source directory to the destination directory."""
    if os.path.exists(self.dst):
      shutil.rmtree(self.dst)
    shutil.copytree(self.src, self.dst)
