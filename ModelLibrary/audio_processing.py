import librosa
import numpy as np
import os
import matplotlib.pyplot as plt
import librosa.display
import pathlib


PATH = str(pathlib.Path(__file__).parent.parent.resolve())
SAVE_PATH = '/'.join((PATH, 'spectograms/'))
AUDIOS_FILE = '/'.join((PATH, 'audios/'))


class Loader:
    # loader is responsible for loading the audio file

    def __init__(self, sample_rate, duration, mono):
        """constructor of the class

        Args:
            sample_rate (Integer): the value we take as sample rate
            duration (Integer): duration of each audio
            mono (Boolean): if is true converts the audio to mono
        """        
        self.sample_rate = sample_rate
        self.duration = duration
        self.mono = mono

    def load(self, file_path):
        """load an audio file as a float in point time series, audio will be automatically resample to the given rate

        Args:
            file_path (PathLike): path of the audio

        Returns:
         AudioTimeSeries ,a npy.ndarray of floating point values 
        """        
        signal = librosa.load(file_path,        #
                              sr=self.sample_rate,
                              duration=self.duration,
                              mono=self.mono)[0]
        return signal


class Padder:
    """Padder is responsible to apply padding to an array
    """
    def __init__(self, mode="constant"):
        """constructor of the padder

        Args:
            mode (str, optional): To specify the array's size. Defaults to "constant".
        """        
        self.mode = mode

    def left_pad(self, array, num_missing_items):
        """missing element in the left with 0

        Args:
            array (Array): array to pad
            num_missing_items (Integer): number of elements that we have to
                                         pad with 0

        Returns:
           an array, the same array but padded
        """        
        padded_array = np.pad(array,
                              (num_missing_items, 0),
                              mode=self.mode)
        return padded_array

    def right_pad(self, array, num_missing_items):
        """pad missing element in the right with 0

        Args:
            array (array): array to pad 
            num_missing_items (integer): number of elements that we have to pad with 0

        Returns:
            an array, the same array but padded
        """        
        padded_array = np.pad(array,
                              (0, num_missing_items),
                              mode=self.mode)
        return padded_array


class LogSpectrogramExtractor:
    """class that  extracts log spectrogram (in dB) from a time series signal
    """

    def __init__(self, frame_size, hop_length):
        """constructor of the class

        Args:
            frame_size (integer): size of the frame 
            hop_length (integer): lenght of the hop
        """        
        self.frame_rate = frame_size
        self.hop_length = hop_length

    def extract(self, signal):
        """extracts log spectogram (in dB) from a time series signal

        Args:
            signal (AudioSerieSignal npy.ndArray): audio signal represented as a one dimentional npy.ndarray of floating point values

        Returns:
           a  matrix, the values of the matrix will be floats representing the db
        """        
        stft = librosa.stft(signal,
                            n_fft=self.frame_rate,
                            hop_length=self.hop_length,
                            win_length=149)[:-1]
        spectrogram = np.abs(stft)
        log_spectrogram = librosa.amplitude_to_db(spectrogram)

        return log_spectrogram


class Saver:
    """Saver is responsible to save features, and the min max values
    """
    def __init__(self, feature_save_dir):
        """construction  of the class Saver

        Args:
            feature_save_dir (PathLike): path where spectograms are saved
        """
        self.feature_save_dir = feature_save_dir

    def save_feature(self, feature, file_path):
        """function that save features

        Args:
            feature (array): array to be saved
            file_path (PathLike): path where is the file

        Returns:
            a path where the file is saved
        """        
        save_path = self._generate_save_path(file_path)
        with open(save_path, 'wb') as f:
            np.save(f, feature, allow_pickle=True)
        return save_path

    def _generate_save_path(self, file_path):
        """function that generates the save path with the extension npy

        Args:
            file_path (PathLike): path of the corresponding file

        Returns:
            a path where the file is saved
        """
        file_name = os.path.split(file_path)[1]
        save_path = os.path.join(self.feature_save_dir, file_name + ".npy")
        return save_path


class PreprocessingPipeline:
    """
    PreprocessingPipeline processes audio files in a directory,
    applying the following to each file
        1 - load a file
        2 - pad the signal (if necessary)
        3 - extracting log spectrogram from signal
        4 - normalise spectrogram
        5 - save the normalised signal
    storing all the min max values for all the log spectrogram
    """

    def __init__(self):
        """construction  of the class PreprocessingPipeline

        """
        self.padder = None
        self.extractor = None
        self.normaliser = None
        self.saver = None
        self.min_max_values = {}
        self._loader = None
        self._num_expected_samples = None
        self.save_path = None

    @property
    def loader(self):
        """function that act as the getter of loader

        """
        return self._loader

    @loader.setter
    def loader(self, loader):
        """function that act as the setter of loader 

        Args:
            loader (Loader): class responsible for loading the audio file
        """
        # Setter
        self._loader = loader
        self._num_expected_samples = int(
            self.loader.sample_rate * self.loader.duration)

    def process(self, audio_files_directory):
        """function that process the audios of the given directory path

        Args:
            audio_files_directory (Pathlike): path of the audios
        """
        for root, _, files in os.walk(audio_files_directory):
            for file in files:
                file_path = os.path.join(root, file)
                self._process_file(file_path)
                print(f"Processed file {file_path}")

    def _process_file(self, file_path):
        """function that converts the audio file into a audio time series call signal

        Args:
            file_path (Pathlike): path of the file
        """
        signal = self.loader.load(file_path)
        if self._is_padding_necessary(signal):
            signal = self._apply_padding(signal)
        feature = self.extractor.extract(signal)
        self.save_path = self.saver.save_feature(feature, file_path)

    def _is_padding_necessary(self, signal):
        """function that check if it is necessary to pad the signal

        Args:
            signal (AudioSerieSignal npy.ndArray): a npy.ndarray of floating point values 

        Returns:
            a boolean that indicates if it is necessary to pad
        """
        if len(signal) < self._num_expected_samples:
            return True
        return False

    def _apply_padding(self, signal):
        """function that pad the array if  the length of the signal is less than the expected examples

        Args:
            signal (AudioSerieSignal npy.ndArray): a npy.ndarray of floating point values 

        Returns:
            the signal(array) padded
        """
        num_missing_samples = self._num_expected_samples - len(signal)
        padded_signal = self.padder.right_pad(signal, num_missing_samples)
        return padded_signal


def audio_processing(spectogram_save_dir=SAVE_PATH, audios_file=AUDIOS_FILE):
    """function that process the audios of the given path and convert them into  spectograms with extension .npy
       and save them in the path given

        Args:
            spectogram_save_dir (Pathlike): path where the spectograms will be stored
            audios_file (Pathlike) : path where the audios are

        
        """
    FRAME_SIZE = 299
    HOP_LENGTH = 705
    DURATION = 10  # In seconds
    SAMPLE_RATE = 22050
    MONO = True

    loader = Loader(SAMPLE_RATE, DURATION, MONO)
    padder = Padder()
    log_spectrogram_extractor = LogSpectrogramExtractor(FRAME_SIZE, HOP_LENGTH)
    saver = Saver(spectogram_save_dir)

    preprocessing_pipeline = PreprocessingPipeline()
    preprocessing_pipeline.loader = loader
    preprocessing_pipeline.padder = padder
    preprocessing_pipeline.extractor = log_spectrogram_extractor
    preprocessing_pipeline.saver = saver

    preprocessing_pipeline.process(audios_file)


if __name__ == "__main__":
    FRAME_SIZE = 299
    HOP_LENGTH = 705
    DURATION = 10
    SAMPLE_RATE = 22050
    MONO = True

    SPECTROGRAM_SAVE_DIR = "C:/Users/antho/Downloads/audio/spectograms2"
    FILES_DIR = "C:/Users/antho/Downloads/audio/audio"

    loader = Loader(SAMPLE_RATE, DURATION, MONO)
    padder = Padder()
    log_spectrogram_extractor = LogSpectrogramExtractor(FRAME_SIZE, HOP_LENGTH)
    saver = Saver(SPECTROGRAM_SAVE_DIR)

    preprocessing_pipeline = PreprocessingPipeline()
    preprocessing_pipeline.loader = loader
    preprocessing_pipeline.padder = padder
    preprocessing_pipeline.extractor = log_spectrogram_extractor
    preprocessing_pipeline.saver = saver

    preprocessing_pipeline.process(FILES_DIR)
