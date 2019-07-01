import os
import shlex
import subprocess
import sys
from datetime import datetime

from IPython.display import IFrame
from IPython.display import display, Javascript, clear_output, HTML
from ipywidgets import Button, IntProgress, HBox

from IPython import get_ipython


from pyjano import is_notebook

class ConsoleRunSink:
    def add_line(self, line):
        print(line)

    def display(self):
        print("Rendering in console")

    @property
    def is_displayed(self):
        return True

from IPython.core.display import display
from ipywidgets import widgets


class NotebookRunSink:

    def __init__(self):
        self._output_widget = widgets.Output()
        self._is_displayed = True

    # noinspection PyTypeChecker
    def display(self):
        title_widget = widgets.HTML('<em>Vertical Box Example</em>')

        accordion = widgets.Accordion(children=[self._output_widget], selected_index=None)
        accordion.set_title(0, 'Full log')

        vbox = widgets.VBox([title_widget, accordion])

        #display(accordion)
        display(vbox)
        self._is_displayed = True

    def add_line(self, line):
        self._output_widget.append_stdout(line+'\n')

    @property
    def is_displayed(self):
        return self._is_displayed

def _run(command, output):
    """Wrapper around subprocess.Popen that returns:

    :return retval, start_time, end_time, lines
    """
    if isinstance(command, str):
        command = shlex.split(command)

    # Pretty header for the command
    pretty_header = "RUN: " + " ".join(command)
    output.add_line('=' * len(pretty_header))
    output.add_line(pretty_header)
    output.add_line('=' * len(pretty_header))

    # Record the start time
    start_time = datetime.now()
    lines = []

    # stderr is redirected to STDOUT because otherwise it needs special handling
    # we don't need it and we don't care as C++ warnings generate too much stderr
    # which makes it pretty much like stdout
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = process.stdout.readline().decode('latin-1').replace('\r', '\n')

        if process.poll() is not None and line == '':
            break
        if line:
            if line.endswith('\n'):
                line = line[:-1]

            output.add_line(line)
            lines.append(line)

    # Get return value and finishing time
    retval = process.poll()
    end_time = datetime.now()

    output.add_line("------------------------------------------")
    output.add_line(f"RUN DONE. RETVAL: {retval} \n\n")

    return retval, start_time, end_time, lines

class Jana(object):

    server = None

    def __init__(self):
        self.config = {}

        self.is_notebook = is_notebook()
        if self.is_notebook:
            self.sink = NotebookRunSink()
        else:
            self.sink = ConsoleRunSink()

        self.runner = None

        self.exec_path = '/home/romanov/eic/ejana/dev/compiled/bin/ejana'
        self.plugin_search_paths = [
            '/home/romanov/eic/ejana/dev/compiled/plugins',
            '/home/romanov/eic/jana/jana-greenfield/plugins'
        ]

        self._environ_is_updated = False

    def update_environment(self):
        def print_plugin_locations(locations):
            for loc in locations:
                print(f"   {loc}")

        ex_plugin_locations = [loc for loc in os.environ.get('JANA_PLUGIN_PATH', '').split(':') if loc]
        if ex_plugin_locations and ex_plugin_locations[0]:
            print("Existing plugin locations")
            print_plugin_locations(ex_plugin_locations)

        if self.plugin_search_paths:
            print("Appending them by plugin search locations")
            print_plugin_locations(self.plugin_search_paths)

        # remove a location from existing locations. We will prepend the list anyway

        env_plugin_path = ':'.join(self.plugin_search_paths + ex_plugin_locations)
        os.environ['JANA_PLUGIN_PATH'] = env_plugin_path
        print(os.environ['JANA_PLUGIN_PATH'])
        self._environ_is_updated = True

    def configure_plugin_paths(self, plugin_paths):
        # The later plugin location will have greater load priority
        # This means that it must be earlier in the list
        for path in plugin_paths:
            try:
                self.plugin_search_paths.remove(path)
            except ValueError:
                pass   # no such path

            self.plugin_search_paths.insert(0, path)

        self._environ_is_updated = False

    def configure(self, plugins=None, flags=None, in_files=None, params='', plugin_paths=None):
        if plugins:
            self.config['plugins'] = plugins
        if flags:
            self.config['flags'] = flags
        if in_files:
            self.config['input_files'] = in_files

        if plugin_paths:
            self.configure_plugin_paths(plugin_paths)


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
        if self.is_notebook:
            display(Javascript('console.log("hello world")', lib='https://code.jquery.com/jquery-3.4.1.slim.js'))
            clear_output()
            display(HTML('<b>JANA</b> loaded...'))

    def plugins_gui(self):
        # display(IFrame('http://127.0.0.1:5000', width='100%', height=550))
        #from pyjano.server import create_server
        #server = create_server()

        from pyjano.server.jana import offline_render
        display(widgets.HTML(offline_render()))


    def start_gui(self):
        # display(IFrame('http://127.0.0.1:5000/start', width='100%', height=170))
        self.sink.display()

    def get_plugins_html(self):
        pass






    def run(self):
        if not self._environ_is_updated:
            self.update_environment()

        if not self.sink.is_displayed:
            self.sink.display()

        command = f"""{self.exec_path}
            -Pplugins=hepmc_reader,open_charm
            -Popen_charm:e_beam_energy=5
            -Popen_charm:ion_beam_energy=100
            -Pnevents=10000
            -Pnthreads=1
            /mnt/c/eic/data/herwig6_e-p_5x100.hepmc
            -PJANA:DEBUG_PLUGIN_LOADING=1
        """
        _run(command, self.sink)

if __name__ == "__main__":
    jana = Jana()
    jana.start_gui()
    jana.run()