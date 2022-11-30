from tensorflow.keras.layers import Conv2D, BatchNormalization, MaxPooling2D, Dropout, GlobalAveragePooling2D, Dense, ZeroPadding2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Input, Model
from pcc import correlation

class MERModel:
# Model build and configure model A2Mid2Joint for trainning
    def __init__(self, input_shape, learning_rate = 0.0005):

        self._input_shape = input_shape
        self._learning_rate = learning_rate
        self._model = None
        self._inputs = None
        self._outputs = None

        self._build()
        

    @property
    def model(self):
        return self._model

    def _build(self):
        self._build_total_model()
        self.compile(self._learning_rate)

    def _build_base_model(self):

        self._input = Input(shape=self._input_shape)
        x = ZeroPadding2D(padding=(2,2))(self._input)
        x = Conv2D(64, (5, 5), strides=2, activation="relu", padding="valid")(x)
        x = BatchNormalization()(x)

        # 2nd Layer
        x = ZeroPadding2D(padding=(1,1))(x)
        x = Conv2D(64, (3, 3), strides=1, activation="relu", padding="same")(x)
        x = BatchNormalization()(x)

        # 3rd Layer
        x = MaxPooling2D((2, 2))(x)
        x = Dropout(0.3)(x)

        # 4th Layer
        x = ZeroPadding2D(padding=(1,1))(x)
        x = Conv2D(128, (3, 3), strides=1, activation="relu", padding="same")(x)
        x = BatchNormalization()(x)

        # 5th Layer
        x = ZeroPadding2D(padding=(1,1))(x)
        x = Conv2D(128, (3, 3), strides=1, activation="relu", padding="same")(x)
        x = BatchNormalization()(x)

        # 6th Layer
        x = MaxPooling2D((2, 2))(x)
        x = Dropout(0.3)(x)

        # 7th Layer
        x = ZeroPadding2D(padding=(1,1))(x)
        x = Conv2D(256, (3, 3), strides=1, activation="relu", padding="same")(x)
        x = BatchNormalization()(x)

        # 8th Layer
        x = ZeroPadding2D(padding=(1,1))(x)
        x = Conv2D(256, (3, 3), strides=1, activation="relu", padding="same")(x)
        x = BatchNormalization()(x)

        # 9th Layer
        x = ZeroPadding2D(padding=(1,1))(x)
        x = Conv2D(384, (3, 3), strides=1, activation="relu", padding="same")(x)
        x = BatchNormalization()(x)

        # 10th Layer
        x = ZeroPadding2D(padding=(1,1))(x)
        x = Conv2D(512, (3, 3), strides=1, activation="relu", padding="same")(x)
        x = BatchNormalization()(x)

        # 11th Layer
        x = Conv2D(256, (3, 3), strides=1, activation="relu", padding="same")(x)
        x = BatchNormalization()(x)

        # 12th Layer
        # x = tfa.layers.AdaptiveAveragePooling2D((1,1)) 
        # x = Flatten()

        # It looks like the authors of the Paper deviate from VGG
        # in this point, they don't use fully connected layers,
        # instead they use AdaptativeAveragePooling2D(1,1) and they
        # connect the result with a final linear layer (flattening 
        # it), so by what I have been investigating this can be 
        # changed by a GlobalAveragePooling2D -> because they are 
        # using thisconcept indirectly -> AdaptiveAveragePooling2D
        # transform the input into a tensor (256,1,1), so to connect
        # it to a linnear layer we should use flatten -> the result
        # is the same as using GlobalAveragePooling
        
        x = GlobalAveragePooling2D()(x)


        return x

    def _build_A2Mid2EJointBranch(self):

        x = self._build_base_model()

        #mid_level_features =  Dense(7, name='mid_level_features')(x)

        emotions = Dense(8, activation="softmax", name='emotions')(x)

        #self._outputs = (mid_level_features, emotions)
        self._outputs = emotions
        model = Model(inputs=self._input, outputs=self._outputs, name='MusicEmotionRecognitor')

        return model

    def _build_total_model(self):

        A2Mid2EJoint_B = self._build_A2Mid2EJointBranch()
        self._model = A2Mid2EJoint_B

    def compile(self, learning_rate):
        
        optimizer = Adam(learning_rate=learning_rate)
        losses = {
            #'mid_level_features':'mse',
            'emotions':'mse',
        }
        loss_weights = {
            #'mid_level_features':1.0,
            'emotions':1.0,
        }
        metrics = [correlation]
        self._model.compile(optimizer=optimizer, loss=losses, metrics=metrics, loss_weights=loss_weights)

    def save(self):
        self._model.save('trained_MER.h5')

