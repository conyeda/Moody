import numpy as np
from os import listdir
from os.path import isfile, join

def np_transformation(np_array):
    return np_array.reshape(149,313,1)

def data_from_npy(path) -> np.ndarray:
    files = listdir(path)
    files.sort()
    data = [
            np.load(np_path)
            for np_path in map(
                lambda i: join(path, i), 
                files
                )
            if isfile(np_path)
            ]
    final_data = list(map(np_transformation, data))
    

    return np.array(final_data)

def test_data(data):
    EXPECTED_X = 149
    EXPECTED_Y = 313

    count = 0
    
    for song in data:
        count += 1
        if len(song) != EXPECTED_X:
            print(f'Error in song {count} in x -> {len(song)}')
        for line in song:
            if len(line) != EXPECTED_Y:
                print(f'Error in song {count} in y -> {len(line)}')

if __name__ == '__main__':
    import pathlib

    PATH = str(pathlib.Path(__file__).parent.resolve())
    FILE_PATH = '/'.join((PATH,'../spectrograms/'))
    
    data = data_from_npy(FILE_PATH)
    test_data(data)