from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, SlideTransition
from kivy.core.window import Window

import traceback

screens = {
    "drive_button": "drive_screen",
    "control_button": "control_screen",
    "socket_button": "socket_screen",
    "debug_button": "debug_screen",
    "info_button": "info_screen"
}

def init(app_, sm_):
    global app
    app = app_
    global sm
    sm = sm_

def get_id(instance):
    for id_, widget in instance.parent.ids.items():
        if widget.__self__ == instance:
            return id_

def get_id_from(instance, parent):
    for id_, widget in parent.ids.items():
        if widget.__self__ == instance:
            return id_

def switch_screen(instance):
    id_ = get_id_from(instance, instance.parent.parent)
    old_id = [x for x, y in screens.items() if y == sm.current][0]
    if id_ == old_id:
        return

    # Determine direction
    new_index = list(instance.parent.parent.ids).index(id_)
    old_index = list(screens).index(old_id)
    
    sm.transition = SlideTransition()
    if new_index > old_index:
        sm.transition.direction = "left"

    else:
        sm.transition.direction = "right"

    selected = str(id_)
    sm.current = str(screens[id_])

    instance = sm.ids[sm.current].ids["navbar"].ids[id_]

    for widget in instance.parent.children:
        if widget.__self__ == instance:
            continue

        widget.color = (87/255, 104/255, 93/255, 1)

    instance.color = (20/255, 183/255, 28/255, 1)

def test_error(instance = None):
    try:
        9 + "10" == 21

    except:
        error("Test exception")

def error(reason):
    ids = sm.ids["error_screen"].ids

    reason_widget = ids["reason"]
    exception_widget = ids["exception"]

    reason_widget.text = reason
    exception_widget.text = traceback.format_exc()

    Window.clearcolor = (32/255, 26/255, 26/255, 1)
    sm.transition = NoTransition()
    sm.current = "error_screen"