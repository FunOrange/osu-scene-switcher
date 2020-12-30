import os
import time
import obspython as obs

initial_load = False
status_file = ''
desktop_audio_source = ''
microphone_audio_source = ''
game_volume_playing = 0
mic_volume_playing = 0
game_volume_idle = 0
mic_volume_idle = 0

def undb(db):
    return pow(10, db/20)

def script_description():
    return 'Script that automatically adjusts certain settings upon entering osu! gameplay.\n\n' \
            'See github page for setup instructions.\n\n' \
            'Stream Companion must be open to take effect.'
    
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, 'status_file', 'osu! status file location', obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, 'desktop_audio_source', 'Main audio source (eg. Desktop Audio)', obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, 'microphone_audio_source', 'Microphone audio source (eg. Mic/Aux)', obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_float(props, 'game_volume_playing', 'Game volume - playing (dB)', -94.6, 0, 0.1)
    obs.obs_properties_add_float(props, 'mic_volume_playing', 'Mic volume - playing (dB)', -94.6, 0, 0.1)
    obs.obs_properties_add_float(props, 'game_volume_idle', 'Game volume - not playing (dB)', -94.6, 0, 0.1)
    obs.obs_properties_add_float(props, 'mic_volume_idle', 'Mic volume - not playing (dB)', -94.6, 0, 0.1)
    return props

def script_load(settings):
    global status_file
    global desktop_audio_source
    global microphone_audio_source
    global game_volume_playing
    global mic_volume_playing
    global game_volume_idle
    global mic_volume_idle
    status_file = obs.obs_data_get_string(settings, 'status_file')
    desktop_audio_source = obs.obs_data_get_string(settings, 'desktop_audio_source')
    microphone_audio_source = obs.obs_data_get_string(settings, 'microphone_audio_source')

    game_volume_playing = obs.obs_data_get_double(settings, 'game_volume_playing')
    mic_volume_playing = obs.obs_data_get_double(settings, 'mic_volume_playing')
    game_volume_idle = obs.obs_data_get_double(settings, 'game_volume_idle')
    mic_volume_idle = obs.obs_data_get_double(settings, 'mic_volume_idle')

    # Delay check valid source until OBS is fully loaded
    obs.script_log(obs.LOG_INFO, 'Starting in 10 seconds...')
    obs.timer_add(validate_and_start, 10000)

def script_update(settings):
    global status_file
    global desktop_audio_source
    global microphone_audio_source
    global initial_load
    global game_volume_playing
    global mic_volume_playing
    global game_volume_idle
    global mic_volume_idle
    if not initial_load:
        return

    status_file = obs.obs_data_get_string(settings, 'status_file')
    desktop_audio_source = obs.obs_data_get_string(settings, 'desktop_audio_source')
    microphone_audio_source = obs.obs_data_get_string(settings, 'microphone_audio_source')

    game_volume_playing = obs.obs_data_get_double(settings, 'game_volume_playing')
    mic_volume_playing = obs.obs_data_get_double(settings, 'mic_volume_pla')
    game_volume_idle = obs.obs_data_get_double(settings, 'game_volume_idle')
    mic_volume_idle = obs.obs_data_get_double(settings, 'mic_volume_idle')

    validate_and_start()

"""
Checks if status file exists, source exists, and Noise Suppression filter exists,
then starts the main script timer
"""
def validate_and_start():
    global initial_load
    global desktop_audio_source
    global microphone_audio_source
    initial_load = True
    obs.timer_remove(validate_and_start)
    obs.timer_remove(check_status_and_toggle)

    # check if file exists
    if not os.path.isfile(status_file):
        raise FileNotFoundError("Could not find file pointed to by 'osu! status file location'")
    obs.script_log(obs.LOG_INFO, f'{status_file} found!')

    # check if desktop audio source exists
    desktop_audio = obs.obs_get_source_by_name(desktop_audio_source)
    if desktop_audio == None:
        raise Exception(f"No source named '{desktop_audio_source}' was found.")
    obs.obs_source_release(desktop_audio)
    obs.script_log(obs.LOG_INFO, f'{desktop_audio_source} found!')

    # check if microphone audio source exists
    mic_audio = obs.obs_get_source_by_name(microphone_audio_source)
    if mic_audio == None:
        raise Exception(f"No source named '{microphone_audio_source}' was found.")
    obs.obs_source_release(mic_audio)
    obs.script_log(obs.LOG_INFO, f'{microphone_audio_source} found!')

    obs.script_log(obs.LOG_INFO, 'Script is now active.')
    obs.timer_add(check_status_and_toggle, 1000)
    
"""
Checks the osu! status file for 'Playing',
then toggles Noise Suppression accordingly
"""
previous_status = ''
def check_status_and_toggle():
    global status_file
    global desktop_audio_source
    global microphone_audio_source
    global game_volume_playing
    global mic_volume_playing
    global game_volume_idle
    global mic_volume_idle
    global previous_status
    
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
    if status == previous_status: # status has not changed
        return

    # adjust volume according to status
    desktop_audio = obs.obs_get_source_by_name(desktop_audio_source)
    mic_audio = obs.obs_get_source_by_name(microphone_audio_source)
    if status == 'Playing':
        obs.obs_source_set_volume(desktop_audio, undb(game_volume_playing))
        obs.obs_source_set_volume(mic_audio, undb(mic_volume_playing))
        print(f'adjusting volume: {game_volume_playing} dB ({desktop_audio_source}), {mic_volume_playing} dB ({microphone_audio_source})')
    else:
        obs.obs_source_set_volume(desktop_audio, undb(game_volume_idle))
        obs.obs_source_set_volume(mic_audio, undb(mic_volume_idle))
        print(f'adjusting volume: {game_volume_idle} dB ({desktop_audio_source}), {mic_volume_idle} dB ({microphone_audio_source})')
    obs.obs_source_release(desktop_audio)
    obs.obs_source_release(mic_audio)

    previous_status = status

    # target_source = obs.obs_get_source_by_name(desktop_audio_source)
    # noise_suppression = obs.obs_source_get_filter_by_name(target_source, 'Noise Suppression')
    # if obs.obs_source_enabled(noise_suppression) != is_playing:
    #     obs.obs_source_set_enabled(noise_suppression, is_playing)
    #     if is_playing:
    #         obs.script_log(obs.LOG_INFO, f'Noise suppression enabled')
    #     else:
    #         obs.script_log(obs.LOG_INFO, f'Noise suppression disabled')
    # obs.obs_source_release(target_source)
