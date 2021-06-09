#!/usr/bin/kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics.svg import Svg
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.clock import Clock

from utils import fonts
from utils import kivyutils
from utils import motor 
from utils import settings 
from utils import websocket

from utils.streamer import MjpegViewer



class AScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(AScreenManager, self).__init__(**kwargs)

class ControlScreen(Screen):
    def __init__(self, **kwargs):
        super(ControlScreen, self).__init__(**kwargs)

class DriveScreen(Screen):
    def __init__(self, **kwargs):
        super(DriveScreen, self).__init__(**kwargs)

class SocketScreen(Screen):
    def __init__(self, **kwargs):
        super(SocketScreen, self).__init__(**kwargs)

class DebugScreen(Screen):
    def __init__(self, **kwargs):
        super(DebugScreen, self).__init__(**kwargs)

class InfoScreen(Screen):
    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)

class ErrorScreen(Screen):
    def __init__(self, **kwargs):
        super(ErrorScreen, self).__init__(**kwargs)

# Widgets
class Spacer(Label):
    pass

class IconButton(Button):
    def __init__(self, **kwargs):
        super(IconButton, self).__init__(**kwargs)

class Separator(Widget):
    pass

class NavbarButton(Button):
    def __init__(self, **kwargs):
        super(NavbarButton, self).__init__(**kwargs)

class MovementButton(NavbarButton):
    def __init__(self, **kwargs):
        super(MovementButton, self).__init__(**kwargs)

class NavBar(GridLayout):
    def __init__(self, **kwargs):
        super(NavBar, self).__init__(**kwargs)

class VideoStream(GridLayout):
    def __init__(self, **kwargs):
        super(VideoStream, self).__init__(**kwargs)

class NotConnected(GridLayout):
    def __init__(self, **kwargs):
        super(NotConnected, self).__init__(**kwargs)

class SocketConnected(GridLayout):
    def __init__(self, **kwargs):
        super(SocketConnected, self).__init__(**kwargs)

class SocketDisconnected(GridLayout):
    def __init__(self, **kwargs):
        super(SocketDisconnected, self).__init__(**kwargs)

# Handlers
class SafeExceptionHandler(ExceptionHandler):
    def handle_exception(self, inst):
        kivyutils.error("Uncaught exception in clock")

ExceptionManager.add_handler(SafeExceptionHandler())

fonts.register()
kv = Builder.load_file("main.kv")

sm = AScreenManager()


def init(*args):
    settings.load()
    settings.update_all()
    websocket.update_widgets()

class RCApp(App):
    def build(self):
        Clock.schedule_once(init, 0)
        Window.clearcolor = (29/255, 33/255, 31/255, 1)
        return sm


app = RCApp()

kivyutils.init(app, sm)
motor.init(app, sm)
settings.init(app, sm)
websocket.init(app, sm, VideoStream(), NotConnected(), SocketConnected(), SocketDisconnected())

app.run()