from pcc import correlation
from npy_opening import data_from_npy
from keras.models import load_model
from audio_processing import audio_processing
import pathlib
import sys
import os


PATH = pathlib.Path(__file__).parent

class Classifier:
# Class that use model tu classify audios in folders
    def __init__(self, model_path='../trained_MER.h5') -> None:
        self._model = load_model(model_path, custom_objects={'correlation':correlation})
       
    
    def test_folders(self) -> None:
    # Test if the expected folders had been created
    # If not -> Create them
    # If yes -> Nothing is done
        path = PATH
        os.makedirs(''.join((str(path),'/xy_instances')), exist_ok=True)
            
    

    def audio_processing(self) -> None:
    # Process the audios into npy
        audio_processing()

    def clean(self) -> None:
    # Delete npy audios
    # Delete initial audios
        for spectfile in os.listdir(''.join(((str(PATH.parent.resolve())),'/spectograms/'))):
            os.remove(os.path.join(''.join(((str(PATH.parent.resolve())),'/spectograms/',spectfile))))

        for audiofile in os.listdir(''.join(((str(PATH.parent.resolve())),'/audios/'))):
            os.remove(os.path.join(''.join(((str(PATH.parent.resolve())),'/audios/', audiofile))))

    def classify(self) -> None:
    # Do all the process of classifying
    # 1. Use test_folders()
    # 2. Use audio_processing()
    # 3. Use the model to predict the results
    # 4. Classify the results
    # 5. Use clean() 
        file = open('contador.txt')
        cont = int(file.read())
        file.close()

        self.test_folders()
        audio_processing()
        files = os.listdir(''.join(((str(PATH.parent.resolve())),'/audios')))
        files.sort()
        predictions = self._model.predict(data_from_npy(''.join(((str(PATH.parent.resolve())),'/spectograms'))))
        lengthpred = len(predictions)
        for i in range(0,lengthpred):
            x,y = predictions[i][0:2]
            os.rename((''.join((str(PATH.parent.resolve()),'/audios/',str(files[i])))),(''.join((str(PATH.resolve()),'/xy_instances/',str(cont+i),"_",str(x),"_",str(y),"_", str(files[i])))))
        cont = cont + lengthpred

        file = open('contador.txt', 'w')
        file.write(str(cont))
        file.close()
        self.clean()


# What needs the Classifier?
# - Import Model
# - Audio processing
# - Delete audio processed data
# - Move audio into folders
if __name__ == '__main__':
    hola = Classifier()
    hola.classify()
