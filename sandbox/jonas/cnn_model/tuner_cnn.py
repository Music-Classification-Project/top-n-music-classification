"""
Tunes hyperparameters for the baseline CNN model using Keras Tuner.

Searches over learning rate, L2 regularization, and dropout parameters,
using the same GTZAN features and training pipeline as train_model_cnn.py.
"""

import os
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau
)
from datetime import datetime
import keras_tuner as kt

from model_cnn import build_baseline_cnn_model
from train_model_cnn import load_data, DATA_DIR, METADATA_PATH, RANDOM_SEED

# CONFIG
LOG_DIR = "./sandbox/jonas/cnn_model/tuner_logs"
MAX_TRIALS = 15     # Number of different combinations to test
EPOCHS = 30         # Keep small for tuning
BATCH_SIZE = 32
VAL_SIZE = 0.2
TEST_SIZE = 0.2


def build_model(hp):
    """
    Build model function for Keras Tuner.
    Defines search space for hyperparameters.
    """
    learning_rate = hp.Choice('learning_rate', [1e-4, 5e-4, 1e-3])
    regularizer = hp.Choice('regularizer', [1e-5, 1e-4, 1e-3])
    dropout_1 = hp.Float('dropout_1', 0.2, 0.5, step=0.1)
    dropout_2 = hp.Float('dropout_2', 0.2, 0.5, step=0.1)

    model = build_baseline_cnn_model(
        learning_rate=learning_rate,
        regularizer_1=regularizer,
        regularizer_2=regularizer,
        regularizer_3=regularizer,
        regularizer_4=regularizer,
        dropout_1=dropout_1,
        dropout_2=dropout_2,
        input_shape=(128, 431, 1),  # GTZAN Mel spec shape
        num_classes=10,
    )

    return model


def tune_hyperparameters():
    np.random.seed(RANDOM_SEED)  # Ensures same shuffle() result

    # Load data
    X, y, genres = load_data(METADATA_PATH, DATA_DIR, feature_key="mel_spec")

    # Dataset-wide normalization
    X = (X - np.mean(X)) / (np.std(X) + 1e-6)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=VAL_SIZE, random_state=RANDOM_SEED,
        stratify=y_train
    )

    y_train = to_categorical(y_train, num_classes=len(genres))
    y_val = to_categorical(y_val, num_classes=len(genres))
    y_test = to_categorical(y_test, num_classes=len(genres))

    # Setup tuner
    tuner_logdir = os.path.join(
        LOG_DIR, datetime.now().strftime("%Y%m%d-%H%M%S"))
    tuner = kt.RandomSearch(
        build_model,
        objective='val_accuracy',
        max_trials=MAX_TRIALS,
        executions_per_trial=1,
        directory=tuner_logdir,
        project_name='cnn_tuning'
    )

    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5,
                      restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                          patience=3, min_lr=1e-6),
    ]

    # Run search
    print(f"Starting hyperparameter tuning with {MAX_TRIALS} trials...")
    tuner.search(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        verbose=1
    )

    # Retrieve best model and parameters
    best_model = tuner.get_best_models(num_models=1)[0]
    best_hp = tuner.get_best_hyperparameters(num_trials=1)[0]

    print("\nBest Hyperparameters:")
    print(f"Learning Rate: {best_hp.get('learning_rate')}")
    print(f"Regularizer: {best_hp.get('regularizer')}")
    print(f"Dropout 1: {best_hp.get('dropout_1')}")
    print(f"Dropout 2: {best_hp.get('dropout_2')}")

    # Evaluate on test set
    test_loss, test_acc = best_model.evaluate(X_test, y_test, verbose=1)
    print(f"\nTest Accuracy (best model): {test_acc:.4f}")
    print(f"\nTest Loss (best model): {test_loss:.4f}")

    # Save best model
    save_path = "./sandbox/jonas/cnn_model/models/best_tuned_cnn.keras"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    best_model.save(save_path)
    print(f"Best model saved to {save_path}")


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    tune_hyperparameters()
