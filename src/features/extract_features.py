import librosa
import numpy as np
import os
from tqdm import tqdm
import json
from typing import Dict, Any


def normalize_feature(f: np.ndarray) -> np.ndarray:
    mean = np.mean(f)
    std = np.std(f)
    if std < 1e-6:
        return f - mean
    return (f - mean) / std


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
                                            sr=config["sample_rate"],
                                            mono=True)
    features = {}

    if config["use_mfcc"]:
        mfcc = librosa.feature.mfcc(y=audio_array, sr=sample_rate,
                                    n_mfcc=config["n_mfcc"],
                                    hop_length=config["hop_length"])

        features["mfcc"] = np.expand_dims(mfcc, axis=-1)

    if config["use_mel"]:
        mel_spec = librosa.feature.melspectrogram(
            y=audio_array,
            sr=sample_rate,
            n_fft=config["n_fft"],
            hop_length=config["hop_length"],
            n_mels=config["n_mels"]
        )

        # Convert to decibels (log-scale) for better numerical stability
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        if config["normalize_per_feature"]:
            mel_spec_db = normalize_feature(mel_spec_db)

        features["mel_spec"] = np.expand_dims(mel_spec_db, axis=-1)

    if config["use_chroma"]:
        chroma = librosa.feature.chroma_stft(y=audio_array, sr=sample_rate,
                                             n_fft=config["n_fft"],
                                             hop_length=config[
                                                 "hop_length"])

        features["chroma"] = np.expand_dims(chroma, axis=-1)

    return features


def extract_features(input_dir: str, output_dir: str, config: Dict[str, Any]
                     ) -> None:
    """Walks through processed dataset, extracts features, and saves them.

    Expected directory structure:
        input_dir/
            train/
                genre/
                    file.wav
            val/
                genre/
                    file.wav
            test/
                genre/
                    file.wav
    """

    os.makedirs(output_dir, exist_ok=True)
    metadata = []

    if not os.path.isdir(input_dir):
        print(
            f"Input directory {input_dir} does not exist.")
        return output_dir

    # Loop over splits (train/val/test)
    for split in sorted(os.listdir(input_dir)):
        print(f"Processing split: {split}")

        # Build the input path for the split
        split_input_path = os.path.join(input_dir, split)
        if not os.path.isdir(split_input_path):
            continue

        # Create split folder in output
        split_output_path = os.path.join(output_dir, split)
        os.makedirs(split_output_path, exist_ok=True)

        # Loop over genres inside split
        for genre in sorted(os.listdir(split_input_path)):
            # Build the path to the split's genre folder
            genre_input_path = os.path.join(split_input_path, genre)
            if not os.path.isdir(genre_input_path):
                continue

            # Sort files for reproducibility
            files = sorted(os.listdir(genre_input_path))

            # Create the split/genre folder
            genre_output_path = os.path.join(split_output_path, genre)
            os.makedirs(genre_output_path, exist_ok=True)

            for file in tqdm(
                    files,
                    desc=f"Extracting features from {genre} directory"
            ):
                if not file.lower().endswith(".wav"):
                    continue

                input_filepath = os.path.join(genre_input_path, file)

                try:
                    # Extract and save features
                    features = extract_features_from_file(
                        input_filepath, config)

                    output_name = os.path.splitext(file)[0] + ".npz"
                    output_filepath = os.path.join(genre_output_path,
                                                   output_name)
                    np.savez(output_filepath, **features)

                    # Add info to metadata
                    metadata.append({
                        "split": split,
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
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    CONFIG = {
        "sample_rate": 22050,
        "n_fft": 2048,
        "hop_length": 512,
        "n_mels": 128,
        "n_mfcc": 13,
        "use_mfcc": False,
        "use_mel": True,
        "use_chroma": False,
        "normalize_per_feature": False
    }

    input_dir = "./data/processed/gtzan"
    output_dir = "./data/features/gtzan"

    print(CONFIG)

    extract_features(input_dir, output_dir, CONFIG)
