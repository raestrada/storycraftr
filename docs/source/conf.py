# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "StoryCraftr"
copyright = "2024, Rodrigo Estrada"
author = "Rodrigo Estrada"
release = "MIT"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []

language = "Python"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

# Añadir estas líneas al final de conf.py
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_click.ext",
]

# Opcionalmente, si quieres usar un tema como 'alabaster' o 'readthedocs'
html_theme = "alabaster"
