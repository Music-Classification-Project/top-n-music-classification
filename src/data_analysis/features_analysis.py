import numpy as np
import librosa
import matplotlib.pyplot as plt

loaded_file = np.load('/Users/jaclynrutter/PycharmProjects/top-n-music-classification/data/features/gtzan/blues/blues.00000_norm.npz')

plt.figure(figsize=(10, 5))
librosa.display.specshow(loaded_file['mfcc'], x_axis='time', cmap='viridis', hop_length=512)
plt.colorbar(format='%+2.0f dB')
plt.title('MFCC')
plt.xlabel('Time (s)')
plt.ylabel('MFCC Coefficients')
plt.show()