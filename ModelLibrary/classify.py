from keras.models import load_model

class Classifier:
# Class that use model tu classify audios in folders
    def __init__(self, model_path='trained_MER.h5', audio_path='data/spectrograms/') -> None:
        self._model = load_model(model_path)
        self._audio_path=audio_path
    
    def test_folders() -> None:
    # Test if the expected folders had been created
    # If not -> Create them
    # If yes -> Nothing is done
        pass 

    def audio_processing() -> None:
    # Process the audios into npy
        pass

    def clean_npy() -> None:
    # Delete npy audios
        pass

    def classify(self) -> None:
    # Do all the process of classifying
    # 1. Use test_folders()
    # 2. Use audio_processing()
    # 3. Use the model to predict the results
    # 4. Classify the results
    # 5. Use clean_npy() 
        
        predictions = self._model.predict()
    
    @staticmethod
    def classify(model, audio_path) -> None:
        print('hola')
        pass


# What needs the Classifier?
# - Import Model
# - Audio processing
# - Delete audio processed data
# - Move audio into folders
if __name__ == '__main__':
    Classifier.classify(2,3)