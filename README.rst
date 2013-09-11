fundfind - an Open way to share, visualise and map out scholarly funding opportunities

How It Works
============

Up and running at http://fundfind.cottagelabs.com

Just hop in and search for (or share!) funding opportunities!

You can also look at, download and reuse nice visualisations and maps of scholarly / scientific funding across the world.

FundFind also exposes **all** the funding opportunities it knows about via a machine-friendly ReSTful API under a Creative Commons Attribution 3.0 License. So you can integrate FundFind data into your software. A "permissions" feature is planned however, allowing people to submit funding information to a running fundfind instance for private purposes only (e.g. sharing only with a certain group of users). CC-BY will then become the default option.

Install
=======

NOTE: this is only for people who want to run their own instance of FundFind. If you just want to find/share/visualise funding information, go to http://fundfind.cottagelabs.com .

1. Install stuff:
  - Python_ (2.7+ preferable; NOT TESTED on 3.x)
  - ElasticSearch_ (0.19 series) (tested and should run on 0.17 and up)

2. [optional] Create a virtualenv and enable it::

    # in bash
    virtualenv {myenv}
    . {myenv}/bin/activate

3. Get the source::

    # by convention we put it in the virtualenv but you can put anywhere
    mkdir {myenv}/src
    git clone https://github.com/cottagelabs/fundfind {myenv}/src/

4. Install the app::

    cd {myenv}/src/fundfind
    # for dev install:
    pip install -e .

5. Run the webserver::

    python fundfind/web.py

.. _Python: http://www.python.org/
.. _ElasticSearch: http://www.elasticsearch.org/
