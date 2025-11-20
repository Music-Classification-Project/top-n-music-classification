import os
import os.path
import wave
import librosa
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import sys
import random

"""
Dataset Analysis - May be used for raw and normalized datasets.
Requires data set path.
Example path: raw_genre_path = '../../data/raw/Data/genres_original/'
Input: Path and Processed State [Normalized, Processed, Raw]
"""

EXPECTED_GENRES = ["blues", "classical", "country", "disco", "hiphop", "jazz",
                   "metal", "pop", "reggae", "rock"]


def genre_count(path: str) -> tuple:
    """
    Input: dataset PATH
    Output: Total file count & genre count returned.
    """
    files, dirs = 0, 0

    for root, dirnames, filenames in os.walk(path):
        dirs += len(dirnames)
        files += len(filenames)
    return files, dirs


def return_genre_lst(path: str) -> list:
    """
    Input: dataset PATH
    Output: List of genre uploaded names.
    """

    genres_downloaded = []
    for genre in os.listdir(path):
        genres_downloaded.append(genre)

    return genres_downloaded


def return_wave_statistics(path: str, processed_state: str) -> dict:
    """
    Input: dataset PATH
    Output: Wave statistics returned.
    """

    wav_stats, samplerates, durations, mean_amplitudes = [], [], [], []

    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            try:
                samplerate, data = wavfile.read(root + "/" + filename)
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

    plt.plot(durations)
    plt.title('Durations')
    plt.ylabel('Duration (s)')
    plt.savefig(f'output/{processed_state}/{processed_state}_durations.png')
    plt.autoscale()
    plt.close()

    plt.plot(samplerates)
    plt.title('Sample Rates')
    plt.ylabel('Sample Rate (Hz)')
    plt.autoscale()
    plt.savefig(f'output/{processed_state}/{processed_state}_samplerates.png')
    plt.close()

    plt.plot(mean_amplitudes)
    plt.title('Mean Amplitudes')
    plt.ylabel('Amplitude (dB)')
    plt.autoscale()
    plt.savefig(f'output/{processed_state}/{processed_state}_amplitudes.png')
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
            'sd_amplitudes': int(np.std(mean_amplitudes))}


def random_wav_plot(path: str, processed_state: str):
    """ Plots random wav file in path"""
    random_genre = random.choice(EXPECTED_GENRES)
    random_wav = random.choice(os.listdir(f'{path}/{random_genre}'))
    random_pth = f'{path}/{random_genre}/{random_wav}'
    spec = wave.open(random_pth, "r")
    signal = spec.readframes(-1)
    signal = np.frombuffer(signal, dtype=np.int16)

    fs = spec.getframerate()

    time = np.linspace(0, len(signal) / fs, num=len(signal))

    plt.figure(1)
    plt.title(f'Signal Wave From Random Wave File : {random_wav}')
    plt.plot(time, signal)
    plt.autoscale()
    plt.savefig(f'output/{processed_state}/{random_wav[:-4]}.png')
    plt.close()

    y, sr = librosa.load(random_pth)
    librosa.display.waveshow(y, sr=sr)


def feature_analysis(path: str):

    """ Analyzes extracted features """

    # Generate random file path, do not include .json files
    random_genre = random.choice(os.listdir(path))
    random_npz = random.choice(os.listdir(f'{path}/{random_genre}'))

    while random_npz.endswith('.json'):
        random_npz = random.choice(os.listdir(f'{path}/{random_genre}'))
    random_pth = f'{path}/{random_genre}/{random_npz}'

    # Load Features
    loaded_file = np.load(random_pth)
    mel_spec = loaded_file['mel_spec'].squeeze()
    mfcc = loaded_file['mfcc'].squeeze()

    # Display Random MFCC
    plt.figure(figsize=(10, 5))
    librosa.display.specshow(mfcc, x_axis='time',
                             cmap='viridis', hop_length=512)
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'MFCC for {random_npz}')
    plt.xlabel('Time (s)')
    plt.ylabel('MFCC Coefficients')
    plt.savefig(f'output/{processed_state}/{random_npz[:-4]}_MFCC.png')
    plt.close()

    # Display Random Mel Spectrogram
    fig, ax = plt.subplots()
    s_db = librosa.power_to_db(mel_spec, ref=np.max)
    img = librosa.display.specshow(s_db,
                                   x_axis='time', y_axis='mel', fmax=8000,
                                   ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel-frequency spectrogram for ' + random_npz)
    fig.savefig(f'output/{processed_state}/{random_npz[:-4]}_MELSPEC.png')


def gtzan_analysis(path: str, processed_state: str):
    files, dirs = genre_count(path)
    pth = f'output/{processed_state}/{processed_state}_metrics.txt'
    with open(pth, 'w') as f:
        print('DATASET PATH: ', path, '\n', file=f, flush=True)
        print('Total Files in GTZAN Dataset: ', files, file=f)
        print('Total Genres: ', dirs, '\n', file=f)

        genres_downloaded = return_genre_lst(path)

        [print(f'{genre} {len(os.listdir(path + genre))}', file=f)
            for genre in genres_downloaded if os.path.isdir(path+genre)]
        if genres_downloaded.sort() == EXPECTED_GENRES.sort():
            print("\nDataset genres match expected.\n", file=f)

        if processed_state in ['processed', 'raw']:
            stats = return_wave_statistics(path, processed_state)
            [print(f'{stat}: {stats[stat]}', file=f) for stat in stats]
            random_wav_plot(path, processed_state)

        elif processed_state == 'features':
            feature_analysis(path)

        else:
            print("Supply 'processed', 'raw', or 'features' as the second"
                  "argument.")


if __name__ == "__main__":

    """
    EXAMPLE USAGE:
    python dataset_analysis.py '../../data/raw/Data/genres_original/' raw

    PATHS:
    raw_genre_path = '../../data/raw/Data/genres_original/'
    processed_genre_path = '../../data/processed/'
    featuers = '../../data/features/gtzan'
    """

    path = sys.argv[1]
    processed_state = sys.argv[2]

    gtzan_analysis(path, processed_state)
