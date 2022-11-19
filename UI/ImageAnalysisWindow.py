from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from ImageAnalyser.ImageMood import ImageMood
from UI.LoadDialog import LoadDialog

from threading import Thread
import os

class ImageAnalysisWindow(Screen):
    load_file = ObjectProperty(None)
    image_path_label = ObjectProperty(None)
    mood_label = ObjectProperty(None)
    image_view = ObjectProperty(None)
    _file_chooser_path = ""

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path, filename):
        self.image_path_label.text = os.path.join(path, filename[0])
        self._file_chooser_path = self.image_path_label.text
        self.image_view.source = self.image_path_label.text
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup, path=self._file_chooser_path)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def analyse(self):
        if (self.image_path_label.text is not None):
            self.mood_label.text = "analysing..."
            Thread(target=self.analyse_async).start()

    def analyse_async(self):
        image_mood = ImageMood(self.image_path_label.text)
        image_mood.analyse()
        self.mood_label.text = image_mood.mood