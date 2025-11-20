# flake8: noqa
from typing import Any


import os
from keras import keras
from types import Dict, Any
import numpy as np

class GenrePredictor:
    def __init__(self, model_path: str, config: Dict[str, Any]):
        """Initializes the predictor by loading the trained model."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")

        print(f"Loading model from {model_path}...")
        self.model = keras.models.load_model(model_path)

        self.genres = sorted([
            'blues', 'classical', 'country', 'disco', 'hiphop', 
            'jazz', 'metal', 'pop', 'reggae', 'rock'
        ])

        self.config = config

        self.samples_per_window = int(
            self.config["sample_rate"] * self.config["window_seconds"]
            )

    def _preprocess_audio(self, audio_path: str) -> np.ndarray:
        """Loads audio, slices into windows, and converts to spectrograms."""
        pass

    def predict(self, audio_path: str) -> Dict:
        """Performs full song prediction."""

        X = self._preprocess_audio(audio_path)

        if len(X) == 0:
            return {"error": "could not process audio"}

        predictions = self.model.predict(X, verbose=0)

        # Average probabilities across all windows (Soft Voting)
        avg_probabilities = np.mean(predictions, axis=0)

        top_index = np.argmax(avg_probabilities)
        predicted_genre = self.genres[top_index]
        confidence = avg_probabilities[top_index]

        result = {
            "filename": os.path.basename(audio_path),
            "predicted_genre": predicted_genre,
            "confidence": float(f"{confidence: .2f}"),
            "all_probabilities": {
                genre: float(f"{prob :.4f}")
                for genre, prob in zip(self.genres, avg_probabilities)
            }
        }

        return result


if __name__ == "__main__":

    MODEL_PATH = "models/82ta_0.68loss.keras"
    TEST_FILE = "./data/raw/gtzan/hiphop/hiphop.00071.wav"

    config = {
        "sample_rate": 22050,
        "window_seconds": 5.0,  # Duration of each window in seconds
        "normalize_audio": False,
        "n_fft": 2048,
        "hop_length": 512,
        "n_mels": 128,
        "use_mfcc": False,
        "use_mel": True,
        "use_chroma": False,
        "normalize_per_feature": False
    }

    predictor = GenrePredictor(MODEL_PATH, config)

    if os.path.exists(TEST_FILE):
        print(f"Analyzing file: {TEST_FILE}...")
        result = predictor.predict(TEST_FILE)

        print("-" * 30)
        print(f"Prediction: {result['predicted_genre'].upper()}")
        print(f"Confidence: {result['confidence'] * 100}%")
        print("-" * 30)

        print("Prediction probabilities:")
        sorted_probs = sorted(
            result['all_probabilities'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        for g, p in sorted_probs:
            print(f"{g}: {p*100:.1f}%")

    else:
        print(f"Test file not found: {TEST_FILE}")
