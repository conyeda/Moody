import numpy as np
from os import listdir
from os.path import isfile, join


def np_transformation(np_array):
    """necessary transformation of the array

    Args:
        np_array (NumPyArray): array to be transformed 

    Returns:
       NumPyArray: transformed array
    """    
    return np_array.reshape(149, 313, 1)


def data_from_npy(path) -> np.ndarray:
    """take all the .npy files that are in the directory path and return a npy array with all of them

    Args:
        path (PathLike): path of the npy files

    Returns:
        np.ndarray: array with all the npy files
    """    
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
    """test the size of the spectograms are the requires wanted

    Args:
        data (npy array): array with a set of files 
    """    
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
    FILE_PATH = '/'.join((PATH, '../spectrograms/'))

    data = data_from_npy(FILE_PATH)
    test_data(data)
