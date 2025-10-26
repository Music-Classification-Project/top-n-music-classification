"""
Analysis of NORMALIZED GTZAN datset.
"""
import os

import numpy as np
from scipy.io import wavfile

NORMALIZED_PATH = '../../data/processed/Data/genres_original/'

def return_wave_statistics():
    """
    Input: Normalized wave file from raw dataset
    Output: Wave statistics returned.
    """

    wav_stats = []
    wav_stats, samplerates, durations, mean_amplitudes = [], [], [], []

    for root, dirnames, filenames in os.walk(NORMALIZED_PATH):
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

def gtzan_normalized_analysis():
    stats = return_wave_statistics()
    [print(f'{stat}: {stats[stat]}') for stat in stats]

if __name__ == '__main__':
    gtzan_normalized_analysis()