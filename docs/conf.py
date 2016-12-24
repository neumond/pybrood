#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shlex

extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'pybrood'
copyright = '2016, neumond'
author = 'neumond'
version = '1.0'
release = '1.0'
language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False
html_title = 'pybrood'

# -- Options for HTML output ----------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']
htmlhelp_basename = 'pybrooddoc'