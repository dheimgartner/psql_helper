"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = psql_helper.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
from ast import IsNot
import logging
import sys
import os
import getpass
from dotenv import find_dotenv, load_dotenv, dotenv_values, set_key

from psql_helper import __version__

__author__ = "dheimgartner"
__copyright__ = "dheimgartner"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from psql_helper.skeleton import fib`,
# when using this Python module as a library.
def missing_dotenv():
    """Missing dotenv"""
    if not find_dotenv():
        return True
    else:
        return False


def already_initialized(db):
    """DB already initialized"""
    pw = db + "_PASSWORD"
    if (os.getenv(pw) is not None):
        return True
    else:
        return False


def db_set_up(db="MULTIMODALITY", dbname ="multimodality", host="id-hdb-psgr-ct17.ethz.ch", user="multimod", port="5432", install=False, overwrite=False, path_env="~"):
    """Save db creds to env var

    Args:
        db (str, optional): db shorthand. Defaults to "MULTIMODALITY".
        dbname (str, optional): db name. Defaults to "multimodality".
        host (str, optional): host name. Defaults to "id-hdb-psgr-ct17.ethz.ch".
        user (str, optional): user name. Defaults to "multimod".
        port (str, optional): port. Defaults to "5432".
        install (bool, optional): write to env. Defaults to False.
        overwrite (bool, optional): overwrite if already exists. Defaults to False.
    """
    load_dotenv()
    existing_env = dotenv_values()
    params = {"DB": db, "DBNAME": dbname, "HOST": host, "USER": user, "PORT": port}

    if (not install):
        print("Env vars will not persist. Consider install=True")
        os.environ[db + "_DBNAME"] = dbname
        os.environ[db + "_HOST"] = host
        os.environ[db + "_USER"] = user
        os.environ[db + "_PORT"] = port
        os.environ[db + "_PASSWORD"] = getpass.getpass()

    file = os.path.expanduser(path_env + "/.env")

    if install:
        # init .env file
        if missing_dotenv():
            try:
                open(file, "a").close()
            except OSError:
                print("Failed creating the file")
            else:
                print("File created under " + file)

        # check if already initialized and overwrite=True
        if (already_initialized(db) & (not overwrite)):
            raise Exception("db already set up. Consider overwrite=True")
        
        for key, value in params.items():
            if key == "DB":
                continue
            key_combined = db + "_" + key
            set_key(file, key_to_set=key_combined, value_to_set=value)

        pw_key = db + "_PASSWORD"
        set_key(file, pw_key, getpass.getpass())



## TODO: write assert functions (with exeptions?) and write tests




def assert_init(db):
    """Assert `db_set_up()` has been called

    Args:
        db (str): db shorthand
    """    
    assertIsNotNone(os.getenv(db + "_PASSWORD")), "Call db_set_up() first!"



def test_assert(db):
    assert_init(db)


def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for _i in range(n - 1):
        a, b = b, a + b
    return a


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version="psql_helper {ver}".format(ver=__version__),
    )
    parser.add_argument(dest="n", help="n-th Fibonacci number", type=int, metavar="INT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    print("The {}-th Fibonacci number is {}".format(args.n, fib(args.n)))
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m psql_helper.skeleton 42
    #
    run()
