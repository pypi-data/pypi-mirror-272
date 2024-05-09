# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('../src'))

import redmost

# -- Project information -----------------------------------------------------

project = 'redmost'
copyright = "2022-2024, Maurizio D'Addona <mauritiusdadd@gmail.com>"
author = "Maurizio D'Addona"

# The full version, including alpha/beta/rc tags
release = redmost.__version__

github_url = "https://github.com/mauritiusdadd/redmost"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
]

issuetracker = 'github'
issuetracker_project = 'mauritiusdadd/redmost'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

numfig = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    os.path.join('css', 'custom.css'),
]

html_logo = os.path.join('pics', 'redmost.svg')
html_theme_options = {
    'logo_only': True,
    'display_version': True
}

html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "mauritiusdadd", # Username
    "github_repo": "redmost", # Repo name
    "github_version": "main", # Version
    "conf_py_path": "/docs/", # Path in the checkout to the docs root
}

# EPUB options
epub_show_urls = 'footnote'
