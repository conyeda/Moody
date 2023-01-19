import numpy as np


def csv_to_np(path, skip_header) -> np.ndarray:
    """Read a csv file and return a numpy array.

    Args:
        path (PathLike): Path to the csv file
        skip_header (_type_): skip the first n lines of the csv file being n the number of the argument

    Returns:
        np.ndarray: numpy array with the data from the csv file
    """
    return np.genfromtxt(path, delimiter=';', skip_header=skip_header)

if __name__ == '__main__':
    import pathlib

    PATH = str(pathlib.Path(__file__).parent.parent.parent.resolve())
    FILE_PATH = '/'.join((PATH, 'mid_level_features.csv'))

    data = csv_to_np(FILE_PATH,0)
    print(data)
