from typing import Union, IO, List, TypedDict


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
    similarity_score: float


class AudioProcessingError(Exception):
    """Raised for errors during audio loading or processing."""
    pass


class ModelLoadError(Exception):
    """Raised when the model fails to load properly."""
    pass


class MusicModelService:
    def __init__(self, model_path: str):
        """Loads the trained model.

        Args:
            model_path (str): Path to the model file to load.

        Raises:
            FileNotFoundError: If the model_path does not exist.
            ModelLoadError: If the model fails to load properly.
        """
        pass

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

    def predict_genres(
        self, audio_data: Union[str, IO[bytes]], top_k: int = 5
    ) -> List[tuple[str, float]]:
        """Always returns the same fixed genre predictions."""
        return [
            ("rock", 0.85),
            ("pop", 0.10),
            ("jazz", 0.05),
        ][:top_k]

    def get_recommendations(
        self, audio_data: Union[str, IO[bytes]], num_recommendations: int = 5
    ) -> List[SongRecommendation]:
        """Always returns the same fixed set of song recommendations."""
        fixed_recommendations: List[SongRecommendation] = [
            SongRecommendation(
                title="Black Hole Sun",
                artist="Soundgarden",
                genre="rock",
                similarity_score=0.95,
            ),
            SongRecommendation(
                title="Man In The Box",
                artist="Alice In Chains",
                genre="rock",
                similarity_score=0.91,
            ),
            SongRecommendation(
                title="Lithium",
                artist="Nirvana",
                genre="rock",
                similarity_score=0.89,
            ),
            SongRecommendation(
                title="Even Flow",
                artist="Perl Jam",
                genre="rock",
                similarity_score=0.87,
            ),
            SongRecommendation(
                title="Would?",
                artist="Alice In Chains",
                genre="rock",
                similarity_score=0.85,
            ),
        ]
        return fixed_recommendations[:num_recommendations]


if __name__ == "__main__":
    mockModel = DummyMusicModelService("path/to/imaginary/model")
    if mockModel.loaded:
        print("The model has loaded successfully\n\n")

    print("Results for predict_genres():\n")
    print(mockModel.get_recommendations("path/to/imaginary/audio/file", 3))
    print("\n\n")

    print("Results for get_recommendations():\n")
    print(mockModel.get_recommendations("path/to/imaginary/audio/file", 4))
    print("\n")
