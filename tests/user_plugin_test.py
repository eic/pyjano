from pyjano.jana import Jana
import os
from pyjano.jana.user_plugin import PluginFromSource

my_plugin = PluginFromSource('/home/romanov/eic/minimal_example', name='minimal_example')

jana = Jana()
jana.plugin('lund_reader') \
    .plugin('jana', nevents=1000, output='mydiHadSmearedOut.root') \
    .plugin(my_plugin, verbose=2) \
    .source('/home/romanov/Downloads/pipi.lund')\
    .run()
