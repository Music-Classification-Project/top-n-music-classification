import librosa
import numpy as np
import os
import warnings

# Ignore expected warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Genres in GTZAN_Genre_Dataset
genres = [
        "blues", "classical", "country",
        "disco", "hiphop", "jazz", "metal",
        "pop", "reggae", "rock"
        ]


# Returns a NumPy array of length 40 that contains the mean "color" (timber) of
# each of the 40 MFCCs over the first 30 seconds of the inputted audio file.
def extract_features(file_path):
    waveform, sampling_rate = librosa.load(file_path, duration=30)
    mfcc = librosa.feature.mfcc(y=waveform, sr=sampling_rate, n_mfcc=40)
    return np.mean(mfcc.T, axis=0)


def main():
    genres_path = "data/GTZAN_Genre_Dataset/genres_original"
    song_features, song_genres = [], []

    for genre in genres:
        genre_path = os.path.join(genres_path, genre)
        for file in os.listdir(f"{genres_path}/{genre}"):
            file_path = os.path.join(genre_path, file)
            try:
                features = extract_features(f"{genres_path}/{genre}/{file}")
                song_features.append(features)
                song_genres.append(genre)
            except Exception as e:
                print(f"WARNING: Skipping {file_path}: {e}")

    # Convert to NumPy arrays
    X = np.array(song_features)
    y = np.array(song_genres)

    # Save in NumPy arrays in one compressed file
    np.savez_compressed("jonas_sandbox/features_and_labels.npz", X=X, y=y)

    print("Saved features_and_labels.npz successfully!")


if __name__ == "__main__":
    main()
