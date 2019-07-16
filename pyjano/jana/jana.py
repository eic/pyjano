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

    def done(self):
        pass

    def show_running_command(self, command):
        print(f'Command = "{command}"')

    @property
    def is_displayed(self):
        return True

from IPython.core.display import display
from ipywidgets import widgets


class NotebookRunSink:

    def __init__(self):
        self._output_widget = widgets.Output()
        self._is_displayed = True
        self._label = widgets.Label(value="Initializing...")
        self._stop_button = widgets.Button(
                        description='Terminate',
                        disabled=False,
                        button_style='', # 'success', 'info', 'warning', 'danger' or ''
                        tooltip='Terminate jana process',
                        #icon='check'
                    )
        self._command_label = widgets.HTML()

    # noinspection PyTypeChecker
    def display(self):
        #title_widget = widgets.HTML('<em>Vertical Box Example</em>')
        self._stop_button.layout.display = ''
        control_box = widgets.HBox([self._stop_button, self._label])

        accordion = widgets.Accordion(children=[self._output_widget, self._command_label], selected_index=None)
        accordion.set_title(0, 'Full log')
        accordion.set_title(1, 'Run command')

        vbox = widgets.VBox([control_box, accordion])

        #display(accordion)
        display(vbox)
        self._is_displayed = True

    def add_line(self, line):
        to_show = [
            'Initializing plugin',
            'Total events processed',
            'events processed'
        ]

        tokens = line.split('\n')
        for token in tokens:
            for test in to_show:
                if test in token:
                    self._label.value = token

        self._output_widget.append_stdout(line+'\n')

    def done(self):
        self._stop_button.layout.display = 'none'

    def show_running_command(self, command):
        tokens = shlex.split(command)
        self._command_label.value = '<br>'.join(tokens)

    @property
    def is_displayed(self):
        return self._is_displayed


def _run(command, sink):
    """Wrapper around subprocess.Popen that returns:

    :return retval, start_time, end_time, lines
    """
    if isinstance(command, str):
        command = shlex.split(command)

    # Pretty header for the command
    sink.add_line('=' * 20)
    sink.add_line("RUN: " + " ".join(command))

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
            sink.add_line(line)
            lines.append(line)

    # Get return value and finishing time
    retval = process.poll()
    end_time = datetime.now()
    sink.done()

    sink.add_line("------------------------------------------")
    sink.add_line(f"RUN DONE. RETVAL: {retval} \n\n")

    return retval, start_time, end_time, lines

class Jana(object):
    static_content_is_inserted = False

    server = None

    def __init__(self, gui='auto'):
        self.config = {}

        if not gui:
            self.is_notebook = False
            self.sink = ConsoleRunSink()
        else:
            self.is_notebook = is_notebook()
            if (gui == 'auto' and self.is_notebook) or gui == 'notebook':
                self.sink = NotebookRunSink()
            else:
                self.sink = ConsoleRunSink()

        self.runner = None

        self.exec_path = 'ejana'
        self.plugin_search_paths = [
            '/home/romanov/eic/ejana/dev/compiled/plugins',
            '/home/romanov/eic/jana/jana-greenfield/plugins'
        ]
        self.config['params'] = {}
        self.config['plugins'] = {}
        self.config['flags'] = []
        self.config['input_files'] = []

        self._environ_is_updated = False

    def update_environment(self):
        def print_plugin_locations(locations):
            for loc in locations:
                self.sink.add_line(f"   {loc}")

        ex_plugin_locations = [loc for loc in os.environ.get('JANA_PLUGIN_PATH', '').split(':') if loc]
        if ex_plugin_locations and ex_plugin_locations[0]:
            self.sink.add_line("Existing plugin locations")
            print_plugin_locations(ex_plugin_locations)

        if self.plugin_search_paths:
            self.sink.add_line("Appending them by plugin search locations")
            print_plugin_locations(self.plugin_search_paths)

        # remove a location from existing locations. We will prepend the list anyway

        env_plugin_path = ':'.join(self.plugin_search_paths + ex_plugin_locations)
        os.environ['JANA_PLUGIN_PATH'] = env_plugin_path
        #print(os.environ['JANA_PLUGIN_PATH'])
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


    def configure_plugins(self, plugins):
        self.config['plugins'] = {}
        if not plugins:
            return self.config['plugins']

        def _update(plugin_name, plugin_data):
            if plugin_name == 'jana' and plugin_data:
                self.config['params'] = plugin_data
            else:
                self.config['plugins'][plugin_name] = plugin_data

        assert isinstance(plugins, list)
        for item in plugins:
            if isinstance(item, str):
                _update(item, {})
            elif isinstance(item, tuple) or isinstance(item, list):
                # plugin in form:
                # ('name', {config})
                assert isinstance(item[1], dict)
                _update(item[0], item[1])
            else:
                assert isinstance(item, dict)
                # dict must be with one key like:
                # {'beagle_reader': { ... configs ... }}
                plugin_name = list(item)[0]
                _update(plugin_name, item[plugin_name])

        return self.config['plugins']

    def configure(self, plugins=None, flags=None, files=None, params=None, plugin_paths=None):
        if plugins:
            self.configure_plugins(plugins)
        if params:
            if self.config['params']:
                self.config['params'].update(params)
            else:
                self.config['params']=params
        if flags:
            self.config['flags'] = flags
        if files:
            self.config['input_files'] = files

        if plugin_paths:
            self.configure_plugin_paths(plugin_paths)


        # noinspection PyTypeChecker
        if self.is_notebook:
            #display(Javascript('console.log("hello world")', lib='https://code.jquery.com/jquery-3.4.1.slim.js'))
            clear_output()
            display(HTML('<b>JANA</b> configured...'))

    def interactive_notebook(self):

        '/static/css/bootstrap.min.css'

        display(HTML("""        
        <link rel="stylesheet" href="/static/css/bootstrap.min.css" crossorigin="anonymous">
        <script src="/static/js/bootstrap.min.js"></script>        
        <script src="/static/js/plugins.js"></script>        
        <link rel="stylesheet" href="/static/css/pretty-checkbox.min.css">
        '<b>Pyjano</b> jupyter notebook interactive loaded...'        
        """))

    def plugins_gui(self):
        #display(IFrame('http://localhost:8888/pyjano', width='100%', height=550))
        #from pyjano.server import create_server
        #server = create_server()

        from pyjano.server.jana import offline_render
        display(widgets.HTML(offline_render()))
        display(Javascript("""
            if(typeof jQuery=='undefined') {
                var headTag = document.getElementsByTagName("head")[0];
                var jqTag = document.createElement('script');
                jqTag.type = 'text/javascript';
                jqTag.src = '/static/jsroot/libs/jquery.js';
                jqTag.onload = activatePluginsGui;
                headTag.appendChild(jqTag);
            } else {
                 activatePluginsGui();
            }
                """))


    def start_gui(self):
        display(IFrame('http://localhost:8888/pyjano/start', width='100%', height=170))
        #self.sink.display()

    def get_plugins_html(self):
        pass

    def run(self):
        if not self._environ_is_updated:
            self.update_environment()

        #if not self.sink.is_displayed:
        self.sink.display()
        command = f"""{self.exec_path} {self.get_run_command()} -Pjana:debug_plugin_loading=1 """
        self.sink.show_running_command(command)
        _run(command, self.sink)

    def get_run_command(self):
        add_plugins_str = "-Pplugins=" + ",".join(self.config['plugins'].keys())
        plugins_params_str = ""
        for plugin_name, plugin_params in self.config['plugins'].items():
            if plugin_params:
                for name, value in plugin_params.items():
                    plugins_params_str += f' -P{plugin_name}:{name}={value}'

        params_str = " ".join([f'-P{name}={value}' for name, value in self.config['params'].items()])
        files_str = " ".join([file for file in self.config['input_files']])
        flags_str = " ".join([flag for flag in self.config['flags']])
        return f'{add_plugins_str} {plugins_params_str} {params_str}  {files_str} {flags_str}'


if __name__ == "__main__":
    jana = Jana()
    jana.configure(
        plugins=[  # a list of plugins to use:
            'beagle_reader',    # plugin name, no additional parameters
            {'open_charm': {    # add vmeson plugin & set '-Pvmeson:verbose=2' parameter
                'verbose': 1,   # Set verbose mode for that plugin
                'smearing': 1}  # Set smearing mode
            },
        ],
        files=["/home/romanov/ceic/data/herwig6_e-p_5x100.hepmc"],
        # or [list, of, files]
        params={'nthreads': 4, 'nevents': 2000}  # for parameters that don't follow <plugin>:<name> naming
        # Smart enough to run it like --nthreads=8
    )  # instead of -P...

    print(jana.get_run_command())