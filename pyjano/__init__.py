import itertools
import os
from time import sleep

import click
from IPython.display import IFrame
from IPython.display import display, Javascript, clear_output, HTML
from ipywidgets import Button, IntProgress, HBox


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



class Jana(object):

    def __init__(self):
        self.config = {}

    def configure(self, plugins=None, flags=None, in_files=None, params=''):
        if plugins:
            self.config['plugins'] = plugins
        if flags:
            self.config['flags'] = flags
        if in_files:
            self.config['input_files'] = in_files


        """
        <script src="integrity="sha256-BTlTdQO9/fascB1drekrDVkaKd9PkwBymMlHOiG+qLI=" crossorigin="anonymous"></script>
		"""

        script = """
            window.onload = function() {
                if (window.jQuery) {  
                    // jQuery is loaded  
                    console.log("Yeah!");
                } else {
                    // jQuery is not loaded
                    console.log("Doesn't Work");
                }
            }
        """

        # noinspection PyTypeChecker
        display(Javascript('console.log("hello world")', lib='https://code.jquery.com/jquery-3.4.1.slim.js'))
        clear_output()
        display(HTML('<b>JANA</b> loaded...'))

    def plugins_gui(self):

        display(IFrame('http://127.0.0.1:5000', width='100%', height=550))

    def start_gui(self):
        display(IFrame('http://127.0.0.1:5000/start', width='100%', height=170))

    def run(self):
        sleep(3)
        display(HTML(

            """
            ejana -Pplugins=hepmc_reader,open_charm -Popen_charm:smearing=1 -Pnevents=1000  /home/romanov/ceic/data/herwig6_e-p_5x100.hepmc
getcwd: /mnt/c/eic/pyjano_proto
[INFO] Adding source: /home/romanov/ceic/data/herwig6_e-p_5x100.hepmc

[INFO] Initializing plugin "/home/romanov/eic/ejana/dev/compiled/plugins/hepmc_reader.so"
[INFO] Initializing plugin "/home/romanov/eic/ejana/dev/compiled/plugins/open_charm.so"
Suppressed exception in JEventSourceManager::GetUserEventSourceGenerator!
Opening source "/home/romanov/ceic/data/herwig6_e-p_5x100.hepmc" - JEventSource_hepmc : BeAGLE generated Text file
JEventSource_hepmc: Opening TXT file /home/romanov/ceic/data/herwig6_e-p_5x100.hepmc
[INFO] Creating 8 processing threads ...

                    Config. Parameters
  =======================================================
             name                          value
  --------------------------   --------------------------
                    AFFINITY = 0
   JANA:DEBUG_PLUGIN_LOADING = 0
    JANA:DEBUG_THREADMANAGER = 0
   JANA:MAX_NUM_OPEN_SOURCES = 1
      JANA:QUEUE_DEBUG_LEVEL = 0
   JANA:TASK_POOL_DEBUGLEVEL = 0
         JANA:TASK_POOL_SIZE = 200
     JANA:THREAD_DEBUG_LEVEL = 0
  JANA:THREAD_ROTATE_SOURCES = 1
   JANA:THREAD_SLEEP_TIME_NS = 100
                     nevents = 1000
                       nskip = 0
                    NTHREADS = 8
         open_charm:smearing = 1
                     plugins = hepmc_reader,open_charm
     ROOT:EnableThreadSafety = 1

Start processing ...
OpenCharmProcessor: Init()

--------- EVENT 0 ---------
All threads have ended.  263.8 Hz (399.8 Hz avg)
Event processing ended.
OpenCharmProcessor::Finish(). Cleanup

Final Report
------------------------------------------------------------------------------
Source                                              Nevents  Queue   NTasks
------------------------------------------------------------------------------
/home/romanov/ceic/data/herwig6_e-p_5x100.hepmc        1000  Events  999

Total events processed: 1000 (~ 1000.0 evt)
Integrated Rate: 395.5 Hz

[INFO] JResourcePoolSimple<JFactorySet>::~JResourcePool: Deleted 8 items (8 expected).

            """.replace('\n', '<br>').replace('INFO', '<span style="color:blue">INFO</span>')
        ))

if __name__ == '__main__':
    ejpm_cli()
