"""
This script trains the model and saves it.
"""

import matplotlib.pyplot as plt
from model import MERModel
from excel_opening import y_from_excel
import pathlib
from npy_opening import data_from_npy
from keras.callbacks import EarlyStopping
from csv_opening import csv_to_np


if __name__ == '__main__':
    PATH = str(pathlib.Path(__file__).parent.resolve())
    FILE_PATH = '/'.join((PATH, '..', '..', '..', 'spectrograms/'))

    data = data_from_npy(FILE_PATH)

    expected_results = y_from_excel(
        '/'.join([PATH, '..', '..', '..', 'mean_ratings_set1.xls']))
    
    mid_level_feature_results = csv_to_np('/'.join((PATH, '..', '..', 'mid_level_features.csv')), 0)
    mid_level_feature_results = mid_level_feature_results*0.1

    A2Mid2Joint = MERModel((149, 313, 1))
    es = EarlyStopping(patience=50)
    history = A2Mid2Joint.model.fit(
        # epochs is an arbitrary big number -> early stop is the important think
        x=data, y={'emotions': expected_results, 'mid_level_features':mid_level_feature_results}, batch_size=8,
        epochs=4000, shuffle=True,
        validation_split=0.2,
        callbacks=[es]
    )
    # Save Model
    A2Mid2Joint.save()

    # list all data in history
    print(history.history.keys())
    # summarize history for emotions_correlation
    plt.plot(history.history['emotions_correlation'])
    plt.plot(history.history['val_emotions_correlation'])
    plt.title('model mse')
    plt.ylabel('mse')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for mid_level_features_correlation
    plt.plot(history.history['mid_level_features_correlation'])
    plt.plot(history.history['val_mid_level_features_correlation'])
    plt.title('model mse')
    plt.ylabel('mse')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for emotions_loss
    plt.plot(history.history['emotions_loss'])
    plt.plot(history.history['val_emotions_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for mid_level_features_loss
    plt.plot(history.history['mid_level_features_loss'])
    plt.plot(history.history['val_mid_level_features_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    

    
