import itertools
import os
from time import sleep

import click
from IPython import get_ipython
from IPython.display import IFrame
from IPython.display import display, Javascript, clear_output, HTML
from ipywidgets import Button, IntProgress, HBox




def is_notebook():
    try:

        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter

@click.group(invoke_without_command=True)
@click.option('--debug/--no-debug', default=False)
@click.option('--top-dir', default="")
@click.pass_context
def ejpm_cli(ctx, debug, top_dir):
    """EJPM stands for EIC Jana Packet Manager"""
    pass

def gen(max):
    num = 0
    while num < max:
        # instead of sleep, extract event number here
        sleep(0.01)
        yield num*1000
        num += 1

class ControlWidget:
    def __init__(self, sequence, size=None, every=None, name='Events'):
        self.__button = Button(description='Run', icon='play')
        self.__progress = IntProgress(min=0, max=1, value=0)
        self.__label = HTML()
        self.__box = HBox(children=[self.__button, self.__progress, self.__label])
        self.__button.on_click(self.__on_click)
        self.__every = every
        self.__is_size_unknown = False
        self.name = name
        self.__size = size
        self.set_new_sequence(sequence, size, every, name)

    def __on_click(self, b):
        self.__sequence, seq = itertools.tee(self.__sequence)
        index = 0
        try:
            for index, record in enumerate(seq, 1):
                if index == 1 or index % self.__every == 0:
                    if self.__is_size_unknown:
                        self.__progress.value = 1
                        self.__label.value = '{name}: {index} / ?'.format(
                            name=self.name,
                            index=index
                        )
                    else:
                        self.__progress.value = index
                        self.__label.value = u'{name}: {index} / {size}'.format(
                            name=self.name,
                            index=index,
                            size=self.__size
                        )
                # yield record
        except:
            self.__progress.bar_style = 'danger'
            raise
        else:
            self.__progress.bar_style = 'success'
            self.__progress.value = index
            self.__label.value = "{name}: {index}".format(
                name=self.name,
                index=str(index or '?')
            )

    def set_new_sequence(self, seq, size=None, every=None, name='Events'):
        self.__sequence = seq
        self.name = name

        self.__is_size_unknown = False
        self.__size = size
        self.__every = every
        if size is None:
            try:
                self.__size = len(seq)
            except TypeError:
                self.__is_size_unknown = True
        if size is not None:
            if every is None:
                if size <= 200:
                    self.__every = 1
                else:
                    self.__every = int(size / 200)
        else:
            if every is None:
                self.__every = 1

        if self.__is_size_unknown:
            self.__progress.min = 0
            self.__progress.max = 1
            self.__progress.value = 0
            self.__progress.bar_style = 'info'
        else:
            self.__progress.min = 0
            self.__progress.max = size
            self.__progress.value = 0
            self.__progress.bar_style = ''

    def draw(self):
        display(self.__box)

if __name__ == "__main__":
    print(is_notebook())

