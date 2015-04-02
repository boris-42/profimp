===============================
Profimp - python imports tracer
===============================


Profimp allows you to trace imports of your code.

This lib should be used to simplify optimization of imports in your code.
At least you will find what consumes the most part of time and do the
right decisions.

Syntax:

.. code-block::

    profimp [import_module_line]

Samples:

.. code-block::

    profimp "import re"

    or

    profimp "from somemoudle import something"
