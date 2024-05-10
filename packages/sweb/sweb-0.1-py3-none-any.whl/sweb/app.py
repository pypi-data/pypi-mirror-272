# File: generator.py

import json
import os
import shutil
from template_processor import TemplateProcessor
from style_processor import StyleProcessor
from asset_manager import AssetManager
from data_loader import DataLoader

class SiteGenerator:
  """Generates a static website by processing templates, styles, and assets."""

  def __init__(self, data_dir, template_dir, output_dir, assets_src, assets_dst, styles_src, styles_dst):
    self.data_dir = data_dir
    self.template_dir = template_dir
    self.output_dir = output_dir
    self.assets_src = assets_src
    self.assets_dst = assets_dst
    self.styles_src = styles_src
    self.styles_dst = styles_dst

  def setup_directory(self):
    """Clears the output directory and creates a new one."""
    if os.path.exists(self.output_dir):
      shutil.rmtree(self.output_dir)
    os.makedirs(self.output_dir)

  def generate_site(self):
    """Generates the static site by processing templates, styles, and assets."""
    self.setup_directory()

    data_loader = DataLoader(self.data_dir)
    data = data_loader.load()

    template_processor = TemplateProcessor(self.template_dir, self.output_dir, data)
    style_processor = StyleProcessor(self.styles_src, self.styles_dst)
    asset_manager = AssetManager(self.assets_src, self.assets_dst)

    template_processor.process_templates()
    style_processor.process_styles()
    asset_manager.copy_assets()

if __name__ == "__main__":
  generator = SiteGenerator(
    data_dir='app/data',
    template_dir='app/templates',
    output_dir='dist',
    assets_src='app/assets',
    assets_dst='dist/assets',
    styles_src='app/styles',
    styles_dst='dist/styles'
  )
  generator.generate_site()
