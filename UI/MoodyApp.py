from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.window import Window

from UI.ImageAnalysisWindow import ImageAnalysisWindow
from UI.SongAnalysisWindow import SongAnalysisWindow
from UI.RecommenderWindow import RecommenderWindow

Window.clearcolor = (1, 1, 1, 1)

class MainWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("UI/main_screen.kv")

class MoodyApp(App):
    def build(self):
        return kv