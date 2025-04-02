# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import asyncio
import os

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

NOTEBOOKS_DIR = os.path.join(os.path.dirname(__file__), "..", "pyturbo", "notebooks")


def list_notebooks(directory):
    """List all notebooks in a directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".ipynb")]


list_nb = list_notebooks(NOTEBOOKS_DIR)


@pytest.fixture(scope="session")
def execute_preprocessor():
    """Return a preprocessor that executes notebooks."""
    return ExecutePreprocessor(timeout=600)


@pytest.mark.parametrize("notebook_path", list_nb)
def test_notebook_execution(execute_preprocessor, notebook_path):
    """Test that a notebook can be executed without error."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    try:
        execute_preprocessor.preprocess(
            notebook, {"metadata": {"path": os.path.dirname(notebook_path)}}
        )
    except Exception as e:
        pytest.fail(f"Notebook execution failed for {notebook_path}: {e}")
