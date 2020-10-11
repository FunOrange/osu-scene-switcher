import os
import time
import obspython as obs

initial_load = False
status_file = ''
target_source_name = ''

def script_description():
    return 'Toggle Noise Suppression while playing osu!\n\n' \
            'Noise suppression is enabled during gameplay and disabled during song select, score screen, etc.\n\n' \
            'Stream Companion must be open to take effect.'
    
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, 'status_file', 'osu! status file location', obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, 'target_source_name', 'Target audio source (eg. Mic/Aux)', obs.OBS_TEXT_DEFAULT)
    return props

def script_load(settings):
    global status_file
    global target_source_name
    status_file = obs.obs_data_get_string(settings, 'status_file')
    target_source_name = obs.obs_data_get_string(settings, 'target_source_name')

    # Delay check valid source until OBS is fully loaded
    obs.script_log(obs.LOG_INFO, 'Starting in 10 seconds...')
    obs.timer_add(validate_and_start, 10000)

def script_update(settings):
    global status_file
    global target_source_name
    global initial_load
    if not initial_load:
        return

    status_file = obs.obs_data_get_string(settings, 'status_file')
    target_source_name = obs.obs_data_get_string(settings, 'target_source_name')

    validate_and_start()

"""
Checks if status file exists, source exists, and Noise Suppression filter exists,
then starts the main script timer
"""
def validate_and_start():
    global initial_load
    initial_load = True
    obs.timer_remove(validate_and_start)
    obs.timer_remove(check_status_and_toggle)

    # check if file exists
    if not os.path.isfile(status_file):
        raise FileNotFoundError("Could not find file pointed to by 'osu! status file location'")


    target_source = obs.obs_get_source_by_name(target_source_name)
    if target_source == None:
        raise Exception(f"No source '{target_source_name}' named was found.")
    if obs.obs_source_get_filter_by_name(target_source, 'Noise Suppression') == None:
        raise Exception(f"Source '{target_source_name}' does not have a Noise Suppression filter.")

    obs.script_log(obs.LOG_INFO, 'osu! status file found!')
    obs.script_log(obs.LOG_INFO, 'Target audio source found!')
    obs.script_log(obs.LOG_INFO, 'Script is active.')
    obs.timer_add(check_status_and_toggle, 1000)
    
"""
Checks the osu! status file for 'Playing',
then toggles Noise Suppression accordingly
"""
def check_status_and_toggle():
    global status_file
    # read status file contents
    if not os.path.isfile(status_file):
        obs.timer_remove(check_status_and_toggle)
        raise FileNotFoundError("Could not find file pointed to by 'osu! status file location'")
    f = open(status_file, 'r')
    status = f.readlines()
    f.close()
    if status == []:
        return
    status = status[0].strip()

    # toggle noise suppression depending on status
    enable_noise_suppression = (status == 'Playing')

    target_source = obs.obs_get_source_by_name(target_source_name)
    noise_suppression = obs.obs_source_get_filter_by_name(target_source, 'Noise Suppression')
    if obs.obs_source_enabled(noise_suppression) != enable_noise_suppression:
        obs.obs_source_set_enabled(noise_suppression, enable_noise_suppression)
        if enable_noise_suppression:
            obs.script_log(obs.LOG_INFO, f'Noise suppression enabled')
        else:
            obs.script_log(obs.LOG_INFO, f'Noise suppression disabled')
    obs.obs_source_release(target_source)
