#  Script used to train the model and save it

import matplotlib.pyplot as plt
from model import MERModel
from excel_opening import y_from_excel
import pathlib
from npy_opening import data_from_npy
from keras.callbacks import EarlyStopping

"""train the model
"""
if __name__ == '__main__':
    PATH = str(pathlib.Path(__file__).parent.resolve())
    FILE_PATH = '/'.join((PATH, '..', '..', '..', 'spectrograms/'))

    data = data_from_npy(FILE_PATH)

    expected_results = y_from_excel(
        '/'.join([PATH, '..', '..', '..', 'mean_ratings_set1.xls']))

    A2Mid2Joint = MERModel((149, 313, 1))
    # TODO Understand how data is saved and get y results
    es = EarlyStopping(patience=50)
    history = A2Mid2Joint.model.fit(
        # epochs is an arbitrary big number -> early stop is the important think
        x=data, y=expected_results, batch_size=8,
        epochs=4000, shuffle=True,
        validation_split=0.2,
        callbacks=[es]
    )
    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history['correlation'])
    plt.plot(history.history['val_correlation'])
    plt.title('model mse')
    plt.ylabel('mse')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # Save Model
    A2Mid2Joint.save()
