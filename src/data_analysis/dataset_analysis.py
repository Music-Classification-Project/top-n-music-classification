import os, os.path

from matplotlib.pyplot import title
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

""" 
Dataset Analysis - May be used for raw and normalized datasets. 
Requires data set path.
Example path: raw_genre_path = '../../data/raw/Data/genres_original/'
"""

EXPECTED_GENRES = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

def genre_count(path: str) -> tuple:
    """
    Input: dataset PATH
    Output: Total file count & genre count returned.
    """
    files, dirs = 0, 0

    for root, dirnames, filenames in os.walk(path):
        dirs += len(dirnames)
        files += len(filenames)
    return (files, dirs)


def return_genre_lst(path: str) -> list:
    """
    Input: dataset PATH
    Output: List of genre uploaded names.
    """

    genres_downloaded = []
    for genre in os.listdir(path):
        genres_downloaded.append(genre)

    return genres_downloaded

def return_wave_statistics(path: str) -> dict:
    """
    Input: dataset PATH
    Output: Wave statistics returned.
    """

    wav_stats, samplerates, durations, mean_amplitudes = [], [], [], []

    for root, dirnames, filenames in os.walk(path):
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

    # TODO: Prevent png overwriting
    plt.plot(durations)
    plt.title('Durations')
    plt.ylabel('Duration (s)')
    plt.savefig("output/durations.png")
    plt.close()

    plt.plot(samplerates)
    plt.title('Sample Rates')
    plt.ylabel('Sample Rate (Hz)')
    plt.savefig("output/samplerates.png", )
    plt.close()

    plt.plot(mean_amplitudes)
    plt.title('Mean Amplitudes')
    plt.ylabel('Amplitude (dB)')
    plt.savefig("output/amplitudes.png")
    plt.close()

    return {'mean_duration': int(np.mean(durations)),
            'mean_amplitude': int(np.mean(mean_amplitudes)),
            'mean_samplerate': int(np.mean(samplerates)),
            'min_duration': int(np.min(durations)),
            'max_duration': int(np.max(durations)),
            'min_amplitude': int(np.min(mean_amplitudes)),
            'max_amplitude': int(np.max(mean_amplitudes)),
            'min_samplerate': int(np.min(samplerates)),
            'max_samplerate': int(np.max(samplerates)),
            'sd_samplerates': int(np.std(samplerates)),
            'sd_durations': int(np.std(durations)),
            'sd_amplitudes': int(np.std(mean_amplitudes)),}

def gtzan_analysis(path: str):

    files, dirs = genre_count(path)
    file_name  = input("What would you like to name your output?\n")
    with open(f'output/{file_name}.txt', 'a') as f:
        print('DATASET PATH: ', path, '\n', file=f, flush=True)
        print('Total Files in GTZAN Dataset: ', files, file=f)
        print('Total Genres: ', dirs, '\n', file=f)

        genres_downloaded = return_genre_lst(path)
        [print(f'{genre} {len(os.listdir(path + genre))}', file=f) for genre in genres_downloaded]
        if genres_downloaded.sort() == EXPECTED_GENRES.sort():
            print("\nDataset genres match expected.\n",file=f)

        stats = return_wave_statistics(path)
        [print(f'{stat}: {stats[stat]}', file=f) for stat in stats]

if __name__ == "__main__":
    raw_genre_path = '../../data/raw/Data/genres_original/'
    normalized_genre_path = '../../data/processed/Data/genres_original/'
    gtzan_analysis(raw_genre_path)
    gtzan_analysis(normalized_genre_path)