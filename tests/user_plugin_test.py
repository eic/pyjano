from pyjano.jana import Jana, PluginFromSource

my_plugin = PluginFromSource('/home/romanov/eic/minimal_example', name='minimal_example')

jana = Jana()
jana.plugin('lund_reader') \
    .plugin('jana', nevents=1000, output='mydiHadSmearedOut.root') \
    .plugin(my_plugin, verbose=1) \
    .source('/home/romanov/Downloads/pipi.lund')\
    .run()
