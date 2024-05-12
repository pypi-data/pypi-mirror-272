import requests
import awtrix.effects as ef

AWTRIX_BASE_URL = "http://192.168.11.160"

def setup_AWTRIX():
    disable_built_in_apps('HUM')
    disable_built_in_apps('BAT')
    disable_built_in_apps('TEMP')
    set_transition_effect(ef.transistion_effects.random, time_ms=2000)
    reboot()

def set_transition_effect(ef:ef.transistion_effects, time_ms: int = 500 ) -> None:
    url = AWTRIX_BASE_URL + '/api/settings'
    myobj = {
        'TEFF': ef.value,
        'TSPEED': time_ms
    }
    requests.post(url=url, json=myobj)

def disable_built_in_apps(app_name: str):
    url = AWTRIX_BASE_URL + '/api/settings'
    myobj = {app_name:False}
    requests.post(url=url, json=myobj)

def enable_built_in_apps(app_name: str):
    url = AWTRIX_BASE_URL + '/api/settings'
    myobj = {app_name:True}
    requests.post(url=url, json=myobj)

def reboot():
    requests.post(url=AWTRIX_BASE_URL+'/api/reboot')
