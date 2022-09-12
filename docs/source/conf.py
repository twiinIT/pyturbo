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

from pyturbo._version import __version__

sys.path.insert(0, os.path.abspath("../.."))
sys.setrecursionlimit(1500)

# -- Project information -----------------------------------------------------

project = "pyturbo"
copyright = "2022, twiinIT"
author = "Adrien DELSALLE"

autosummary_generate = True
autodoc_typehints = "none"

version = str(__version__)
release = version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.viewcode",
    "nbsphinx",
    "autoapi.extension",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "**.ipynb_checkpoints"]

napoleon_include_init_with_doc = True

autodoc_member_order = "bysource"

## Default flags used by autodoc directives
autodoc_default_options = {
    "members": True,
    "member-order": "alphabetical",
    "undoc-members": True,
    "show-inheritance": True,
}

## Generate autodoc stubs with summaries from code
autosummary_generate = True
autoapi_type = "python"
autoapi_dirs = ["../../pyturbo"]
autoapi_root = "api/reference"
autoapi_options = [
    "members",
    "undoc-members",
    "show-module-summary",
    "special-members",
    "imported-members",
    "show-inheritance",
]
autoapi_template_dir = "_templates/autoapi"


def skip_util_classes(app, what, name, obj, skip, options):
    if what == "class":
        skip = False
    else:
        skip = True
    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_util_classes)


# -- Options for HTML output -------------------------------------------------

html_logo = "../assets/twiinIT_grayscale.svg"

html_theme = "pydata_sphinx_theme"

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "tango"

html_theme_options = {
    "github_url": "https://github.com/twiinit/pyturbo",
    "show_prev_next": False,
    "navbar_end": ["search-field.html", "navbar-icon-links.html"],
    "show_toc_level": 1,
}

source_suffix = ".rst"
master_doc = "index"
project = "pyturbo"

copyright = "2022, twiinIT"
author = "twiinIT"

html_context = {
    "display_github": True,
    "github_user": "twiinit",
    "github_repo": "pyturbo",
    "github_version": "master",
    "source_suffix": "",
    "source_url_prefix": "https://gitlab.com/anarcat/foo/blob/HEAD/doc/",
}

napoleon_use_param = True

nbsphinx_execute = "always"
nbsphinx_allow_errors = False


import nbsphinx

napoleon_custom_sections = [
    "variables",
    "inputs",
    "outputs",
    "sub-systems",
    "good practice",
    "design methods",
]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = ["css/default.css"]

import sys

sys.path.insert(0, os.path.abspath(".."))
