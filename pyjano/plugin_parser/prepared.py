# This is prepared plugin DB for test purpuses
from markupsafe import Markup

plugins = [
    {'name': 'lund_reader', 'type': 'reader'},
    {'name': 'beagle_reader', 'type': 'reader'},
    {'name': 'hepmc_reader', 'type': 'reader'},
    {'name': 'jleic_geant_reader', 'type': 'reader'},
    {'name': 'jleic_gemc_reader', 'type': 'reader'},
    {'name': 'jana', 'type': ''},
    {'name': 'eic_smear', 'type': ''},
    {'name': 'trk_eff', 'type': ''},
    {'name': 'jleic_iff', 'type': ''},
    {'name': 'jleic_occupancy', 'type': ''},
    {'name': 'vmeson', 'type': ''},
    {'name': 'open_charm', 'type': ''},
]

plugins_by_name = {p['name']: p for p in plugins}

def prepare_plugins():
    """Sets predefined values for plugins set"""

    # all plugins have some help and verbosity level
    for plugin in plugins:
        plugin['help'] = plugin['name'] + " help"
        plugin['config'] = [
            {'name': 'verbose', 'type': 'int', 'value': 0, 'help': Markup('verbosity level: 0 - silent, 2 - print all')}
        ]

    #
    # === jana - general flags ===
    plugins_by_name['jana']['help'] = Markup("""
          General configuration for JANA2 framework itself<br>          
          <br>
          <a href="https://jeffersonlab.github.io/JANA2/Installation.html" target='_blank'>More documentation</a>
          """)

    plugins_by_name['jana']['config'].extend(
        [
            {'name': 'nevents', 'type': 'int', 'value': 0, 'help': Markup('Number of events to process. 0 = all')},
            {'name': 'nskip', 'type': 'int', 'value': 0, 'help': Markup('Number of events to skip')},
            {'name': 'nthreads', 'type': 'float', 'value': 5, 'help': Markup('Number of processing threads')},
        ]
    )

    #
    # === beagle_reader ===
    plugins_by_name['beagle_reader']['help'] = Markup("""
       Opens files from BeAGLE event generator as a data source<br>
       <strong>BeAGLE</strong> - <strong>Be</strong>nchmark <strong>eA</strong> <strong>G</strong>enerator for <strong>LE</strong>ptoproduction 
       <br>
       <a href="https://wiki.bnl.gov/eic/index.php/BeAGLE" target='_blank'>Documentation</a>

       """)

    # === lund_reader ===
    plugins_by_name['lund_reader']['help'] = Markup("""
       Opens files in LUND format.
       <p>It is a text format. Its header defines quantities such as the number N of generated particle for each event and other kinematic properties.
       <p><a href="https://gemc.jlab.org/gemc/html/documentation/generator/lund.html"> More info </a>
       """)

    # === Open charm analysis ===
    plugins_by_name['open_charm']['help'] = Markup("""
           Makes analysis on charm particles. Extracting basic invariant masses and other parameters with or without smearing
           """)

    plugins_by_name['open_charm']['config'].extend(
        [
            {'name': 'smearing_source', 'type': 'int', 'value': 1,
             'help': Markup('Smearing type: 0 - no, 1 - basic, 2 - eic-smear, 3 ')},
            {'name': 'eEnergy', 'type': 'float', 'value': 5, 'help': Markup('electron beam energy GeV')},
            {'name': 'iEnergy', 'type': 'float', 'value': 50, 'help': Markup('ion beam energy GeV ')},
        ]
    )

    plugins_by_name['lund_reader']['config'].append(

        {'name': 'smearing_source', 'type': 'int', 'value': 1,
         'help': Markup('Smearing type: 0 - no, 1 - basic, 2 - eic-smear, 3 ')}

    )

    return plugins