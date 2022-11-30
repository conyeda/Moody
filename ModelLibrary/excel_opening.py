import xlrd
import numpy as np

def y_from_excel(path) -> np.ndarray:
    
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)

    row_count = sheet.nrows
    col_count = sheet.ncols

    y = [
        np.array([
            sheet.cell(cur_row, cur_col).value
            for cur_col in range(1, col_count-1)
        ]) / 7.83
        for cur_row in range(1, row_count)
    ]
    return np.array(y)

if __name__ == '__main__':
    import pathlib

    PATH = str(pathlib.Path(__file__).parent.resolve())
    FILE_PATH = '/'.join((PATH,'../mean_ratings_set1.xls'))
    
    data = y_from_excel(FILE_PATH)
    
    print(len(data))