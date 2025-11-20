from typing import Union, IO, List, TypedDict
from pathlib import Path
import requests
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
    # similarity_score: float
    image_url: str


class AudioProcessingError(Exception):
    """Raised for errors during audio loading or processing."""
    pass


class ModelLoadError(Exception):
    """Raised when the model fails to load properly."""
    pass

# Work in progess (only use Dummy class for now - not functional)
class MusicModelService:
    # string path or pathlib.Path object
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
            raise FileNotFoundError(str(path))

        try:
            self.model = self._load_model(path)
        except Exception as e:
            raise ModelLoadError(f"Failed to load model at {path}") from e

        # Basic service metadata; adjust as the real model is integrated
        self.model_path: Path = path
        self.loaded: bool = True
        self.version: str = "unknown"
        self.labels: List[str] = []
        self.sample_rate: int = 22050
        self.max_top_k: int = 10

    def _load_model(self, path: Path):
        """Internal helper to load the underlying model object.

        Replace this stub with the concrete framework loader (e.g., TensorFlow/PyTorch).
        """
        # TODO: Implement framework-specific loading
        return object()

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
        
        pass

    def get_recommendations(
        self, audio_data: Union[str, IO[bytes]], num_recommendations: int = 10
    ) -> list[SongRecommendation]:
        """Generates song recommendations similar to the input audio clip.

        Args:
            audio_data (Union[str, IO[bytes]]): Path to the input audio file
                or a file-like object containing the audio data.
            num_recommendations (int, optional): The number of recommendations
                to generate. Defaults to 10.

        Returns:
            list[SongRecommendation]: A list of recommended songs.

        Raises:
            FileNotFoundError: If audio_data is a path that does not exist.
            AudioProcessingError: If the audio file is corrupt or in an
                                  unsupported format.
        """
        pass


class DummyMusicModelService:
    """A simple dummy implementation of MusicModelService for mocking."""

    def __init__(self, model_path: str):
        """Simulates loading a trained model from disk."""
        self.model_path = model_path
        self.loaded = True
        # Provide sensible defaults for frontend metadata (aligned to src/preprocess)
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

        # Audio and feature config matched to extract_features.py and normalize_data.py
        self.sample_rate = 22050  # Hz
        self.input_duration_sec = 10  # seconds (see normalize_data.DURATION)
        self.channels = 1  # librosa.load(..., mono=True)

        # Feature settings (see extract_features.py CONFIG defaults)
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

    def get_recommendations(self, audio_data: Union[str, IO[bytes]], num_recommendations: int = 5) -> List[SongRecommendation]:
        genre_results = self.predict_genres(audio_data)
        # get genre with max similarity score
        genre = max(genre_results, key=lambda x: x[1])[0]

        # call Last FM API 
        API_KEY = "bdd956594989c58ec49cff748be79644"
        BASE_URL = "http://ws.audioscrobbler.com/2.0/"

        params = {
            "method":"tag.gettoptracks",
            "tag":genre, 
            "api_key":API_KEY, 
            "format":"json"
        }

        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            return jsonify({"error": "Error calling Last.fm"}), 500

        recs_list = []
        i=1
        while i <= 5:
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
                    genre=genre,
                    image_url=new_value["image"][-1]["#text"]
                )
            )
            i+=1

        return(recs_list)

        # """Always returns the same fixed set of song recommendations."""
        # fixed_recommendations: List[SongRecommendation] = [
        #     SongRecommendation(
        #         title="Black Hole Sun",
        #         artist="Soundgarden",
        #         genre="rock",
        #         similarity_score=0.95,
        #     ),
        #     SongRecommendation(
        #         title="Man In The Box",
        #         artist="Alice In Chains",
        #         genre="rock",
        #         similarity_score=0.91,
        #     ),
        #     SongRecommendation(
        #         title="Lithium",
        #         artist="Nirvana",
        #         genre="rock",
        #         similarity_score=0.89,
        #     ),
        #     SongRecommendation(
        #         title="Even Flow",
        #         artist="Perl Jam",
        #         genre="rock",
        #         similarity_score=0.87,
        #     ),
        #     SongRecommendation(
        #         title="Would?",
        #         artist="Alice In Chains",
        #         genre="rock",
        #         similarity_score=0.85,
        #     ),
        # ]
        # return fixed_recommendations[:num_recommendations]


if __name__ == "__main__":
    mockModel = DummyMusicModelService("path/to/imaginary/model")
    if mockModel.loaded:
        print("The model has loaded successfully\n\n")

    print("Results for predict_genres():\n")
    print(mockModel.predict_genres("path/to/imaginary/audio/file", 3))
    print("\n\n")

    print("Results for get_recommendations():\n")
    print(mockModel.get_recommendations("path/to/imaginary/audio/file", 4))
    print("\n")
