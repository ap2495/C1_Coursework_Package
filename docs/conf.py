# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sphinx_rtd_theme
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Dual Autodifferentiaton Package'
copyright = '2024, Alexandr Prucha'
author = 'Alexandr Prucha'
release = '0.1.dev0+d20241205'
autoclass_content = 'both'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.mathjax',
              'nbsphinx',
              'sphinx.ext.autosummary',
              'sphinx.ext.intersphinx',
              'sphinx.ext.viewcode',
              'sphinxcontrib.spelling']

mathjax3_config = {
    'tex2jax': {
        'inlineMath': [['$', '$'], ['\\(', '\\)']],
        'displayMath': [['$$', '$$'], ['\\[', '\\]']]
    }
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'dual_autodiff/version.py', '**/version.py']
autodoc_mock_imports = ['dual_autodiff.version']

# Spelling settings
spelling_lang = 'en_US'  # Language for spell-checking (e.g., 'en_GB' for British English)
spelling_word_list_filename = 'spelling_wordlist.txt'  # Custom word list

autosummary_generate = True
add_module_names = False  # Remove module paths like dual_autodiff.dual
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'special-members': '__add__,__sub__,__mul__,__pow__',
    'show-inheritance': True
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
