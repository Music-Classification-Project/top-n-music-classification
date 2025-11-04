import librosa
import numpy as np
import os
from tqdm import tqdm
import json
from typing import Dict, Any


def extract_features_from_file(file_path: str,
                               config: Dict[str, Any]
                               ) -> Dict[str, np.ndarray]:
    """Extracts features (MFCC, Mel, or Chroma) from a single audio file.

    Args:
        file_path (str): Path to the audio file.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        Dict[str, np.ndarray]: A dictionary where keys are feature names
        (e.g., "mfcc", "mel_spec") and values are the feature matrices.

        Example Shapes:
         - "mfcc": (n_mfcc, number of frames, channels)
         - "mel_spec": (n_mels, number of frames, channels)
         - "chroma": (12, number of frames, channels)
    """
    audio_array, sample_rate = librosa.load(file_path,
                                            sr=config["sample_rate"])
    features = {}

    if config["use_mfcc"]:
        mfcc = librosa.feature.mfcc(y=audio_array, sr=sample_rate,
                                    n_mfcc=config["n_mfcc"],
                                    hop_length=config["hop_length"])

        mfcc_norm = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)

        features["mfcc"] = np.expand_dims(mfcc_norm, axis=-1)

    if config["use_mel"]:
        mel_spec = librosa.feature.melspectrogram(
            y=audio_array,
            sr=sample_rate,
            n_fft=config["n_fft"],
            hop_length=config["hop_length"],
            n_mels=config["n_mels"]
        )

        # Convert to decibels for better numerical stability
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        # Zero-centered normalization
        mel_spec_db_norm = (mel_spec_db - np.mean(mel_spec_db)
                            ) / (np.std(mel_spec_db) + 1e-6)

        features["mel_spec"] = np.expand_dims(mel_spec_db_norm, axis=-1)

    if config["use_chroma"]:
        chroma = librosa.feature.chroma_stft(y=audio_array, sr=sample_rate,
                                             n_fft=config["n_fft"],
                                             hop_length=config[
                                                 "hop_length"])

        chroma_norm = (chroma - np.mean(chroma)) / (np.std(chroma) + 1e-6)

        features["chroma"] = np.expand_dims(chroma_norm, axis=-1)

    return features


def extract_features(input_dir: str, output_dir: str, config: Dict[str, Any]
                     ) -> None:
    """Loops through the dataset, extracts features, and saves them"""
    os.makedirs(output_dir, exist_ok=True)
    metadata = []

    if not os.path.isdir(input_dir):
        print(
            f"Input directory {input_dir} does not exist, skipping directory.")
        return output_dir

    for genre in sorted(os.listdir(input_dir)):
        # Build the path to the input_dir/genre folder
        genre_input_path = os.path.join(input_dir, genre)
        if not os.path.isdir(genre_input_path):
            continue

        # Create the output_dir/genre folder
        genre_output_path = os.path.join(output_dir, genre)
        os.makedirs(genre_output_path, exist_ok=True)

        for file in tqdm(os.listdir(genre_input_path),
                         desc=f"Extracting features from {genre} directory"):
            input_filepath = os.path.join(genre_input_path, file)

            try:
                # Extract and save features
                features = extract_features_from_file(input_filepath, config)

                output_filepath = os.path.join(genre_output_path,
                                               file.replace(".wav", ".npz"))
                np.savez(output_filepath, **features)

                # Add info to metadata
                metadata.append({
                    "genre": genre,
                    "filename": file,
                    "features": list(features.keys())
                })

            except Exception as e:
                print(f"Error processing {input_filepath}: {e}")

    # Save metadata to output_dir/metadata.json
    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    return output_dir


if __name__ == "__main__":
    import warnings

    # Ignore expected warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    CONFIG = {
        "sample_rate": 22050,
        "n_fft": 2048,
        "hop_length": 512,
        "n_mels": 128,
        "n_mfcc": 13,
        "use_mfcc": True,
        "use_mel": True,
        "use_chroma": False
    }

    input_dir = "./data/processed/gtzan"
    output_dir = "./data/features/gtzan"
    extract_features(input_dir, output_dir, CONFIG)
