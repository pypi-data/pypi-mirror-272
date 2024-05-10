# File: generator.py

import json
import os
import shutil
import sys
from .template_processor import TemplateProcessor
from .style_processor import StyleProcessor
from .asset_manager import AssetManager
from .data_loader import DataLoader

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

def generate_site():
  """Generates the static site by processing templates, styles, and assets."""
  if not os.path.exists('.sweb'):
    print('Not a sweb project.')
    return
  else:
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

def create_project(project_name):
  """Creates a new project with the necessary directories and files."""
  project_dir = os.path.join(os.getcwd(), project_name)
  if os.path.exists(project_dir):
    print('Project already exists.')
    return
  os.makedirs(project_dir)
  os.makedirs(os.path.join(project_dir, 'app'))
  os.makedirs(os.path.join(project_dir, 'app', 'data'))
  # create a default data.json
  with open(os.path.join(project_dir, 'app', 'data', 'index.json'), 'w') as f:
    f.write(f"{{\n  \"title\": \"{project_name}\",\n  \"description\": \"A sweb project.\"\n}}")
  os.makedirs(os.path.join(project_dir, 'app', 'templates'))
  # create a default index.hbs
  with open(os.path.join(project_dir, 'app', 'templates', 'index.hbs'), 'w') as f:
    f.write("<!DOCTYPE html>\n<html>\n  <head>\n    <title>{{index.title}}</title>\n    <link rel='stylesheet' href='styles/style.css'>\n  </head>\n  <body>\n    <h1>Hello, world to {{index.description}}!</h1>\n  </body>\n</html>")
  os.makedirs(os.path.join(project_dir, 'app', 'styles'))
  # create a default style.scss
  with open(os.path.join(project_dir, 'app', 'styles', 'style.scss'), 'w') as f:
    f.write('body { h1 { color: red; } }')
  os.makedirs(os.path.join(project_dir, 'app', 'assets'))

  os.makedirs(os.path.join(project_dir, 'dist'))
  # create a empty .sweb file to identify the folder as a sweb project
  open(os.path.join(project_dir, '.sweb'), 'w').close()
  # create a .gitignore to ignore dist folder
  with open(os.path.join(project_dir, '.gitignore'), 'w') as f:
    f.write('dist')

def main():
  args = sys.argv[1:]  # Skip the script name itself
  if len(args) == 0 or (len(args) == 1 and args[0] in ['g', 'generate']):
    generate_site()
  elif len(args) == 2 and args[0] == 'new':
    create_project(args[1])
  else:
    print('Invalid parameters.')

if __name__ == "__main__":
  main()