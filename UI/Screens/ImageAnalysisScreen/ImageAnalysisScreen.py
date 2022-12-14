from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from ImageMood import ImageMood
from UI.Components.LoadDialog.LoadDialog import LoadDialog

from recommender import Recommender

from threading import Thread
import os

class ImageAnalysisScreen(Screen):
    load_file = ObjectProperty(None)
    image_path_label = ObjectProperty(None)
    image_analysis_result = ObjectProperty(None)
    image_view = ObjectProperty(None)
    _file_chooser_path = os.getcwd()

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
        if (self.image_path_label.text is not ""):
            self.image_analysis_result.text = "analysing..."
            Thread(target=self.analyse_async).start()

    def analyse_async(self):
        rec = Recommender(self.image_path_label.text)
        valence,energy = rec.analyze()
        self.image_analysis_result.text = "Valence: {}. Energy: {}.".format(valence, energy)