import numpy as np
import pandas

def csv_to_np(path, skip_header) -> np.ndarray:
    """_summary_

    Args:
        path (_type_): _description_
        skip_header (_type_): skip the first n lines of the csv file being n the number of the argument

    Returns:
        np.ndarray: _description_
    """
    return np.genfromtxt(path, delimiter=';', skip_header=skip_header)

if __name__ == '__main__':
    import pathlib

    PATH = str(pathlib.Path(__file__).parent.parent.parent.resolve())
    FILE_PATH = '/'.join((PATH, 'mid_level_features.csv'))

    data = csv_to_np(FILE_PATH,0)
    print(data)
