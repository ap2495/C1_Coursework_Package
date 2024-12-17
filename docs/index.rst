.. DualAutodifferentiation Package documentation master file, created by 
   sphinx-quickstart on Thu Dec  5 15:28:19 2024.

Dual Class Documentation
==============================================

- **Author**: Alexandr Prucha 
- **Project**: Autodifferentiation with Dual Numbers  
- **Version**: 0.1  
- **Python Version**: 3.12.3
- **License**: MIT 

Welcome to the documentation for the Dual Autodifferentiation Package! This package provides utilities for automatic differentiation.

Installation
------------

To install the package, use the following command:

.. code-block:: bash

   pip install dual_autodiff

In this section we provide detailed documentation for the modules and classes in the `dual_autodiff` package.


Dual Class Overview
===================

The `Dual` generates Dual numbers from pairs of inputs. It also provides methods for performing basic calculations, and evaluating elementary functions:

.. automodule:: dual_autodiff.dual
   :members:
   :special-members: __add__, __sub__, __mul__, __pow__
   :undoc-members:
   :show-inheritance:
   :no-index:


.. toctree::
   :maxdepth: 2
   :caption: Class Documentation
   :hidden:

   self





Jupyter Notebook Example
========================

Below is an example of a Jupyter notebook demonstrating the package's usage:

.. toctree::
   :maxdepth: 1
   :caption: Tutorial

   dual_autodiff

.. toctree::
   :maxdepth: 1
   :caption: Indices

   Index <genindex>
   Module Index <modindex>


Module Reference
----------------
.. toctree::
   :maxdepth: 1
   :caption: Summary

   Dual Autodiff Module <source/modules>
