from typing import Any, Dict
import os
import keras
import numpy as np
import librosa


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

        # Load audio
        try:
            audio, sr = librosa.load(audio_path, sr=self.config["sample_rate"])
        except Exception as e:
            print(f"Error loading audio: {e}")
            return np.array([])

        # Slice into 5-second non-overlapping windows
        window_samples = self.samples_per_window
        hop_samples = window_samples

        if len(audio) < window_samples:
            window_seconds = self.config["window_seconds"]
            print(
                f"Audio file is less than {window_seconds} long"
            )
            return np.array([])

        windows = []
        for start in range(0, len(audio) - window_samples + 1, hop_samples):
            end = start + window_samples
            windows.append(audio[start:end])

        # Convert windows into Mel Spectrograms
        batch_images = []
        for window in windows:
            mel_spec = librosa.feature.melspectrogram(
                y=window,
                sr=self.config["sample_rate"],
                n_fft=self.config["n_fft"],
                hop_length=self.config["hop_length"],
                n_mels=self.config["n_mels"]
            )

            # Convert to log scale (dB)
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

            # Ensure exact shape (sometimes rounding errors cause +/- 1 frame)
            # The model expects (128, 216).
            # If it's slightly off, we trim or pad.
            target_width = 216
            current_width = mel_spec_db.shape[1]

            if current_width < target_width:
                mel_spec_db = np.pad(
                    mel_spec_db,
                    ((0, 0), (0, target_width - current_width))
                )
            elif current_width > target_width:
                mel_spec_db = mel_spec_db[:, :target_width]

            # Add channel dimension (height, width, 1)
            mel_spec_db = np.expand_dims(mel_spec_db, axis=-1)
            batch_images.append(mel_spec_db)

        return np.array(batch_images)

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
        "window_seconds": 5.0,
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
