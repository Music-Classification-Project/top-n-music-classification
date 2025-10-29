"""
Defines the baseline Convolutional Neural Network (CNN) architecture
for music genre classification using Mel spectrogram inputs.

This module exposes a single function: build_baseline_cnn_model() that returns
a compiled Keras model ready for training.
"""


from keras.models import Sequential
from keras.layers import (Conv2D, BatchNormalization, MaxPooling2D, Dropout,
                          Flatten, Dense)
from keras.optimizers import Adam


def build_baseline_cnn_model(input_shape=(128, 130, 1), num_classes=10,
                             learning_rate=0.001):
    """
    Build and compile a simple baseline CNN for genre classification.

    Parameters
    ----------
    input_shape : tuple
        Shape of input Mel spectrograms (n_mels, time_steps, channels).
    num_classes : int
        Number of output genres.
    learning_rate : float
        Learning rate for the Adam optimizer.

    Returns
    -------
    model : keras.Model
        A compiled Keras CNN model.
    """

    model = Sequential(name="Baseline_CNN")

    # --- FEATURE EXTRACTION LAYERS 1, 2, & 3 ---
    # These three main layers are the "convolutional" part of the CNN. Their
    # job is to find and "detect" patterns in the spectrogram "image." Think of
    # them as a stack of increasingly sophisticated feature detectors.

    # Create layer 1: This is the core convolutional layer with 32 filters that
    # are 3x3 pixels in size. Each filter learns simple features such as a
    # sharp vertical line which might be a drum hit, or a horizontal texture
    # which might be a sustained vocal as it scans the entire input image.
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same',
                     input_shape=input_shape))
    model.add(BatchNormalization())  # Utility layer that standardizes outputs
    model.add(MaxPooling2D(pool_size=(2, 2)))  # Down-sampling layer

    # Create layer 2: These 64 filters combine the features of the first layer
    # to find more complex patterns such as a series of drum hits.
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # Create layer 3: This layer's filters combine the features of the second
    # layer to find even more complex patterns, such as a melodic pattern
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))  # Regularization technique to prevent overfitting

    # --- DECISION LAYERS ---
    # After layer 3, the model has extracted a bunch of high-level features
    # (e.g., "this looks like it has a strong backbeat," "this has complex
    # high-frequency patterns"). But the data is still in the form of many
    # small 2D "images" (called feature maps). This layer make the final
    # decision.

    # Flatten features for dense layers
    model.add(Flatten())

    # Dense layer that takes all the high-level features and learns how to
    # combine them to make a final decision.
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.4))  # Prevent overfitting

    # ---- OUTPUT LAYER ----
    # Dense layer of one neuron for each genre
    model.add(Dense(num_classes, activation='softmax'))

    # ---- COMPILE ----
    # Configures CNN for the training process
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model


if __name__ == "__main__":
    # Example usage of a test build
    test_model = build_baseline_cnn_model(input_shape=(128, 130, 1),
                                          num_classes=10)
    test_model.summary()
