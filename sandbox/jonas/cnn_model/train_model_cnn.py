"""
Trains a baseline CNN model for music genre classification using
pre-extracted features from the GTZAN dataset.

This script:
  - Loads metadata.json and feature files (.npz)
  - Splits data into training/validation/test sets
  - Builds a CNN model via build_baseline_cnn_model()
  - Trains and evaluates the model
  - Saves training logs, checkpoints, and final model
"""

import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from keras.utils import to_categorical
from keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
    TensorBoard
)
from datetime import datetime
from model_cnn import build_baseline_cnn_model


DATA_DIR = "./data/features/gtzan"
METADATA_PATH = os.path.join(DATA_DIR, "metadata.json")
LOG_DIR = "./sandbox/jonas/cnn_model/logs"
MODEL_SAVE_PATH = "./sandbox/jonas/cnn_model/models/baseline_cnn_gtzan.keras"

# CNN hyperparameters
LEARNING_RATE = 0.0005
REGULARIZER_1 = 1e-5
REGULARIZER_2 = 1e-5
REGULARIZER_3 = 1e-5
REGULARIZER_4 = 1e-5
DROPOUT_1 = 0.3
DROPOUT_2 = 0.3

# Training hyperparameters
BATCH_SIZE = 32
EPOCHS = 50
TEST_SIZE = 0.2
VAL_SIZE = 0.2
RANDOM_SEED = 42


def load_data(metadata_path: str, base_dir: str, feature_key="mel_spec"):
    """
    Load features and labels from .npz files listed in metadata.json.

    Args:
        metadata_path (str): Path to metadata.json.
        base_dir (str): Base directory containing genre subfolders.
        feature_key (str): Which feature to load ('mel_spec' or 'mfcc').

    Returns:
        X (np.ndarray): Feature tensors.
        y (np.ndarray): Encoded labels.
        genres (List[str]): Genre class names.
    """

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    X, y = [], []
    genres = sorted(list({item["genre"] for item in metadata}))
    print(f"The genres are: {genres}")
    genre_to_idx = {genre: idx for idx, genre in enumerate(genres)}

    print(f"Loading data from {len(metadata)} files...")

    for entry in metadata:
        genre = entry["genre"]
        filename = entry["filename"].replace(".wav", ".npz")
        npz_path = os.path.join(base_dir, genre, filename)

        if not os.path.exists(npz_path):
            print(f"Warning: missing {npz_path}, skipping.")
            continue

        try:
            with np.load(npz_path) as data:
                if feature_key not in data:
                    continue
                feature = data[feature_key]
                X.append(feature)
                y.append(genre_to_idx[genre])
        except Exception as e:
            print(f"Error loading {npz_path}: {e}")

    X = np.array(X, dtype=np.float32)
    y = np.array(y)

    # Normalize dataset globally
    X = (X - np.mean(X)) / (np.std(X) + 1e-6)

    # Shuffle before splitting
    X, y = shuffle(X, y, random_state=RANDOM_SEED)

    print(f"Loaded {len(X)} samples with feature '{feature_key}'.")
    print(f"Feature shape: {X[0].shape if len(X) > 0 else 'N/A'}")

    return X, y, genres


def train_model():
    np.random.seed(RANDOM_SEED)  # Ensures same shuffle() result

    # Load data
    X, y, genres = load_data(METADATA_PATH, DATA_DIR, feature_key="mel_spec")

    # Train/Val/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=VAL_SIZE, random_state=RANDOM_SEED,
        stratify=y_train
    )

    # One-hot encode labels
    y_train = to_categorical(y_train, num_classes=len(genres))
    y_val = to_categorical(y_val, num_classes=len(genres))
    y_test = to_categorical(y_test, num_classes=len(genres))

    # Build model
    input_shape = X_train.shape[1:]  # (128, 431, 1)
    model = build_baseline_cnn_model(
        learning_rate=LEARNING_RATE,
        regularizer_1=REGULARIZER_1,
        regularizer_2=REGULARIZER_2,
        regularizer_3=REGULARIZER_3,
        regularizer_4=REGULARIZER_4,
        dropout_1=DROPOUT_1,
        dropout_2=DROPOUT_2,
        input_shape=input_shape,
        num_classes=len(genres),
    )

    # Set callbacks
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_logdir = os.path.join(LOG_DIR, f"run_{timestamp}")

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=10,
                      restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5,
                          patience=5, min_lr=1e-6),
        ModelCheckpoint(MODEL_SAVE_PATH, monitor="val_loss",
                        save_best_only=True),
        TensorBoard(log_dir=tensorboard_logdir),
    ]

    # Train
    print("Starting training...")
    model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        verbose=1,
    )

    # Evaluate
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=1)
    print(f"Test Accuracy: {test_acc:.4f}")

    # Save final model
    model.save(MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    import warnings

    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    train_model()
