import os, os.path


# RAW file path
RAW_GENRE_PATH = r'../../data/raw/Data/genres_original/'
expected_genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'reggae', 'pop', 'rock']


def genre_count():
    files, dirs = 0, 0

    for root, dirnames, filenames in os.walk(RAW_GENRE_PATH):
        dirs += len(dirnames)
        files += len(filenames)
    print('\nTotal Files in GTZAN Dataset: ', files)
    print('Total Genres: ', dirs, '\n')

def genre_raw_file_size():
    genres_downloaded = []
    for genre in os.listdir(RAW_GENRE_PATH):
        print(f'{genre} {len(os.listdir(RAW_GENRE_PATH + genre))}')
        genres_downloaded.append(genre)
    if expected_genres.sort() == genres_downloaded.sort():
        print("Genres downloaded match expected: ", genres_downloaded)

def gtzan_raw_analysis():
    print("GTZAN Raw Analysis")
    genre_count()
    genre_raw_file_size()

if __name__ == "__main__":
    gtzan_raw_analysis()