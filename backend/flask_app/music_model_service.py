from typing import Union, IO, List, TypedDict
from pathlib import Path
import tempfile
import os
import numpy as np
import requests
import librosa
from flask import jsonify


class SongRecommendation(TypedDict):
    """
    A dictionary representing a single song recommendation.

    Attributes:
        title (str): The title of the recommended song
        artist (str): The artist of the song
        genre (str): The predicted or dominant genre
        similarity_score (float): Score indicating similarity to the input clip
    """
    title: str
    artist: str
    genre: str
    image_url: str


class AudioProcessingError(Exception):
    """Raised for errors during audio loading or processing."""
    pass


class ModelLoadError(Exception):
    """Raised when the model fails to load properly."""
    pass


class MusicModelService:
    def __init__(self, model_path: Union[str, Path]) -> None:
        """Loads the trained model and initializes service metadata.

        Args:
            model_path (Union[str, Path]): Path to the model file or directory.

        Raises:
            FileNotFoundError: If the model_path does not exist.
            ModelLoadError: If the model fails to load properly.
            TypeError: If model_path is not a str or Path.
        """
        if not isinstance(model_path, (str, Path)):
            raise TypeError("model_path must be a str or pathlib.Path")

        path = Path(model_path)
        if not path.exists():
            print("Model path does not exist:", str(path))
            print("Current Path:", os.getcwd())
            raise FileNotFoundError(str(path))

        try:
            self.model = self._load_model(path)
        except Exception as e:
            raise ModelLoadError(f"Failed to load model at {path}") from e

        self.model_path: Path = path
        self.loaded: bool = True
        self.model_name: str = "music-genre-classifier"
        self.version: str = "1.0"
        self.dummy_mode: bool = False

        # GTZAN genres in alphabetical order (must match training)
        self.labels: List[str] = [
            "blues",
            "classical", 
            "country",
            "disco",
            "hiphop",
            "jazz",
            "metal",
            "pop",
            "reggae",
            "rock"
        ]
        self.class_count: int = len(self.labels)

        # Audio preprocessing config (must match training)
        self.sample_rate: int = 22050
        self.input_duration_sec: int = 5
        self.channels: int = 1

        # Feature extraction config (must match training)
        self.feature_config = {
            "sample_rate": 22050,
            "window_seconds": 5,
            "normalize_audio": False,
            "n_fft": 2048,
            "hop_length": 512,
            "n_mels": 128,
            "n_mfcc": 13,
            "use_mfcc": False,
            "use_mel": True,
            "use_chroma": False,
            "normalize_per_feature": False
        }

        self.samples_per_window = int(
            self.feature_config["sample_rate"] * self.feature_config["window_seconds"]
        )

        # Store individual values for API metadata
        self.n_mels: int = 128
        self.n_mfcc: int = 13
        self.n_fft: int = 2048
        self.hop_length: int = 512
        self.feature_types: List[str] = ["mel_spec"]

        # Service constraints
        self.max_top_k: int = 10
        self.max_file_mb: int = 32

    def _load_model(self, path: Path):
        """Internal helper to load the underlying model object.

        Loads a Keras model from the specified path.
        """
        import tensorflow as tf
        model = tf.keras.models.load_model(path)
        return model
    
    def _preprocess_audio(self, audio_path: str) -> np.ndarray:
        """Loads audio, slices into windows, and converts to spectrograms."""

        # Load audio
        try:
            audio, sr = librosa.load(audio_path, sr=self.feature_config["sample_rate"])
        except Exception as e:
            print(f"Error loading audio: {e}")
            return np.array([])

        # Slice into 5-second non-overlapping windows
        window_samples = self.samples_per_window
        hop_samples = window_samples

        if len(audio) < window_samples:
            window_seconds = self.feature_config["window_seconds"]
            print(
                f"Audio file is less than {window_seconds} long"
            )
            return np.array([])

        windows = []
        for start in range(0, len(audio) - window_samples + 1, hop_samples):
            end = start + window_samples
            windows.append(audio[start:end])

        # Convert windows into Mel Spectrograms
        batch_images = []
        for window in windows:
            mel_spec = librosa.feature.melspectrogram(
                y=window,
                sr=self.feature_config["sample_rate"],
                n_fft=self.feature_config["n_fft"],
                hop_length=self.feature_config["hop_length"],
                n_mels=self.feature_config["n_mels"]
            )

            # Convert to log scale (dB)
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

            # Ensure exact shape (sometimes rounding errors cause +/- 1 frame)
            # The model expects (128, 216).
            # If it's slightly off, we trim or pad.
            target_width = 216
            current_width = mel_spec_db.shape[1]

            if current_width < target_width:
                mel_spec_db = np.pad(
                    mel_spec_db,
                    ((0, 0), (0, target_width - current_width))
                )
            elif current_width > target_width:
                mel_spec_db = mel_spec_db[:, :target_width]

            # Add channel dimension (height, width, 1)
            mel_spec_db = np.expand_dims(mel_spec_db, axis=-1)
            batch_images.append(mel_spec_db)

        return np.array(batch_images)

    def predict_genres(
        self, audio_data: Union[str, IO[bytes]], top_k: int = 5
    ) -> list[tuple[str, float]]:
        """Predicts the most likely genres for an input audio clip.

        Args:
            audio_data (Union[str, IO[bytes]]): Path to the input audio file
                or a file-like object containing the audio data.
            top_k (int, optional): The number of top genres to return.
                Defaults to 5.

        Returns:
            list[tuple[str, float]]: A list of (genre, confidence) pairs sorted
            by confidence in descending order.

        Raises:
            FileNotFoundError: If audio_data is a path that does not exist.
            AudioProcessingError: If the audio file is corrupt or in an
                                  unsupported format.
        """
        
        temp_input_file = None

        try:
            # Handle file input
            if isinstance(audio_data, str):
                # File path
                audio_file_path = audio_data
                if not Path(audio_file_path).exists():
                    raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            else: 
                # File stream
                temp_input_file = tempfile.NamedTemporaryFile(
                    delete=False, suffix=".wav"
                )
                temp_input_file.write(audio_data.read())
                temp_input_file.close()
                audio_file_path = temp_input_file.name
            

            X = self._preprocess_audio(audio_file_path)

            if len(X) == 0:
                raise AudioProcessingError("Error preprocessing audio")
            
            predictions = self.model.predict(X, verbose=0)

            # Average probabilities across all windows (Soft Voting)
            avg_probabilities = np.mean(predictions, axis=0)

            # Pair genres with probabilities and sort
            genre_probs = list(zip(self.labels, avg_probabilities))
            genre_probs.sort(key=lambda x: x[1], reverse=True)

            # Return top_k results
            top_results = genre_probs[:top_k]

            # Convert numpy float32 to Python float
            top_results = [(genre, float(prob)) for genre, prob in top_results]

            return top_results
        
        except FileNotFoundError:
            raise
        except Exception as e:
            raise AudioProcessingError(f"Error processing audio: {str(e)}") from e
        finally:
            # Clean up temporary files
            if temp_input_file is not None:
                try:
                    os.unlink(temp_input_file.name)
                except Exception:
                    pass

    def get_recommendations(
        self, audio_data: Union[str, IO[bytes]], num_recommendations: int = 5
    ) -> list[SongRecommendation]:
        """Generates song recommendations similar to the input audio clip.

        Args:
            audio_data (Union[str, IO[bytes]]): Path to the input audio file
                or a file-like object containing the audio data.
            num_recommendations (int, optional): The number of recommendations
                to generate. Defaults to 5.

        Returns:
            list[SongRecommendation]: A list of recommended songs.

        Raises:
            FileNotFoundError: If audio_data is a path that does not exist.
            AudioProcessingError: If the audio file is corrupt or in an
                                  unsupported format.
        """
        # Predict genres
        genre_results = self.predict_genres(audio_data, top_k=1)

        # Get genre with highest confidence
        top_genre = genre_results[0][0]

        # Call Last.fm API to get recommendations
        API_KEY = "bdd956594989c58ec49cff748be79644"
        BASE_URL = "http://ws.audioscrobbler.com/2.0/"

        params = {
            "method": "tag.gettoptracks",
            "tag": top_genre, 
            "api_key": API_KEY, 
            "format": "json"
        }
        
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            return jsonify({"error": "Error calling Last.fm"}), 500

        # Parse recommendations
        recs_list = []
        i=1
        while i <= num_recommendations:
            new_value = response.json()["tracks"]["track"][i]
            artist=(new_value["artist"]["name"]).replace(" ", "+")
            track=(new_value["name"].replace(" ", "+"))
            
            get_image_params = {
                "method":"track.getInfo",
                "api_key":API_KEY,
                "artist":artist,
                "track":track,
                "format":"json"
            }
            new_image_response = requests.get(BASE_URL, params=get_image_params).json()
            for key, value in new_image_response.items():
                # print(value["artist"])
                # List of title, artist, genre, album image 
                new_value["image"]=value["album"]["image"]
            
            recs_list.append(
                SongRecommendation(
                    title=new_value["name"],
                    artist=new_value["artist"]["name"],
                    genre=top_genre,
                    image_url=new_value["image"][-1]["#text"]
                )
            )
            i+=1

        return(recs_list)


class DummyMusicModelService:
    """A simple dummy implementation of MusicModelService for mocking."""

    def __init__(self, model_path: str):
        """Simulates loading a trained model from disk."""
        self.model_path = model_path
        self.loaded = True
        # Provide sensible defaults for frontend metadata
        # (aligned to src/preprocess)
        self.model_name = "dummy-music-model"
        self.version = "dummy-1.0"
        self.dummy_mode = True

        # Labels/classes (order matters in real models)
        self.labels: List[str] = [
            "rock",
            "pop",
            "jazz",
            "classical",
            "hiphop",
            "country",
            "electronic",
            "blues",
            "reggae",
            "metal",
        ]
        self.class_count = len(self.labels)

        # Audio and feature config matched to extract_features.py and
        # normalize_data.py
        self.sample_rate = 22050  # Hz
        self.input_duration_sec = 10
        self.channels = 1 

        # Feature settings
        self.feature_types = ["mel_spec", "mfcc"]
        self.n_mels = 128
        self.n_mfcc = 13
        self.n_fft = 2048
        self.hop_length = 512

        # IO constraints and formats
        self.max_top_k = 10
        self.max_file_mb = 32

    def predict_genres(
        self, audio_data: Union[str, IO[bytes]], top_k: int = 5
    ) -> List[tuple[str, float]]:
        """Always returns the same fixed genre predictions."""
        return [
            ("rock", 0.85),
            ("pop", 0.10),
            ("jazz", 0.05),
            ("blues", 0.06),
            ("classical", 0.95),
            ("disco", 0.99),
            ("jazz", 0.80)
        ][:top_k]

    def get_recommendations(self, audio_data: Union[str, IO[bytes]],
                            num_recommendations: int = 5
                            ) -> List[SongRecommendation]:
        genre_results = self.predict_genres(audio_data)
        # get genre with max similarity score
        genre = max(genre_results, key=lambda x: x[1])[0]

        # call Last FM API
        API_KEY = "bdd956594989c58ec49cff748be79644"
        BASE_URL = "http://ws.audioscrobbler.com/2.0/"

        params = {
            "method": "tag.gettoptracks",
            "tag": genre,
            "api_key": API_KEY,
            "format": "json"
        }

        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            return jsonify({"error": "Error calling Last.fm"}), 500

        recs_list = []
        i = 1
        while i <= 5:
            new_value = response.json()["tracks"]["track"][i]
            artist = (new_value["artist"]["name"]).replace(" ", "+")
            track = (new_value["name"].replace(" ", "+"))

            get_image_params = {
                "method": "track.getInfo",
                "api_key": API_KEY,
                "artist": artist,
                "track": track,
                "format": "json"
            }
            new_image_response = requests.get(
                BASE_URL, params=get_image_params).json()
            for key, value in new_image_response.items():
                # print(value["artist"])
                # List of title, artist, genre, album image
                new_value["image"] = value["album"]["image"]

            recs_list.append(
                SongRecommendation(
                    title=new_value["name"],
                    artist=new_value["artist"]["name"],
                    genre=genre,
                    image_url=new_value["image"][-1]["#text"]
                )
            )
            i += 1

        return (recs_list)

if __name__ == "__main__":
    Model = MusicModelService("model_interface/model/M4_82ta_0.68tl.keras")
    if Model.loaded:
        print("The model has loaded successfully\n\n")
    else:
        print("Model failed to load\n\n")

    print("Results for predict_genres():\n")
    print(Model.predict_genres("data/raw/Data/genres_original/metal/metal.00000.wav", 3))
    print("\n\n")

    print("Results for get_recommendations():\n")
    print(Model.get_recommendations("data/raw/Data/genres_original/metal/metal.00000.wav", 4))
    print("\n")
