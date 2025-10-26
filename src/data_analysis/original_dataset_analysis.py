import os, os.path
from scipy.io import wavfile

import numpy as np

"""
Analysis of raw GTZAN datset.
Extracts data from PATH ../../data/raw/Data/genres_original/
"""

# RAW file path
# TODO: Extracted path to txt file / config file?

RAW_GENRE_PATH = '../../data/raw/Data/genres_original/'
expected_genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'reggae', 'pop', 'rock']


def genre_count():
    """
    Input: PATH ../data/raw/Data/genres_original
    Output: Total file count & genre count returned.
    """
    files, dirs = 0, 0

    for root, dirnames, filenames in os.walk(RAW_GENRE_PATH):
        dirs += len(dirnames)
        files += len(filenames)
    return (files, dirs)


def return_genre_lst():
    """
    Input: PATH ../data/raw/Data/genres_original
    Output: List of genre uploaded names.
    """

    genres_downloaded = []
    for genre in os.listdir(RAW_GENRE_PATH):
        genres_downloaded.append(genre)

    return genres_downloaded

def return_wave_statistics():
    """
    Input: Original wave files from raw dataset
    Output: Wave statistics returned.
    """

    wav_stats = []
    wav_stats, samplerates, durations, mean_amplitudes = [], [], [], []

    for root, dirnames, filenames in os.walk(RAW_GENRE_PATH):
        for filename in filenames:
            try:
                samplerate, data = wavfile.read(root+ "/" + filename)
                duration_sec = len(data)/samplerate
                mean_amplitude = np.mean(data)
                stats = {
                    'filename': filename,
                    'samplerate': samplerate,
                    'duration_sec': duration_sec,
                    'mean_amplitude': mean_amplitude
                }

                wav_stats.append(stats)
                samplerates.append(samplerate)
                durations.append(duration_sec)
                mean_amplitudes.append(mean_amplitude)

            except Exception as e:
                print(f'Error processing {filename}: {e}')

    return {'mean_duration': int(np.mean(durations)),
            'mean_amplitude': int(np.mean(mean_amplitudes)),
            'mean_samplerate': int(np.mean(samplerates)),
            'min_duration': int(np.min(durations)),
            'max_duration': int(np.max(durations)),
            'min_amplitude': int(np.min(mean_amplitudes)),
            'max_amplitude': int(np.max(mean_amplitudes)),
            'min_samplerate': int(np.min(samplerates)),
            'max_samplerate': int(np.max(samplerates)),}


def gtzan_raw_analysis():
    print("GTZAN Raw Analysis\n")

    files, dirs = genre_count()
    print('Total Files in GTZAN Dataset: ', files)
    print('Total Genres: ', dirs, '\n')

    genres_downloaded = return_genre_lst()
    [print(f'{genre} {len(os.listdir(RAW_GENRE_PATH + genre))}') for genre in genres_downloaded]
    if genres_downloaded.sort() == expected_genres.sort():
        print("\nDataset genres match expected.\n")

    stats = return_wave_statistics()
    [print(f'{stat}: {stats[stat]}') for stat in stats]

if __name__ == "__main__":
    gtzan_raw_analysis()