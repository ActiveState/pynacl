Installation
============

Binary wheel install
--------------------

PyNaCl ships as a binary wheel on macOS, Windows and Linux ``manylinux1`` [#many]_ ,
so all dependencies are included. Make sure you have an up-to-date pip
and run:

.. code-block:: console

    $ pip install pynacl

Linux source build
------------------

PyNaCl relies on `libsodium`_, a portable C library. This ActiveState
build no longer bundles a copy; it always links against an externally built
``libsodium`` (1.0.20 or later). By default the compiler and linker search
paths are used:

.. code-block:: console

    $ pip install pynacl

To build against a ``libsodium`` installed under a specific prefix, point
``SODIUM_HOME`` at it (its ``include`` and ``lib``/``lib64`` directories are
added to the search paths):

.. code-block:: console

    $ SODIUM_HOME=/opt/libsodium pip install pynacl

.. warning:: Usage of the legacy ``easy_install`` command provided by setuptools
   is generally discouraged, and is completely unsupported in PyNaCl's case.

.. _libsodium: https://github.com/jedisct1/libsodium

.. [#many] `manylinux1 wheels <https://www.python.org/dev/peps/pep-0513/>`_
    are built on a baseline linux environment based on Centos 5.11
    and should work on most x86 and x86_64 glibc based linux environments.
