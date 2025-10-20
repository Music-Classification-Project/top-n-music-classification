import librosa
import numpy as np
import os
import warnings


def extract_features_from_file(file_path, config):
    """Extracts features (MFCC, Mel, or Chroma) from a single audio file.
    Returns an dictionary:
        {"mfcc" : <Type: numpy.ndarray: Shape: (n_mfcc, number of frames)>,
        "mel_spec" : <Type: numpy.ndarray, Shape: (n_mels, number of frames) >,
        "chroma" : <Type: numpy.ndarray, Shape: (12, number of frames)>}
    """
    audio_array, sample_rate = librosa.load(file_path,
                                            sr=config["sample_rate"])
    features = {}

    if config["use_mfcc"]:
        mfcc = librosa.feature.mfcc(y=audio_array, sr=sample_rate,
                                    n_mfcc=config["n_mfcc"],
                                    hop_length=config["hop_length"])
        features["mfcc"] = mfcc

    if config["use_mel"]:
        mel_spec = librosa.feature.melspectrogram(
            y=audio_array,
            sr=sample_rate,
            n_fft=config["n_ftt"],
            hop_length=config["hop_length"],
            n_mels=config["n_mels"]
            )

        # Convert to decibels for better numerical stability
        features["mel_spec"] = librosa.power_to_db(mel_spec, ref=np.max)

    if config["use_chroma"]:
        features["chroma"] = librosa.feature.chroma_stft(y=audio_array,
                                                         sr=sample_rate)

    return features


def extract_features(input_dir, output_dir, config):
    """Loops through the dataset, extracts features, and saves them"""
    os.makedirs(output_dir, exist_ok=True)

    for genre in sorted(os.listdir(input_dir)):
        # Build the path to the input_dir/genre folder
        genre_input_path = os.path.join(input_dir, genre)
        if not os.path.isdir(genre_input_path):
            continue

        # Create the output_dir/genre folder
        genre_output_path = os.path.join(output_dir, genre)
        os.makedirs(genre_output_path, exist_ok=True)

        for file in os.listdir(genre_input_path):
            input_filepath = os.path.join(genre_input_path, file)

            try:
                features = extract_features_from_file(input_filepath, config)

                output_filepath = os.path.join(genre_output_path,
                                               file.replace(".wav", ".npy"))
                np.save(output_filepath, features)
            except Exception as e:
                print(f"Error processing {input_filepath}: {e}")


if __name__ == "__main__":
    # Ignore expected warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    CONFIG = {
        "sample_rate": 22050,
        "n_ftt": 2048,
        "hop_length": 512,
        "n_mels": 128,
        "n_mfcc": 13,
        "use_mfcc": True,
        "use_mel": True,
        "use_chroma": False
    }

    input_dir = "data/raw/gtzan"  # TODO: Update to "data/processed" later
    output_dir = "data/features"
    extract_features(input_dir, output_dir, CONFIG)
