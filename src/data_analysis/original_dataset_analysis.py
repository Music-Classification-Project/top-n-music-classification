import os, os.path

"""
Analysis of raw download.
"""

# RAW file path
RAW_GENRE_PATH = '../../data/raw/Data/genres_original/'
expected_genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'reggae', 'pop', 'rock']


def genre_count():
    """
    Input: PATH ../data/raw/Data/genres_original
    Output: Total file count & genre count returned.
    """
    files, dirs = 0, 0

    for root, dirnames, filenames in os.walk(RAW_GENRE_PATH):
        dirs += len(dirnames)
        files += len(filenames)
    return (files, dirs)


def return_genre_lst():
    """
    Input: PATH ../data/raw/Data/genres_original
    Output: List of genre uploaded names.
    """

    genres_downloaded = []
    for genre in os.listdir(RAW_GENRE_PATH):
        genres_downloaded.append(genre)

    return genres_downloaded

def gtzan_raw_analysis():
    print("GTZAN Raw Analysis\n")

    files, dirs = genre_count()
    print('Total Files in GTZAN Dataset: ', files)
    print('Total Genres: ', dirs, '\n')

    genres_downloaded = return_genre_lst()
    [print(f'{genre} {len(os.listdir(RAW_GENRE_PATH + genre))}') for genre in genres_downloaded]
    if genres_downloaded.sort() == expected_genres.sort():
        print("\nDataset uploaded as expected!")



if __name__ == "__main__":
    gtzan_raw_analysis()