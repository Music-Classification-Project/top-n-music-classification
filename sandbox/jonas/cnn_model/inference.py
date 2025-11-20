# flake8: noqa
import os


class GenrePredictor:
    def __init__(self, model_path, str):
        """Initializes the predictor by loading the trained model."""
        pass

    def _preprocess_audio():
        """Loads audio, slices into windows, and converts to spectrograms."""
        pass

    def predict():
        """Performs full song prediction."""
        pass


if __name__ == "__main__":

    MODEL_PATH = "./models/genre_cnn_best.keras"
    TEST_FILE = "./data/raw/gtzan/hiphop/hiphop.00071.wav"

    predictor = GenrePredictor(MODEL_PATH)

    if os.path.exists(TEST_FILE):
        print(f"Analyzing file: {TEST_FILE}...")
        result = predictor.predict(TEST_FILE)

        print("-" * 30)
        print(f"Prediction: {result['predicted_genre'].upper()}")
        print(f"Confidence: {result['confidence'] * 100}%")
        print("-" * 30)

        print("Detailed breakdown:")
        # Sort by probability
        sorted_probs = sorted(
            result['all_probabilities'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        for g, p in sorted_probs:
            print(f"{g}: {p*100:.1f}%")

    else:
        print(f"Test file not found: {TEST_FILE}")
