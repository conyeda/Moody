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
    """Code associated to the screen that recommends songs, first of all loads the attributes
    and songs from their directory.
    """
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
        """Use to cancel a process (for instance, is going to be used
            to cancel the "image window" in the UI)
        """        
        self._popup.dismiss()

    def load(self, path, filename):
        """Saves the selected image's path and shows the image

        Args:
            path (PathLike): path of the image 
            filename (String): name of the image
        """     
        self.image_path_label.text = os.path.join(path, filename[0])
        self._file_chooser_path = self.image_path_label.text
        self.image_view.source = self.image_path_label.text
        self._popup.dismiss()

    def show_load(self):
        """Shows the window to choose the image
        """    
        content = LoadDialog(
            load=self.load, cancel=self.dismiss_popup, path=self._file_chooser_path)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def recommend(self):
        """Calls to the function recommend_async that is run in a new thread
        """
        if (self.image_path_label.text != ""):
            self.recommended_song_label.text = "analysing..."
            if (self._song is not None):
                self._song.unload()
                self._song = None
            Thread(target=self.recommend_async).start()

    def recommend_async(self):
        """function that recommends a song and shows in the screen the name of the song
        """
        rec = Recommender(self.image_path_label.text)
        self._recommended_song = rec.recommend()
        self.recommended_song_label.text = "Your song is: {}.".format(
            self._recommended_song)

    def play_song(self):
        """Code associated to the botton to play the song use to reproduce the recommended song
        """
        if (self._song is None and self._recommended_song is not None):
            self._song = SoundLoader.load(os.path.join(
                self._SONGS_DIRECTORY, self._recommended_song))

        if (self._song is not None):
            self._song.play()
            self._song.seek(self._song_pos)

    def pause_song(self):
        """Code associated to the botton to pause the song, use to pause the song
        """
        if (self._song is not None and self._song.state == "play"):
            self._song_pos = self._song.get_pos()
            self._song.stop()

    def stop_song(self):
        """Code associated to the botten that stops the song, when this botton is clicked 
            the song is pause and also restart.
        """
        if (self._song is not None):
            self._song_pos = 0
            self._song.stop()
