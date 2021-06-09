import json
import os
import copy

from utils import kivyutils
from utils import websocket
from utils import motor

default_db = {
    "speed": 50,
    "turn_speed": 25,
    "ip": "Not set",
    "ws_port": 5000,
    "mjpg_port": 8000,
    "wss": False,
    "auth": None
}

def init(app_, sm_):
    global app
    app = app_
    global sm
    sm = sm_

def load():
    if not os.path.exists("settings.json"):
        with open("settings.json", "w+") as f:
            f.write(json.dumps(default_db, indent = 4))

    try:
        with open("settings.json", "r") as f:
            global db
            db = json.loads(f.read())

    except:
        kivyutils.error("Settings initialization")
        return

    for key, value in default_db.items():
        if key not in db:
            db[key] = copy.copy(value)

    websocket.db_init(db)
    motor.db_init(db)

def write():
    try:
        with open("settings.json", "w") as f:
            f.write(json.dumps(db, indent = 4))

    except:
        kivyutils.error("Settings dump")
        return

def update_all():
    screens = sm.ids
    ctrl = screens["control_screen"].ids

    # Set speed
    ctrl["speed_label"].text = str(db["speed"])
    ctrl["speed_slider"].value = db["speed"]

    # Set turn speed
    ctrl["turn_speed_label"].text = str(db["turn_speed"])
    ctrl["turn_speed_slider"].value = db["turn_speed"]

    # Set DB
    screens["debug_screen"].ids["db_editor"].text = json.dumps(db, indent = 4)

    # Set IP
    ctrl["ip_input"].text = db["ip"]
    ctrl["ws_port_input"].text = str(db["ws_port"])
    ctrl["mjpg_port_input"].text = str(db["mjpg_port"])
    ctrl["security_toggle"].text = [x for x, y in security_toggle.items() if y == db["wss"]][0]

    ctrl["auth_input"].text = db["auth"] if db["auth"] else ""
    
def update_speed():
    screens = sm.ids
    ctrl = screens["control_screen"].ids

    s = int(ctrl["speed_slider"].value)
    ts = int(ctrl["turn_speed_slider"].value)

    if s == db["speed"] and ts == db["turn_speed"]:
        return

    db["speed"] = s
    db["turn_speed"] = ts

    write()

    update_all()

def update_ip():
    screens = sm.ids
    ctrl = screens["control_screen"].ids

    db["ip"] = ctrl["ip_input"].text
    try:
        db["ws_port"] = int(ctrl["ws_port_input"].text)

    except:
        db["ws_port"] = default_db["ws_port"]

    try:
        db["mjpg_port"] = int(ctrl["mjpg_port_input"].text)

    except:
        db["mjpg_port"] = default_db["mjpg_port"]

    db["wss"] = security_toggle[ctrl["security_toggle"].text]

    write()

    update_all()

def update_auth():
    screens = sm.ids
    ctrl = screens["control_screen"].ids

    db["auth"] = ctrl["auth_input"].text if ctrl["auth_input"].text.strip() != "" else None

    write()

    update_all()


def code_exec(instance):
    screens = sm.ids
    ctrl = screens["debug_screen"].ids

    try:
        exec(ctrl["code_executor"].text, globals())

    except:
        kivyutils.error("Debug code execution")

def update_db_manual():
    screens = sm.ids
    ctrl = screens["debug_screen"].ids

    try:
        new_db = json.loads(ctrl["db_editor"].text)

    except:
        kivyutils.error("DB override")
        return

    # What
    for name, value in new_db.items():
        db[name] = value

    write()

    update_all()
    

security_toggle = {
    "\uf023": True,
    "\uf3c1": False 
}


def toggle_secure(instance):
    instance.text = [x for x in security_toggle if x != instance.text][0]

    print("m")