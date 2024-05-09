=======
Pop-cli
=======

A cli interface for pop that exposes a persistent hub on the command line.

Getting Started
===============

First off, install ``cPop`` from pypi:

.. code-block:: bash

    pip3 install pop-cli



You can now initialize pop from the cli:

.. code-block:: bash

    python -m hub my_sub.init.cli

or:

.. code-block:: bash

    hub my_sub.init.cli

Specify a namespace that should host the authoritative CLI by calling using --cli as the first argument:

.. code-block:: bash

    hub --cli=my_app my_sub.init.cli

If you don't specify a --cli, unknown args will be forwarded as parameters to the reference you give:


.. code-block:: bash

    hub pop.test.func arg1 arg2 --kwarg1=asdf --kwarg2 asdf


You can access anything that is on the hub, this is very useful for debugging.

Try this to see the subs that made it onto the hub:

.. code-block:: bash

    hub _subs

You can do this to see everything that made it into hub.OPT:

.. code-block:: bash

    hub OPT

Start an interactive python shell that includes a hub and allows async code to be run:

.. code-block:: bash

    hub -i
    #>>> await hub.lib.asyncio.sleep(0)


Release
=======
The following steps are how to release a project with hatch

.. code-block:: bash

    pip install .\[build\]
    hatch build
    export HATCH_INDEX_USER="__token__"
    export HATCH_INDEX_AUTH="pypi-api-token"
    hatch publish


Documentation
=============

Check out the docs for more information:

https://pop.readthedocs.io

There is a much more in depth tutorial here, followed by documents on how to
think in Plugin Oriented Programming. Take your time to read it, it is not long
and can change how you look at writing software!
