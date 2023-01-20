# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os, sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../ModelLibrary'))
sys.path.insert(0, os.path.abspath('../ImageAnalyser'))

autodoc_mock_imports = ['kivy', 'tensorflow', 'keras', 'audio_metadata', 'threading', 'pandas', 'xlrd', 'pcc']

project = 'Moody'
copyright = '2023, conyeda lorenaromerom02 Anthony5432 david-fm'
author = 'conyeda lorenaromerom02 Anthony5432 david-fm'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '__pycache__']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
