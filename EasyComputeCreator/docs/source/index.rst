..
  This file is managed by devopsify > update strategy : keep

############
Introduction
############

Welcome to the documentation
----------------------------

To help you navigate the documentation, here is a short overview of how the documentation is
structured. You'll learn about the internal structure of the repository and its main
components and a better understanding on how you can use this project, configure it, troubleshoot
it in case of bugs as well as extending it.


Table of Contents
-----------------

.. toctree::
  :maxdepth: 2


Installation
------------

A Makefile serves as a summary of all important commands to set up the development environment.
The same Makefile is used for testing and linting in the CI.

To create a new environment, install dependencies and pre-commit hooks, run this command:

:code:`make setup`


For instructions on how to install and use :code:`make` on **Windows**, check out
`this wiki <https://github.gamma.bcg.com/cpg-ai/onboarding/wiki/Windows-Setup-(WSL,-Make,-python-venv)>`_.

Packages
--------

.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   this_package_does_not_exist

Coding Standards
________________

We use :code:`black`, :code:`flake8` and :code:`isort` defaults with 120 columns per line.
Additionally, the following conventions are followed:

* Project names must be lowercased
* PEP 8 conventions apply, unless specified for a *Very Good Reason*.
* Simplicity should *always* be prefered over performance, unless specified for a *Very Good Reason*.
