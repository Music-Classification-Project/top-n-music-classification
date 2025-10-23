from pathlib import Path
import librosa
import soundfile as sf
from tqdm import tqdm


#Normalization parameters
SAMPLE_RATE = 22050 #Hz
DURATION = 10 #sec


def normalize_audio(input_path, output_dir, sample_rate = SAMPLE_RATE, duration = DURATION):
    """Normalize audio file and write as .wav to output directory"""
    #Create path objects
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    #Make output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        #Load and resample
        y, _ = librosa.load(input_path, sr=sample_rate, mono=True)

        #Trim Silence
        y, _ = librosa.effects.trim(y)

        #Normalize volume
        y = librosa.util.normalize(y)

        #Trim or pad duration
        y = librosa.util.fix_length(y, size = sample_rate*duration)

        #Write as .wav file to output directory
        output_path = output_dir/(input_path.stem + '_norm.wav')
        sf.write(output_path, y, sample_rate)

        return output_path
    except Exception as e:
        print(f'Error processing {input_path.name}: {e}')
        return None

def batch_normalize(input_dir, output_dir):
    """Normalize all audio files in input directory and write normalized files as .wav to output directory"""
    #Create path objects
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    #Make output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    #Identify supported audio files
    supported_types = {'.wav','.mp3','.m4a','.ogg','.flac','.aac'}
    audio_files = [f for f in input_dir.rglob('*') if f.suffix.lower() in supported_types]

    #Create normalized audio file if it doesn't already exist
    for file in tqdm(audio_files, desc = 'Normalizing audio files'):
        output_path = output_dir/(file.stem + '_norm.wav')
        if not output_path.exists():
            normalize_audio(file, output_dir)

    # print('\nBatch processing complete')
    return output_dir
    

if __name__ == '__main__':
    # Batch Testing
    # input_dir = './data/raw/'
    # output_dir = './data/processed/test'
    # batch_normalize(input_dir, output_dir)

    # Various file type testing
    input_path = './data/raw/mp3/Death March.mp3'
    output_dir = './data/processed/test/mp3'
    normalize_audio(input_path,output_dir)