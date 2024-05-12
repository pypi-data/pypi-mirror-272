.. contents:: **pytest-discord**
   :backlinks: top
   :depth: 2


Summary
============================================
|PyPI pkg ver| |Supported Python ver| |Supported Python impl| |CI status| |Test coverage| |CodeQL|

.. |PyPI pkg ver| image:: https://badge.fury.io/py/pytest-discord.svg
    :target: https://badge.fury.io/py/pytest-discord
    :alt: PyPI package version

.. |Supported Python impl| image:: https://img.shields.io/pypi/implementation/pytest-discord.svg
    :target: https://pypi.org/project/pytest-discord
    :alt: Supported Python implementations

.. |Supported Python ver| image:: https://img.shields.io/pypi/pyversions/pytest-discord.svg
    :target: https://pypi.org/project/pytest-discord
    :alt: Supported Python versions

.. |CI status| image:: https://github.com/thombashi/pytest-discord/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/thombashi/pytest-discord/actions/workflows/ci.yml
    :alt: CI status of Linux/macOS/Windows

.. |Test coverage| image:: https://coveralls.io/repos/github/thombashi/pytest-discord/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/pytest-discord?branch=master
    :alt: Test coverage: coveralls

.. |CodeQL| image:: https://github.com/thombashi/pytest-discord/actions/workflows/github-code-scanning/codeql/badge.svg
    :target: https://github.com/thombashi/pytest-discord/actions/workflows/github-code-scanning/codeql
    :alt: CodeQL

A pytest plugin to notify test results to a Discord channel.


Installation
============================================
::

    pip install pytest-discord


Quick start
============================================

Making a Discord webhook
--------------------------------------------
`Intro to Webhooks – Discord <https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks>`__


Usage
--------------------------------------------
Set a webhook URL when executing ``pytest`` via ``--discord-webhook`` option:

::

    $ pytest --discord-webhook=<https://discordapp.com/api/webhooks/...>

.. figure:: https://cdn.jsdelivr.net/gh/thombashi/pytest-discord@master/ss/pytest-discord.png
    :scale: 80%
    :alt: https://github.com/thombashi/pytest-discord/blob/master/ss/pytest-discord.png

    Notification message example

Or, set a webhook URL to an environment variable ``PYTEST_DISCORD_WEBHOOK``:

::

    $ export PYTEST_DISCORD_WEBHOOK=<https://discordapp.com/api/webhooks/...>
    $ pytest

Or, you can specify a webhook URL of a discord channel via ``ini-options`` (described later).


Increase the verbosity level
--------------------------------------------
::

    $ pytest --discord-verbose=1

.. figure:: https://cdn.jsdelivr.net/gh/thombashi/pytest-discord@master/ss/pytest-discord_verbose.png
    :scale: 80%
    :alt: https://github.com/thombashi/pytest-discord/blob/master/ss/pytest-discord_verbose.png

    Notification message example

Notification messages may omit information caused by Discord limitations (especially when errors occur).
You can get full messages as an attached markdown file with ``--discord-attach-file`` option.


Options
============================================

Command options
--------------------------------------------
::

    notify test results to a discord channel:
      --discord-webhook=WEBHOOK_URL
                            discord webhook url of a discord channel to notify pytest results. you can also specify the value with PYTEST_DISCORD_WEBHOOK environment variable.
      --discord-verbose=VERBOSITY_LEVEL
                            Verbosity level for pytest-discord.
                            If not set, use the verbosity level of pytest.
                            Defaults to 0.
                            you can also specify the value with PYTEST_DISCORD_VERBOSE environment variable.
      --discord-username=DISCORD_USERNAME
                            name for a message. defaults to pytest. you can also specify the value with PYTEST_DISCORD_USERNAME environment variable.
      --discord-success-icon=ICON_URL
                            url to an icon of a successful run. you can also specify the value with PYTEST_DISCORD_SUCCESS_ICON environment variable.
      --discord-skip-icon=ICON_URL
                            url to an icon of a skipped run. you can also specify the value with PYTEST_DISCORD_SKIP_ICON environment variable.
      --discord-fail-icon=ICON_URL
                            url to an icon of a failed run. you can also specify the value with PYTEST_DISCORD_FAIL_ICON environment variable.
      --discord-attach-file
                            post pytest results as a markdown file to a discord channel. you can also specify the value with PYTEST_DISCORD_ATTACH_FILE environment variable.


ini-options
--------------------------------------------
[pytest] ini-options in the first ``pytest.ini``/``tox.ini``/``setup.cfg``/``pyproject.toml (pytest 6.0.0 or later)`` file found:

::

  discord_webhook (string):
                        discord webhook url of a discord channel to notify pytest results.
  discord_verbose (string):
                        Verbosity level for pytest-discord. If not set, use the verbosity level of pytest. Defaults to 0.
  discord_username (string):
                        name for a message. defaults to pytest.
  discord_success_icon (string):
                        url to an icon of a successful run.
  discord_skip_icon (string):
                        url to an icon of a skipped run.
  discord_fail_icon (string):
                        url to an icon of a failed run.
  discord_attach_file (bool):
                        post pytest results as a markdown file to a discord channel.

:Example of ``pyproject.toml``:
    .. code-block:: toml

        [tool.pytest.ini_options]
        discord_webhook = "https://discordapp.com/api/webhooks/..."
        md_report_verbose = 1

:Example of ``setup.cfg``:
    .. code-block:: ini

        [tool:pytest]
        discord_webhook = https://discordapp.com/api/webhooks/...
        md_report_verbose = 1


Dependencies
============================================
- Python 3.8+
- `Python package dependencies (automatically installed) <https://github.com/thombashi/pytest-discord/network/dependencies>`__
