from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from ImageMood import ImageMood
from UI.Components.LoadDialog.LoadDialog import LoadDialog

from recommender import Recommender

from threading import Thread
import os


class ImageAnalysisScreen(Screen):
    """Class asociated to the screen that analyze the images
    """
    load_file = ObjectProperty(None)
    image_path_label = ObjectProperty(None)
    image_analysis_result = ObjectProperty(None)
    image_view = ObjectProperty(None)
    _file_chooser_path = os.getcwd()

    def dismiss_popup(self):
        """use to cancel a process (for instance, is going to be used
            to cancel the "image window" in the UI)
        """
        self._popup.dismiss()

    def load(self, path, filename):
        """saves the selected image's path and shows the image

        Args:
            path (PathLike): path of the image 
            filename (String): name of the image
        """        
        
        self.image_path_label.text = os.path.join(path, filename[0])
        self._file_chooser_path = self.image_path_label.text
        self.image_view.source = self.image_path_label.text
        self._popup.dismiss()

    def show_load(self):
        """shows the window to choose the image
        """        
        content = LoadDialog(
            load=self.load, cancel=self.dismiss_popup, path=self._file_chooser_path)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def analyse(self):
        """function use when the "analyze botton" is clicked.
            executes in a different thread the image analyse using the function analyse_async
        """        
        if (self.image_path_label.text is not ""):
            self.image_analysis_result.text = "analysing..."
            Thread(target=self.analyse_async).start()

    def analyse_async(self):
        """this function calls to the recommender to analyze the image and shows in the screen the values 
            of valence and energy obtained after having done the analyse.
        """        
        rec = Recommender(self.image_path_label.text)
        valence, energy = rec.analyze()
        self.image_analysis_result.text = "Valence: {}. Energy: {}.".format(
            valence, energy)
