import os
import shutil
import unittest
import wget

from pyjano.jana.generator import generate_mini_plugin
from pyjano.jana import Jana, PluginFromSource


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.plugin_name = "test_mini_plugin"
        self.this_dir = os.path.dirname(__file__)
        self.plugin_path = os.path.join(self.this_dir, self.plugin_name)

        if os.path.isdir(self.plugin_path):
            shutil.rmtree(self.plugin_path, ignore_errors=True)

        # download test file if not there
        # https://gitlab.com/eic/escalate/workspace/raw/master/data/beagle_eD.txt
        self.file_name = 'beagle_eD.txt'

    def test_something(self):
        generate_mini_plugin(plugin_name=self.plugin_name, class_name="TestMiniPlugin")

        my_plugin = PluginFromSource(self.plugin_path)
        self.assertEqual(my_plugin.name, self.plugin_name)

        jana = Jana(nevents=5, output='test_miniplugin_output.root')
        jana.plugin('beagle_reader') \
            .plugin(my_plugin, verbose=2) \
            .source(self.file_name) \
            .run(retval_raise=True)         # raise an error if not run successfully



if __name__ == '__main__':
    unittest.main()
