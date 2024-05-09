ezalpy
======

.. image:: https://img.shields.io/pypi/v/ezalpy.svg
    :target: https://pypi.org/project/ezalpy/
    :alt: PyPI Version

.. image:: https://img.shields.io/github/stars/DevMasterLinux/al.py.svg
    :target: https://github.com/DevMasterLinux/al.py
    :alt: GitHub Stars

.. image:: https://img.shields.io/github/v/release/DevMasterLinux/al.py.svg
    :target: https://github.com/DevMasterLinux/al.py/releases
    :alt: GitHub Release

Install
-------

Via pip (Stable)

.. code-block:: bash

    python3 -m pip install --upgrade pip
    pip install al

Via Self Build (Stable, Beta)

.. code-block:: bash

    git clone https://github.com/DevMasterLinux/al.py
    cd al.py
    pip install .

Via Release: Download the `latest release here <https://github.com/DevMasterLinux/al.py/releases>`__
Copy the URL and Run

.. code-block:: bash

    pip install <url>

Or 

.. code-block:: bash
    
    mkdir tmp
    cd tmp
    wget <url>
    cd ..
    pip install tmp/*

The release includes a .so file, use this as a module if you wish for fast import.

How to use (System)
--------------------

Import the System Class, Create a Connection

.. code-block:: python

    import platform
    from al import System
    system = System(platform.system())
    
Now Use the Connection

Run Commands

.. code-block:: python

    system.run(command)

Make a Directory

.. code-block:: python

    system.mkdir(path)

For more, use an IDE.

How to use (Manipulate)
--------------------------

Import the Manipulate Class

.. code-block:: python

    import platform
    from al import Manipulate
    m = Manipulate(platform.system())

Print a Message at X, Y

.. code-block:: python

    m.print(x, y, text)
