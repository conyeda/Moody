from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader

from recommender import Recommender
from ImageAnalyser.ImageMood import ImageMood
from UI.Components.LoadDialog.LoadDialog import LoadDialog

from threading import Thread
import os

class RecommenderScreen(Screen):
    load_file = ObjectProperty(None)
    image_path_label = ObjectProperty(None)
    recommended_song_label = ObjectProperty(None)
    image_view = ObjectProperty(None)

    _SONGS_DIRECTORY = "ModelLibrary/xy_instances"
    _recommended_song = None
    _file_chooser_path = os.getcwd()
    _song = None
    _song_pos = 0

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

    def recommend(self):
        if (self.image_path_label.text != ""):
            self.recommended_song_label.text = "analysing..."
            if (self._song is not None):
                self._song.unload()
                self._song = None
            Thread(target=self.recommend_async).start()

    def recommend_async(self):
        rec = Recommender(self.image_path_label.text)
        self._recommended_song = rec.recommend()
        self.recommended_song_label.text = "Your song is: {}.".format(self._recommended_song)

    def play_song(self):
        if (self._song is None and self._recommended_song is not None):
            self._song = SoundLoader.load(os.path.join(self._SONGS_DIRECTORY, self._recommended_song))

        if (self._song is not None):
            self._song.play()
            self._song.seek(self._song_pos)

    def pause_song(self):
        if (self._song is not None and self._song.state == "play"):
            self._song_pos = self._song.get_pos()
            self._song.stop()

    def stop_song(self):
        if (self._song is not None):
            self._song_pos = 0
            self._song.stop()