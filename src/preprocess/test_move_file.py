from pathlib import Path
import os


def get_directories_in_folder(function="normalize"):
    """Get list of directories in the current folder."""
    if function == "normalize":
        # Get to download folder
        highest_directory = Path.cwd().parents[1]/"data"/"raw"
        print("Highest Directory:", highest_directory)
        isfile = False

        input_directories = set()

        def recursive_search(directory):
            nonlocal isfile
            for new_path in directory.iterdir():
                # print("Checking Path:", new_path)
                if new_path.is_dir():
                    # print("Descending into Directory:", new_path)
                    recursive_search(new_path)
                elif new_path.suffix.lower() in {'.wav', '.mp3', '.m4a',
                                                 '.ogg', '.flac', '.aac'}:
                    # print("Found File:", new_path)
                    isfile = True

                    input_directories.add(new_path.parents[1])
                    return new_path.parents[1]

        recursive_search(highest_directory)
        return input_directories

# Move all files into one directory


def move_files(input_directory):
    # Example input directory: raw/Data
    # for directory in input_directories:
    input_directory = Path(input_directory)

    isfile = False

    def recursive_search(directory):
        nonlocal isfile
        for new_path in directory.iterdir():
            # print("Checking Path:", new_path)
            if new_path.is_dir():
                # print("Descending into Directory:", new_path)
                recursive_search(new_path)
            elif new_path.is_file():  # check if a file
                # print("Found File:", new_path)
                isfile = True
                # Create directory in the input directory with the same name as
                # the parent directory
                print(new_path.parent.name)
                target_path = input_directory / new_path.parent.name
                print("Target path:", target_path)
                target_path.mkdir(parents=True, exist_ok=True)
                # Move file to target directory
                print("Moving file to:", target_path)
                new_path.rename(target_path / new_path.name)

    other_directory = input_directory / "non_genre_files"
    for new_path in input_directory.iterdir():
        if new_path.is_file():
            # Move file to target directory
            print("Moving file to:", other_directory)
            other_directory.mkdir(parents=True, exist_ok=True)
            new_path.rename(other_directory / new_path.name)

    recursive_search(input_directory)

    # Remove empty directories in input_directory
    for dirpath, dirnames, filenames in os.walk(input_directory,
                                                topdown=False):
        for dirname in dirnames:
            dir_to_check = os.path.join(dirpath, dirname)
            if not os.listdir(dir_to_check):
                print("Removing empty directory:", dir_to_check)
                os.rmdir(dir_to_check)

    return input_directory

# final_list = get_directories_in_folder()
# print(final_list)


if __name__ == "__main__":
    move_files(Path("../../data/raw/MillionSongSubset"))
