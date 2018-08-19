import os
from jinja2 import Template

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates',
                             'report.html')


def render(file_path, context):
    with open(TEMPLATE_PATH) as f:
        template = Template(f.read())
    with open(file_path, "w") as f:
        f.write(template.render(context))
