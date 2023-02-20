import os
import shutil
from pathlib import Path

CWD = Path.cwd()
SOURCEDIR = "source"
BUILDDIR = "_build"
NOTEBOOK_FOLDER = "user_guide/notebooks"

RESOURCES = ("tf.html", "textures/twiinIT_logo.png", "textures/twiinIT.png")


def main():
    """Build documentation."""
    build_documentation()
    copy_notebook_resources()


def build_documentation():
    """Build documentation using Sphinx."""
    return os.system("sphinx-build -b html -d _build/doctrees ./source _build")


def copy_notebook_resources():
    """Copy notebook from package to the documentation folders."""
    for resource in RESOURCES:
        source_path = CWD / SOURCEDIR / NOTEBOOK_FOLDER / resource
        target_path = CWD / BUILDDIR / NOTEBOOK_FOLDER / resource

        if not os.path.exists(target_path.parents[0]):
            os.mkdir(target_path.parents[0])

        shutil.copyfile(source_path, target_path)


if __name__ == "__main__":
    main()
