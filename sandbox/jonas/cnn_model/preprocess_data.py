import numpy as np
import os
from typing import Dict, Any, List, Tuple
import librosa
import soundfile as sf
from pathlib import Path
import random
import shutil


def normalize_audio(audio: np.ndarray) -> np.ndarray:
    """Normalizes audio to -1 to 1 with peak normalization."""
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio
    return audio / peak


def slice_audio(audio: np.ndarray, config: Dict[str, Any]) -> list[np.ndarray]:
    """Slices audio into overlapping windows."""
    window_samples = int(config["window_seconds"] * config["sample_rate"])
    hop_samples = int(window_samples * (1 - config["window_overlap"]))

    slices = []
    for start in range(0, len(audio) - window_samples + 1, hop_samples):
        end = start + window_samples
        slices.append(audio[start:end])

    return slices


def create_dir(path: str):
    """Creates directory if it does not exist."""
    Path(path).mkdir(parents=True, exist_ok=True)


def process_file(file_path: str, output_dir: str, config: Dict[str, Any]
                 ) -> None:
    """Loads a file, normalizes it, slices it into windows, and saves processed
    clips."""
    try:
        audio, sr = librosa.load(file_path, sr=config["sample_rate"])

        if config["normalize_audio"]:
            audio = normalize_audio(audio)

        windows = slice_audio(audio, config)

        base_name = os.path.splitext(os.path.basename(file_path))[0]

        for i, chunk in enumerate(windows):
            out_path = os.path.join(output_dir, f"{base_name}_win{i}.wav")
            sf.write(out_path, chunk, sr)

    except Exception as e:
        print(f"ERROR Failed to process {file_path}: {e}")


def split_song_list(songs: List[str], splits: Tuple[float, float, float]
                    ) -> Tuple[List, List, List]:
    """Splits songs list into train/val/test using fixed ratios."""
    train_ratio, val_ratio, test_ratio = splits

    total = len(songs)
    n_train = int(total * train_ratio)
    n_val = int(total * val_ratio)

    train_songs = songs[:n_train]
    val_songs = songs[n_train: n_train + n_val]
    test_songs = songs[n_train + n_val:]

    return train_songs, val_songs, test_songs


def preprocess_dataset(raw_dir: str, processed_dir: str, config: Dict[str, Any]
                       ) -> None:
    """"""
    print("Starting preprocessing...")

    random.seed(config["random_seed"])

    genres = [d for d in os.listdir(raw_dir)
              if os.path.isdir(os.path.join(raw_dir, d))]

    for split in ["train", "val", "test"]:
        create_dir(os.path.join(processed_dir, split))

    create_dir(os.path.join(processed_dir, "test_unprocessed"))

    for genre in genres:
        print(f"Processing genre: {genre}")

        genre_raw_path = os.path.join(raw_dir, genre)

        songs = [f for f in os.listdir(genre_raw_path)
                 if f.lower().endswith(".wav")]

        random.shuffle(songs)

        splits = split_song_list(
            songs,
            (
                config["train_ratio"],
                config["val_ratio"],
                config["test_ratio"]
            )
        )

        split_map = {
            "train": splits[0],
            "val": splits[1],
            "test": splits[2]
        }

        for split_name, split_files in split_map.items():
            print(
                f"Processing {split_name} split for {genre}: \
                 {len(split_files)} songs")

            genre_proc_path = os.path.join(processed_dir, split_name,
                                           genre)
            create_dir(genre_proc_path)

            if split_name == "test":
                unsliced_genre_path = os.path.join(
                    processed_dir, "test_unprocessed", genre)
                create_dir(unsliced_genre_path)

            for filename in split_files:
                file_path = os.path.join(genre_raw_path, filename)
                process_file(file_path, genre_proc_path, config)

                if split_name == "test":
                    unsliced_dest_path = os.path.join(
                        unsliced_genre_path, filename
                    )
                    shutil.copy2(file_path, unsliced_dest_path)                    

        print(f"Finished processing genre: {genre}.")

    print("Preprocessing complete.")


if __name__ == "__main__":
    CONFIG = {
        "sample_rate": 22050,
        "window_seconds": 5.0,
        "window_overlap": .50,
        "normalize_audio": False,
        "random_seed": 42,
        "train_ratio": .7,
        "val_ratio": .1,
        "test_ratio": .2
    }
    raw_dir = "./data/raw/gtzan"
    processed_dir = "./data/processed/gtzan"

    print(CONFIG)

    preprocess_dataset(raw_dir, processed_dir, CONFIG)
