import os
import time
import obspython as obs

initial_load = False
status_file = ''
idle_scene = ''
playing_scene = ''

def undb(db):
    return pow(10, db/20)

def script_description():
    return 'Automatically switch scenes upon entering osu! gameplay.\n\n' \
            'See github page for setup instructions.\n\n' \
            'Stream Companion must be open to take effect.'
    
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, 'status_file', 'osu! status file location', obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, 'playing_scene', 'Scene to switch to when entering gameplay', obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, 'idle_scene', 'Scene to switch to when exiting gameplay', obs.OBS_TEXT_DEFAULT)
    return props

def script_load(settings):
    global status_file
    global idle_scene
    global playing_scene
    status_file = obs.obs_data_get_string(settings, 'status_file')
    idle_scene = obs.obs_data_get_string(settings, 'idle_scene')
    playing_scene = obs.obs_data_get_string(settings, 'playing_scene')


    # Delay check valid source until OBS is fully loaded
    obs.script_log(obs.LOG_INFO, 'Starting in 10 seconds...')
    obs.timer_add(validate_and_start, 10000)

"""
Checks if status file exists and both scenes exist, then starts the main script timer
"""
def validate_and_start():
    global initial_load
    global idle_scene
    global playing_scene
    initial_load = True
    obs.timer_remove(validate_and_start)
    obs.timer_remove(check_status_and_toggle)

    # check if file exists
    if not os.path.isfile(status_file):
        raise FileNotFoundError(f"Could not find file '{status_file}'")
    obs.script_log(obs.LOG_INFO, f'{status_file} found!')

    # check if gameplay enter scene exists
    src = obs.obs_get_source_by_name(playing_scene)
    if src is None or obs.obs_source_get_type(src) != obs.OBS_SOURCE_TYPE_SCENE:
        obs.obs_source_release(src)
        raise FileNotFoundError(f" Could not find scene '{playing_scene}'")
    obs.obs_source_release(src)
    obs.script_log(obs.LOG_INFO, f"Scene '{playing_scene}' found!")

    # check if gameplay exit scene exists
    src = obs.obs_get_source_by_name(idle_scene)
    if src is None or obs.obs_source_get_type(src) != obs.OBS_SOURCE_TYPE_SCENE:
        obs.obs_source_release(src)
        raise FileNotFoundError(f" Could not find scene '{idle_scene}'")
    obs.obs_source_release(src)
    obs.script_log(obs.LOG_INFO, f"Scene '{idle_scene}' found!")

    obs.script_log(obs.LOG_INFO, 'Script is now active.')
    obs.timer_add(check_status_and_toggle, 500)
    
def script_update(settings):
    global status_file
    global idle_scene
    global playing_scene
    global initial_load
    if not initial_load:
        return

    status_file = obs.obs_data_get_string(settings, 'status_file')
    idle_scene = obs.obs_data_get_string(settings, 'idle_scene')
    playing_scene = obs.obs_data_get_string(settings, 'playing_scene')

    validate_and_start()

"""
Checks the osu! status file for 'Playing',
then toggles Noise Suppression accordingly
"""
previous_status = ''
def check_status_and_toggle():
    global status_file
    global idle_scene
    global playing_scene
    global previous_status
    
    # read status file contents
    if not os.path.isfile(status_file):
        obs.timer_remove(check_status_and_toggle)
        raise FileNotFoundError("Could not find file '{status_file}'")
    with open(status_file, 'r') as f:
        status = f.readlines()
    if status == []:
        return
    status = status[0].strip()
    if status == previous_status: # status has not changed
        return

    # Switch scene according to game status
    if status == 'Playing':
        src = obs.obs_get_source_by_name(playing_scene)
    else:
        src = obs.obs_get_source_by_name(idle_scene)
    obs.obs_frontend_set_current_scene(src)
    obs.obs_source_release(src)

    previous_status = status

