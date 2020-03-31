from pyjano.jana import Jana
import os

jana = Jana()
#jana.exec_path = os.environ['EJANA_HOME']
#jana.plugin_search_paths=['/home/romanov/eic/ejana/dev/cmake-build-debug']
jana.plugin('lund_reader') \
    .plugin('jana', nevents=1000, output='mydiHadSmearedOut.root') \
    .plugin('eic_smear') \
    .plugin('event_writer') \
    .plugin('vmeson')\
    .source('/home/romanov/Downloads/pipi.lund')\
    .run()