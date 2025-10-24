from pathlib import Path

def get_directories_in_folder(function="normalize"):
    """Get list of directories in the current folder."""
    if function == "normalize":
        highest_directory = Path.cwd().parents[1]/"data"/"raw" # Get to download folder
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
                elif new_path.suffix.lower() in {'.wav','.mp3','.m4a','.ogg','.flac','.aac'}:
                    # print("Found File:", new_path)
                    isfile = True

                    input_directories.add(new_path.parents[1])
                    return new_path.parents[1]
    
        recursive_search(highest_directory)
        return input_directories

final_list = get_directories_in_folder()
print(final_list)