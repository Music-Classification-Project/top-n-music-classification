# flake8: noqa

def extract_features_from_file(file_path, config):
    """Extracts features (MFCC, Mel, or Chroma) from a single audio file."""
    pass

def extract_features(input_dir, output_dir, config):
    """Loops through the dataset, extracts features, and saves them"""
    pass


if __name__ == "__main__":
    CONFIG = {
        "sample_rate": 22050,
        "n_ftt": 2048,
        "hop_length": 512,
        "n_mels": 128,
        "n_mfcc": 13,
        "use_mfcc": True,
        "use_mel": True,
        "use_chroma": False
    }

    input_dir = "data/raw" # TODO: Update to "data/processed" when available
    output_dir = "data/features"
    extract_features(input_dir, output_dir, CONFIG)
