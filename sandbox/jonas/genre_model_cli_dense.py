import argparse
from keras.models import load_model
import preprocess_data
import warnings
import os

# Prevent TensorFlow predict-before-training/evaluating warning from showing
# 0 = all logs, 1 = filter INFO, 2 = filter WARNING, 3 = filter ERROR
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

# flake8: noqa
"""
Prediction commands:
    NOTE: The metal one is an example of overfitting on the training data, so it gives a 100% confidence score
    python jonas_sandbox/genre_model_cli.py data/GTZAN_Genre_Dataset/genres_original/metal/metal.00013.wav
    python jonas_sandbox/genre_model_cli.py data/GTZAN_Genre_Dataset/genres_original/reggae/reggae.00054.wav
    python jonas_sandbox/genre_model_cli.py data/GTZAN_Genre_Dataset/genres_original/rock/rock.00099.wav
"""

# Load the saved model
model = load_model("jonas_sandbox/music_genre_model.h5")

parser = argparse.ArgumentParser(description="Music Genre Classifier")
parser.add_argument("audio_path", help="Path to audio file")
args = parser.parse_args()

features = preprocess_data.extract_features(args.audio_path).reshape(1, -1)
predictions = model.predict(features)[0]

for genre, conf in sorted(zip(preprocess_data.genres, predictions),
                          key=lambda x: x[1], reverse=True):
    print(f"{genre:10s} — {conf:.2f}")
