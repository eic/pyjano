import unittest
import os
from pprint import pprint

from pyjano.jana.user_plugin import PluginCmakeBuildManager


class TestPluginCmakeBuildManager(unittest.TestCase):

    #def setUp(self) -> None:


    # def test_vmeson_beagle(self):
    #     bm = PluginCmakeBuildManager('minimal_example')
    #     self.assertEqual(bm.config['plugin_path'], 'minimal_example')

    def test_build(self):
        bm = PluginCmakeBuildManager('minimal_example', name='MiniPlugin')
        pprint(bm.config)
        bm.cmake_configure()
        bm.build()


if __name__ == '__main__':
    unittest.main()