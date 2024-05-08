======================================
 `xotless.types`:mod: -- Shared types
======================================

.. module:: xotless.types

.. testsetup::

   from xotless.types import *


.. autoclass:: EqTypeClass

.. autoclass:: OrdTypeClass


.. autoclass:: Domain
   :members: sample, union, __contains__, __sub__, __or__, __and__,
             __le__, __lt__, __ge__, __gt__, __bool__
