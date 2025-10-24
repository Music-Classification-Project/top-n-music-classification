"""
Defines the baseline Convolutional Neural Network (CNN) architecture
for music genre classification using Mel spectrogram inputs.

This module exposes a single function: build_cnn_model(input_shape,
num_classes) that returns a compiled Keras model ready for training.
"""


def build_cnn_model(input_shape=(128, 130, 1), num_classes=10,
                    learning_rate=0.001):
    """
    Build and compile a simple baseline CNN for genre classification.

    Parameters
    ----------
    input_shape : tuple
        Shape of input Mel spectrograms (n_mels, time_steps, 1).
    num_classes : int
        Number of output genres.
    learning_rate : float
        Learning rate for the Adam optimizer.

    Returns
    -------
    model : keras.Model
        A compiled Keras CNN model.
    """
    pass


if __name__ == "__main__":
    # Example usage of a test build
    test_model = build_cnn_model(input_shape=(128, 130, 1), num_classes=10)
    test_model.summary()
