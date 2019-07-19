"""Pyjano stands for Python Jana Orchestrator

The packet contains tools and python wrappers that allows to run JANA2 and eic-JANA frameworks
processes from python. The python also provides IPython widgets and interactive controls
"""
import itertools
import os
from time import sleep

import click

from ipywidgets import Button, IntProgress, HBox


def is_notebook():
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def enable_interactive_jsroot():
    """Fixes CERN.root issue with requirejs in Jupyterlab
    https://github.com/root-project/jsroot/issues/166
    """
    from IPython.display import Javascript, display
    display(Javascript("""
    if (typeof require === 'undefined') {
        var s = document.createElement('script');
        s.src='https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js';
        document.body.appendChild(s);
    }
    """))


@click.group(invoke_without_command=True)
@click.option('--debug/--no-debug', default=False)
@click.option('--top-dir', default="")
@click.pass_context
def ejpm_cli(ctx, debug, top_dir):
    """EJPM stands for EIC Jana Packet Manager"""
    pass



if __name__ == "__main__":
    print(is_notebook())

