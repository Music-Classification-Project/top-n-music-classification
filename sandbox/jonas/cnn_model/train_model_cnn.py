"""
Trains a baseline CNN model for music genre classification using
pre-extracted features from the GTZAN dataset.
"""

import tensorflow as tf
import os
import numpy as np
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
# from keras import mixed_precision
# mixed_precision.set_global_policy("mixed_float16")


DATA_DIR = "./data/features/gtzan"
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")
TEST_DIR = os.path.join(DATA_DIR, "test")

LOG_DIR = "./sandbox/jonas/cnn_model/logs"
MODEL_SAVE_PATH = "./sandbox/jonas/cnn_model/models/baseline_cnn_gtzan.keras"

# CNN hyperparameters
LEARNING_RATE = 1e-3
REGULARIZER_1 = 0.0001
REGULARIZER_2 = 0.0001
REGULARIZER_3 = 0.0001
REGULARIZER_4 = 0.0001
DROPOUT_1 = 0.5
DROPOUT_2 = 0.5

# Training hyperparameters
BATCH_SIZE = 64
EPOCHS = 30
RANDOM_SEED = 42
FEATURE_KEY = "mel_spec"


def load_split_dir(split_dir, feature_key):
    """
    Loads X, y arrays from split folders such as train/val/test.

    Expected folder structure:
        split_dir/
            genre_1/
                file1.npz
                file2.npz
            genre_2/
                ...
    """

    if not os.path.isdir(split_dir):
        raise RuntimeError(f"Missing split directory: {split_dir}")

    genres = sorted([g for g in os.listdir(split_dir)
                     if os.path.isdir(os.path.join(split_dir, g))])

    genre_to_idx = {g: i for i, g in enumerate(genres)}

    X, y = [], []
    file_count = 0

    for genre in genres:
        genre_path = os.path.join(split_dir, genre)
        files = sorted(
            [f for f in os.listdir(genre_path) if f.endswith(".npz")]
        )

        for file in files:
            filepath = os.path.join(genre_path, file)

            try:
                with np.load(filepath) as data:
                    if feature_key not in data:
                        continue

                    feature = data[feature_key].astype(np.float32)
                    X.append(feature)
                    y.append(genre_to_idx[genre])
                    file_count += 1

            except Exception as e:
                print(f"Error loading {filepath}: {e}")

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int32)

    # Shuffle for safety
    X, y = shuffle(X, y, random_state=RANDOM_SEED)

    return X, y, genres, file_count


def train_model():
    np.random.seed(RANDOM_SEED)  # Ensures same shuffle() result

    print("Loading split datasets...")
    X_train, y_train, genres, train_file_count = load_split_dir(
        TRAIN_DIR, FEATURE_KEY)
    X_val, y_val, _, val_file_count = load_split_dir(VAL_DIR, FEATURE_KEY)
    X_test, y_test, _, test_file_count = load_split_dir(TEST_DIR, FEATURE_KEY)

    print(f"Loaded {train_file_count} training files.")
    print(f"Loaded {val_file_count} validation files.")
    print(f"Loaded {test_file_count} test files.")
    print(f"Genres: {genres}")
    num_classes = len(genres)

    print("X_train.shape:", X_train.shape)
    print("X_train.min():", X_train.min())
    print("X_train.max():", X_train.max())
    print("X_train.mean():", X_train.mean())
    print("X_train.std():", X_train.std())

    for i in range(0, 26):
        print("Sample mel_spec shape:", X_train[i].shape)
        print("Sample mel_spec min/max/mean:", X_train[i].min(),
              X_train[i].max(), X_train[i].mean())

    # Clip spectrograms
    X_train = np.clip(X_train, a_min=-80, a_max=0)
    X_val = np.clip(X_val, a_min=-80, a_max=0)
    X_test = np.clip(X_test, a_min=-80, a_max=0)

    # Standardize per-frequency-bin
    mean = np.mean(X_train, axis=(0, 2, 3), keepdims=True)
    std = np.std(X_train, axis=(0, 2, 3), keepdims=True) + 1e-6

    X_train = (X_train - mean) / std
    X_val = (X_val - mean) / std
    X_test = (X_test - mean) / std

    print("After normalization:")
    print("X_train.min():", X_train.min())
    print("X_train.max():", X_train.max())
    print("X_train.mean():", X_train.mean())
    print("X_train.std():", X_train.std())

    # One-hot encode labels
    y_train = to_categorical(y_train, num_classes=num_classes)
    y_val = to_categorical(y_val, num_classes=num_classes)
    y_test = to_categorical(y_test, num_classes=num_classes)

    # Build model
    input_shape = X_train.shape[1:]

    print(f"Model input_shape: {input_shape}")

    model = build_baseline_cnn_model(
        learning_rate=LEARNING_RATE,
        regularizer_1=REGULARIZER_1,
        regularizer_2=REGULARIZER_2,
        regularizer_3=REGULARIZER_3,
        regularizer_4=REGULARIZER_4,
        dropout_1=DROPOUT_1,
        dropout_2=DROPOUT_2,
        input_shape=input_shape,
        num_classes=num_classes,
    )

    # Make dirs for logging and saving model
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

    # Set start timer for training
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_logdir = os.path.join(LOG_DIR, f"run_{timestamp}")

    # Set callbacks
    callbacks = [
        EarlyStopping(monitor="val_loss", patience=10,
                      restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5,
                          patience=5, min_lr=1e-6, verbose=1),
        ModelCheckpoint(MODEL_SAVE_PATH, monitor="val_loss",
                        save_best_only=True, verbose=1),
        TensorBoard(log_dir=tensorboard_logdir),
    ]

    # Train
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    train_dataset = train_dataset.shuffle(buffer_size=1000).batch(
        BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    val_dataset = tf.data.Dataset.from_tensor_slices((X_val, y_val)).batch(
        BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    print("Starting training...")
    print("Training feature shape:", X_train.shape)
    model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        verbose=1,
    )

    # Evaluate
    test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(
        BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    test_loss, test_acc = model.evaluate(test_dataset, verbose=1)
    print(f"Test Accuracy: {test_acc:.4f}")

    # Save final model
    model.save(MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    train_model()
