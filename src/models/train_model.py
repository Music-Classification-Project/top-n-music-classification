import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from keras.utils import to_categorical
from keras.callbacks import (ModelCheckpoint, EarlyStopping,
                             ReduceLROnPlateau)

from model_cnn import build_baseline_cnn_model
from typing import Dict, Any


def load_dataset(data_path: str, split: str, feature_key: str):
    """
    Loads the dataset from .npz files for a specific split (train/val/test).

    Args:
        data_path (str): Root directory of the features
        (e.g., ./data/features/gtzan)
        split (str): 'train', 'val', or 'test'
        feature_key (str): The key inside the .npz file (e.g., 'mel_spec' or
        'mfcc')

    Returns:
        X (np.ndarray): Feature data
        y (np.ndarray): Labels (integer encoded)
        genre_mapping (list): List of genre names corresponding to indices
    """
    split_path = os.path.join(data_path, split)

    X = []
    y = []

    # Ensure genres are sorted to maintain consistent index mapping
    # (0=blues, etc.)
    genres = sorted([d for d in os.listdir(split_path)
                     if os.path.isdir(os.path.join(split_path, d))])

    genre_map = {genre: i for i, genre in enumerate(genres)}

    print(f"Loading {split} data...")

    for genre in genres:
        genre_dir = os.path.join(split_path, genre)
        files = [f for f in os.listdir(genre_dir) if f.endswith('.npz')]

        for file in files:
            file_path = os.path.join(genre_dir, file)
            try:
                with np.load(file_path) as data:
                    # Extract feature matrix
                    feature = data[feature_key]
                    X.append(feature)
                    y.append(genre_map[genre])
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

    return np.array(X), np.array(y), genres


def plot_history(history):
    """Plots accuracy and loss curves."""
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))

    plt.figure(figsize=(12, 5))

    # Plot Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, label='Training Accuracy')
    plt.plot(epochs, val_acc, label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()

    # Plot Loss
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, label='Training Loss')
    plt.plot(epochs, val_loss, label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.legend()

    plt.show()


def train(feature_dir: str, model_save_path: str, config: Dict[str, Any]):
    # Load Data
    X_train, y_train, genres = load_dataset(
        feature_dir, "train", config["training_feature_key"])
    X_val, y_val, _ = load_dataset(
        feature_dir, "val", config["training_feature_key"])
    X_test, y_test, _ = load_dataset(
        feature_dir, "test", config["training_feature_key"])

    # Prepare Data (One-hot encoding for categorical crossentropy)
    num_classes = len(genres)
    y_train_oh = to_categorical(y_train, num_classes)
    y_val_oh = to_categorical(y_val, num_classes)
    y_test_oh = to_categorical(y_test, num_classes)

    input_shape = X_train[0].shape
    print("\nData Loaded:")
    print(f"Train shape: {X_train.shape}")
    print(f"Val shape:   {X_val.shape}")
    print(f"Input Shape: {input_shape}")
    print(f"Classes: {genres}")

    # Build Model
    model = build_baseline_cnn_model(
        learning_rate=config["learning_rate"],
        regularizer_1=config["regularizer_1"],
        regularizer_2=config["regularizer_2"],
        regularizer_3=config["regularizer_3"],
        regularizer_4=config["regularizer_4"],
        dropout_1=config["dropout_1"],
        dropout_2=config["dropout_2"],
        input_shape=input_shape,
        num_classes=num_classes
    )

    model.summary()

    # Set Callbacks
    callbacks = [
        # Save the best model based on validation accuracy
        ModelCheckpoint(model_save_path, save_best_only=True,
                        monitor='val_accuracy', mode='max', verbose=1),

        # Stop training if validation loss stops improving
        EarlyStopping(monitor='val_accuracy', patience=15,
                      restore_best_weights=True, verbose=1),

        # Reduce learning rate if validation loss plateaus
        ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                          patience=3, min_lr=1e-6, verbose=1)
    ]

    # Create directory for models if it doesn't exist
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)

    # Train
    print("\nStarting Training...")
    history = model.fit(
        X_train, y_train_oh,
        validation_data=(X_val, y_val_oh),
        epochs=config["epochs"],
        batch_size=config["batch_size"],
        callbacks=callbacks,
        verbose=1
    )

    # Evaluate
    plot_history(history)

    print("\nEvaluating on Test Set...")
    test_loss, test_acc = model.evaluate(X_test, y_test_oh)
    print(f"Test Accuracy: {test_acc:.4f}")

    # Detailed Classification Report
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_classes, target_names=genres))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred_classes)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=genres, yticklabels=genres)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()


if __name__ == "__main__":
    CONFIG = {
        "learning_rate": 0.0001,
        "batch_size": 32,
        "epochs": 50,
        "regularizer_1": 0.001,
        "regularizer_2": 0.001,
        "regularizer_3": 0.001,
        "regularizer_4": 0.001,
        "dropout_1": 0.3,
        "dropout_2": 0.3,
        "training_feature_key": "mel_spec"  # Must match extract_features.py
    }

    feature_dir = "./data/features/gtzan"
    model_save_path = "./models/genre_cnn_best.keras"

    train(feature_dir, model_save_path, CONFIG)
