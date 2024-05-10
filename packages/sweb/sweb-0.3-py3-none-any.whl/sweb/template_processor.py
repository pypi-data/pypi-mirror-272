# File: template_processor.py

import os
from pybars import Compiler

class TemplateProcessor:
  """Processes Handlebars templates and generates HTML files."""

  def __init__(self, template_dir, output_dir, data):
    self.template_dir = template_dir
    self.output_dir = output_dir
    self.data = data

  def process_templates(self):
    """Processes all templates in the template directory."""
    compiler = Compiler()
    for root, dirs, files in os.walk(self.template_dir):
      for file in files:
        if file.endswith('.hbs'):
          self._compile_template(compiler, root, file)

  def _compile_template(self, compiler, root, file):
    """Compiles a Handlebars template to HTML and saves it in the output directory."""
    template_path = os.path.join(root, file)
    relative_path = os.path.relpath(root, self.template_dir)
    output_path = os.path.join(self.output_dir, relative_path)
    if not os.path.exists(output_path):
      os.makedirs(output_path)

    with open(template_path, 'r') as template_file:
      source = template_file.read()
      template = compiler.compile(source)
      html_content = template(self.data)

    output_file_path = os.path.join(output_path, file.replace('.hbs', '.html'))
    with open(output_file_path, 'w') as html_file:
      html_file.write(html_content)
