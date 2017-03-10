git-wipe: Cleanup your fork branches which were merged as PR to parent repository
=================================================================================

.. image:: https://img.shields.io/pypi/v/git-wipe.svg
    :target: https://pypi.python.org/pypi/git-wipe

.. image:: https://img.shields.io/pypi/l/git-wipe.svg
    :target: https://pypi.python.org/pypi/git-wipe

.. image:: https://img.shields.io/pypi/pyversions/git-wipe.svg
    :target: https://pypi.python.org/pypi/git-wipe

.. image:: https://coveralls.io/repos/github/povils/git-wipe/badge.svg?branch=master
    :target: https://coveralls.io/github/povils/git-wipe?branch=master

.. image:: https://travis-ci.org/povils/git-wipe.svg?branch=master
    :target: https://travis-ci.org/povils/git-wipe

---------------


The problem
-----------------
From time to time if you have many forks and do many pull requests it is inevitable that you will have stale branches. And as time marches on the number of these branches across forks can become big.

The answer
-----------
**git-wipe** is simple command line tool to cleanup your Github fork branches.

Install
-------

::

    $ pip install git-wipe

Usage
------
In order to use **git-wipe** first you need to create your `Personal Access Token <https://github.com/settings/tokens>`_.

You can set this token to your environment variable:

::

    $ export GIT_WIPE_TOKEN=your_access_token

And then you can easily:


::

    $ git-wipe cleanup
    Searching for branches. This may take a while...
    Founded branches:

    povils/repo_1/Branch_1
    povils/repo_1/Branch_2
    povils/repo_2/Branch_1
    povils/repo_3/Branch_1

    Total: 4
    Delete these branches? [y/N]: y


Other options
-------------
::

      --token              instead of environment
      --preview            just to preview merged branches
      --timeout            set connection timeout. Default 30 seconds
      --skip-repository    skip repository you don't want to search. Multiple
      --skip-branch        skip branch you don't want to delete. Multiple
      --no-interaction     do not ask any interactive question

Example:

::

    $ git-wipe cleanup --skip-repository=repo_1 --skip-branch=develop --no-interaction

This command will clean all merged branches without interaction, except from fork with name 'repo_1' and except all branches with name 'develop'

Note:
-----
Only forks where you are **owner** will be involved in search. Also **master branches will never be deleted!**

