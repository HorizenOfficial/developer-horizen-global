import sys
import os

if 'IS_LOCAL_BUILD' in os.environ:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
else:
  html_theme = 'default'

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx_tabs.tabs',
    'sphinxcontrib.httpdomain',
    'sphinx_rtd_theme'
]

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 4
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Horizen Docs'
copyright = u'© 2021 Zen Blockchain Foundation. All rights reserved.'
version = '1.0.1'
release = '1.0.1'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_logo = 'images/Horizen_UBD_white.svg'
html_favicon = 'images/Horizen_favicon_32x32.png'
html_static_path = ['_static']
html_js_files = ['js/target_blank.js','js/expand_tabs.js']
html_css_files = ['custom.css']
htmlhelp_basename = 'Horizen Docs'
