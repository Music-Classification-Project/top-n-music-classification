from pathlib import Path
import librosa
import soundfile as sf
from tqdm import tqdm
from pydub import AudioSegment
import shutil

# Normalization parameters
SAMPLE_RATE = 22050  # Hz
DURATION = 10  # sec


def normalize_audio(input_path, output_dir, sample_rate=SAMPLE_RATE,
                    duration=DURATION):
    """Normalize audio file and write as .wav to output directory"""
    # Create path objects
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    # Make output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Load and resample
        y, _ = librosa.load(input_path, sr=sample_rate, mono=True)

        # Trim Silence
        y, _ = librosa.effects.trim(y)

        # Normalize volume
        y = librosa.util.normalize(y)

        # Trim or pad duration
        y = librosa.util.fix_length(y, size=sample_rate*duration)

        # Write as .wav file to output directory
        output_path = output_dir/(input_path.stem + '_norm.wav')
        sf.write(output_path, y, sample_rate)

        return output_path
    except Exception as e:
        print(f'Error processing {input_path.name}: {e}')
        return None

def split_wav_into_increments(input_file, segment_duration_seconds=DURATION, num_segments=3):
    """
    Splits a WAV file into a specified number of equal-duration segments.

    Args:
        input_file (str): The path to the input WAV file.
        output_file (str): The output wave file path (e.g., "output_").
        segment_duration_seconds (int): The duration of each segment in seconds.
        num_segments (int): The number of segments to create.
    """
    try:
        audio = AudioSegment.from_wav(input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    segment_duration_ms = segment_duration_seconds * 1000  # pydub works with milliseconds

    for i in range(num_segments):
        start_time = i * segment_duration_ms
        end_time = (i + 1) * segment_duration_ms

        # Ensure the segment does not exceed the total audio length
        if start_time >= len(audio):
            break

        segment = audio[start_time:min(end_time, len(audio))]
        output_file = f"{input_file}{i+1}.wav"
        segment.export(output_file, format="wav")
        print(f"Exported: {output_file}")

    return Path(output_file)

def batch_normalize(input_dir, output_dir):
    """Normalize all audio files in input directory and write normalized files
    as .wav to output directory"""
    # Create path objects
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # Identify supported audio files
    supported_types = {'.wav', '.mp3', '.m4a', '.ogg', '.flac', '.aac'}
    audio_files = [f for f in input_dir.rglob(
        '*') if f.suffix.lower() in supported_types]

    for file in tqdm(audio_files, desc='Normalizing audio files'):
        try:
            # Compute relative path to preserve file structure
            rel_path = file.relative_to(input_dir)
            rel_dir = rel_path.parent
            temp_dir = input_dir/"temporary"
            temp_dir.mkdir(parents=True, exist_ok=True)
            target_dir = output_dir/rel_dir
            target_dir.mkdir(parents=True, exist_ok=True)
            output_path = target_dir/(file.stem + '_norm.wav')
            audio = AudioSegment.from_wav(file)
            for segment_number in range(3):
                start_time = segment_number * DURATION
                end_time = (segment_number + 1) * DURATION
                segment = audio[start_time:min(end_time, len(audio))]
                split_file = f"{temp_dir}/{file.stem}{segment_number+1}.wav"
                segment.export(split_file, format="wav")
                split_file_path = Path(split_file)
                print("SPLIT FILE PATH", split_file_path)

            # Skip if the normalized file already exists
                if not output_path.exists():
                    normalize_audio(split_file_path, target_dir)
        except Exception as e:
            print(f'Error processing {file.name}: {e}')

    shutil.rmtree(temp_dir)
    return output_dir


if __name__ == '__main__':
    # Batch Testing
    input_dir = './data/raw/'
    output_dir = './data/processed'
    batch_normalize(input_dir, output_dir)
