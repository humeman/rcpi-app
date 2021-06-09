import websocket
import json
import threading

from kivy.clock import Clock

from utils import kivyutils
from utils import motor


colors = {
    "unselect": (87/255, 104/255, 93/255, 1),
    "highlight": (20/255, 183/255, 28/255, 1) 
}

status = {
    "connected": False,
    "socket": None,
    "retain_log": False,
    "message_cache": []
}

def init(app_, sm_, videostream_, notconnected_, socketconnected_, socketdisconnected_):
    global app
    app = app_
    global sm
    sm = sm_
    global VideoStream
    VideoStream = videostream_
    global NotConnected
    NotConnected = notconnected_
    global SocketConnected
    SocketConnected = socketconnected_
    global SocketDisconnected
    SocketDisconnected = socketdisconnected_

def db_init(db_):
    global db
    db = db_

def disconnect():
    try:
        send(
            {
                "command": "stop"
            }
        )

        status["socket"].close()

    except:
        pass

    VideoStream.ids["viewer"].stop()

    status["connected"] = False
    status["socket"] = None
    status["message_cache"] = []
    status["retain_log"] = False

    update_widgets()

def wrap(function, args):
    try:
        function(*args)

    except:
        traceback.print_exc()

def create(ip):
    #websocket.enableTrace(True)

    status["socket"] = websocket.WebSocketApp(
        ip,
        on_message = on_message,
        on_error = on_error,
        on_open = on_open,
        on_close = on_close
    )

    status["socket"].run_forever()
    #print("Running forever")

def connect():
    status["connected"] = True

    ip = compile_ip()

    status["message_cache"].append(f"[ SOCK ] Connecting to {ip}...")
    update_messages()
    try:
        #print("Creating")
        thread = threading.Thread(target = create, args = [ip], daemon = True)
        thread.start()

        status["thread"] = thread
        #print("Created")

        #with concurrent.futures.ThreadPoolExecutor() as executor:
        #    executor.submit(create)
            #status["thread"] = executor.submit(status["socket"].run_forever, ())


            #status["thread"] = threading.Thread(target = status["socket"].run_forever, args = (), daemon = True)
            #status["thread"].start()

    except:
        kivyutils.error("Connect to websocket")

    VideoStream.ids["viewer"].url = compile_mjpg()
    VideoStream.ids["viewer"].start()

    update_widgets()

def compile_ip():
    return f"ws{'s' if db['wss'] else ''}://{db['ip']}:{db['ws_port']}"

def compile_mjpg():
    return f"http://{db['ip']}:{db['mjpg_port']}/stream.mjpg"

def update_widgets():
    screens = sm.ids

    if status["connected"]:
        # Drive screen
        d = screens["drive_screen"].ids

        for name in ["left", "right", "up", "down"]:
            d[name].background_color = colors["highlight"]

        # Video
        d["video_container"].clear_widgets()
        d["video_container"].add_widget(VideoStream)

        # TODO: Actually init the video stream
        
        # Socket screen
        s = screens["socket_screen"].ids

        s["container"].clear_widgets()
        s["container"].add_widget(SocketConnected)

        # TODO: Actually update socket text

        # Control screen
        c = screens["control_screen"].ids

        c["shutdown_button"].background_color = colors["highlight"]
        c["reboot_button"].background_color = colors["highlight"]

    else:
        # Drive screen
        d = screens["drive_screen"].ids

        for name in ["left", "right", "up", "down"]:
            d[name].background_color = colors["unselect"]

        # Video
        d["video_container"].clear_widgets()
        d["video_container"].add_widget(NotConnected)
        
        # Socket screen
        if not status["retain_log"]:
            s = screens["socket_screen"].ids

            s["container"].clear_widgets()
            s["container"].add_widget(SocketDisconnected)

        # Control screen
        c = screens["control_screen"].ids

        c["shutdown_button"].background_color = colors["unselect"]
        c["reboot_button"].background_color = colors["unselect"]

def update_messages():
    if len(status["message_cache"]) > 50:
        status["message_cache"] = status["message_cache"][-50:]

    s = sm.ids["socket_screen"].ids

    SocketConnected.ids["socket_display"].text = "\n".join(status["message_cache"])

def on_message(ws, message):
    status["message_cache"].append(f"[ RECV ] {message}")

    update_messages()

def on_error(ws, message):
    status["connected"] = False
    status["retain_log"] = True
    status["message_cache"].append(f"[ ERR  ] {message}")

    update_messages()
    update_widgets()

def on_close(ws):
    status["message_cache"].append(f"[ DISC ] Disconnected from websocket.")

    update_messages()

    status["connected"] = False
    status["retain_log"] = True

    update_widgets()

    Clock.schedule_once(add_result(), 1)

def add_result():
    status["message_cache"].append(f"[ DISC ] Thread exited: {status['thread'].result()}")
    update_messages()
    status["thread"] = None

def on_open(ws):
    status["message_cache"].append(f"[ SOCK ] Connected!")
    update_messages()
    update_widgets()

def get_auth():
    if db["auth"]:
        return {"key": db["auth"]}

    return {}

def send(message: dict):
    msg = json.dumps({**message, **get_auth()})

    status["message_cache"].append(f"[ SEND ] {msg}")

    status["socket"].send(msg)

def drive():
    if not status["connected"]:
        return

    send(
        {
            "command": "set",
            "motors": motor.change_direction(),
            "autostart": True
        }
    )

def control(state):
    if not status["connected"]:
        return

    send(
        {
            "command": state
        }
    )

    status["connected"] = False
    status["message_cache"] = []
    update_widgets()