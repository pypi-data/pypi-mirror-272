# File: style_processor.py

import os
import shutil
import sass

class StyleProcessor:
  """Processes styles by compiling Sass files and copying CSS files."""

  def __init__(self, styles_dir, output_dir):
    self.styles_dir = styles_dir
    self.output_dir = output_dir

  def process_styles(self):
    """Processes all style files in the styles directory."""
    for root, dirs, files in os.walk(self.styles_dir):
      for file in files:
        if file.endswith(('.sass', '.scss')):
          self._compile_sass(root, file)
        elif file.endswith('.css'):
          self._copy_css(root, file)

  def _compile_sass(self, root, file):
    """Compiles a Sass file to CSS and saves it in the output directory."""
    file_path = os.path.join(root, file)
    output_path = os.path.join(self.output_dir, os.path.relpath(root, self.styles_dir))
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    css_content = sass.compile(filename=file_path)
    css_file_path = os.path.join(output_path, file.rsplit('.', 1)[0] + '.css')
    with open(css_file_path, 'w') as css_file:
      css_file.write(css_content)

  def _copy_css(self, root, file):
    """Copies a CSS file to the output directory."""
    src_file_path = os.path.join(root, file)
    output_path = os.path.join(self.output_dir, os.path.relpath(root, self.styles_dir))
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    shutil.copy(src_file_path, output_path)
