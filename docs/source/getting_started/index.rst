.. _getting_started:

Getting started
===============

You should have `mamba <https://github.com/thesnakepit/mamba>`_ or `conda <https://github.com/conda/conda>`_ installed.

Using a Python script
---------------------

Create an environment with the minimal requirements:

.. code-block:: console

    $ micromamba create -n pyturbo -c conda-forge pyturbo
    $ micromamba activate pyturbo

.. code-block:: console

    $ cat pyturbo_example.py
    from pyturbo.systems import Turbofan
     
    tf = Turbofan("tf")
    tf.run_once()

    $ python pyturbo_example.py

.. note::
    This example should work on both Windows and Linux. Remember to run that command in the \
    *pyturbo* activated environment!

Using Jupyter
-------------

If you wish to visualize geometries, also install `jupyterlab`, `pyoccad` and `pythreejs` in your environment:

.. code-block:: console

    $ micromamba activate pyturbo
    $ micrommamba install -c conda-forge "jupyterlab>=3" pyoccad pythreejs
    $ jupyterlab

Now you can use the JupyterLab renderer to display your turbofan geometry in a notebook cell output:

.. code-block:: console

    from pyturbo.systems import Turbofan

    tf = Turbofan("tf")
    tf.run_once()
    tf.jupyter_view()
