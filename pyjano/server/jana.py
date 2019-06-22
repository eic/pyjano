from flask import session, redirect, url_for, render_template, request
from flask import Blueprint
from flask import Markup

jana_blueprint = Blueprint('main', __name__)

plugins = [
    {'name': 'lund_reader', 'type': 'reader'},
    {'name': 'beagle_reader', 'type': 'reader'},
    {'name': 'hepmc_reader', 'type': 'reader'},
    {'name': 'jleic_geant_reader', 'type': 'reader'},
    {'name': 'jleic_gemc_reader', 'type': 'reader'},
    {'name': 'trk_fit', 'type': ''},
    {'name': 'trk_eff', 'type': ''},
    {'name': 'jleic_iff', 'type': ''},
    {'name': 'jleic_occupancy', 'type': ''},
    {'name': 'vmeson', 'type': ''},
    {'name': 'open_charm', 'type': ''},
]


@jana_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""

    for plugin in plugins:
        plugin['help'] = plugin['name'] + " help"
        plugin['config'] = [
            {'name':'verbose', 'type': 'int', 'value':0, 'help':Markup('verbosity level: 0 - silent, 2 - print all')}
        ]

    plugins_by_name = {p['name']:p for p in plugins}
    plugins_by_name['beagle_reader']['help'] = Markup("""
    Opens files from BeAGLE event generator as a data source<br>
    <strong>BeAGLE</strong> - <strong>Be</strong>nchmark <strong>eA</strong> <strong>G</strong>enerator for <strong>LE</strong>ptoproduction 
    <br>
    <a href="https://wiki.bnl.gov/eic/index.php/BeAGLE" target='_blank'>Documentation</a>
    
    """)

    plugins_by_name['lund_reader']['help'] = Markup("""
    Opens files in LUND format.
    <p>It is a text format. Its header defines quantities such as the number N of generated particle for each event and other kinematic properties.
    <p><a href="https://gemc.jlab.org/gemc/html/documentation/generator/lund.html"> More info </a>
    """)

    plugins_by_name['open_charm']['help'] = Markup("""
        Makes analysis on charm particles. Extracting basic invariant masses and other parameters with or without smearing
        """)

    plugins_by_name['open_charm']['config'].extend(

            [
                {'name': 'smearing_source', 'type': 'int', 'value': 1, 'help': Markup('Smearing type: 0 - no, 1 - basic, 2 - eic-smear, 3 ')},
                {'name': 'eEnergy', 'type': 'float', 'value': 5, 'help': Markup('electron beam energy GeV')},
                {'name': 'iEnergy', 'type': 'float', 'value': 50, 'help': Markup('ion beam energy GeV ')},
            ]
    )

    plugins_by_name['lund_reader']['config'].append(

        {'name': 'smearing_source', 'type': 'int', 'value': 1,
         'help': Markup('Smearing type: 0 - no, 1 - basic, 2 - eic-smear, 3 ')}

    )

    return render_template('plugins.html', layout="short", plugins=plugins)
#
#
@jana_blueprint.route('/full', methods=['GET', 'POST'])
def full():
    """Login form to enter a room."""

    for plugin in plugins:
        plugin['help'] = plugin['name'] + " help"
        plugin['config'] = [
            {'name': 'verbose', 'type': 'int', 'value': 0, 'help': Markup('verbosity level: 0 - silent, 2 - print all')}
        ]

    plugins_by_name = {p['name']: p for p in plugins}
    plugins_by_name['beagle_reader']['help'] = Markup("""
    Opens files from BeAGLE event generator as a data source<br>
    <strong>BeAGLE</strong> - <strong>Be</strong>nchmark <strong>eA</strong> <strong>G</strong>enerator for <strong>LE</strong>ptoproduction
    <br>
    <a href="https://wiki.bnl.gov/eic/index.php/BeAGLE" target='_blank'>Documentation</a>

    """)

    plugins_by_name['lund_reader']['help'] = Markup("""
    Opens files in LUND format.
    <p>It is a text format. Its header defines quantities such as the number N of generated particle for each event and other kinematic properties.
    <p><a href="https://gemc.jlab.org/gemc/html/documentation/generator/lund.html"> More info </a>
    """)

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

    return render_template('plugins.html', layout="full", plugins=plugins)


@jana_blueprint.route('/start', methods=['GET', 'POST'])
def start_gui():
    """Login form to enter a room."""

    return render_template('start.html', layout="full", plugins=plugins)

@jana_blueprint.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)
