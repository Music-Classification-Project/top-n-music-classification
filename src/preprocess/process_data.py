import argparse
import random
import sys
import time
import download_data as download_data
import extract_features as extract_features
import normalize_data as normalize_data # Does not exist yet 
import yaml
import os
from pathlib import Path
import test_move_file as test_move_file


# Load configuration from YAML
def config_loader(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Get dataset input for download function
def get_download_dataset_input():
    """Get user input for dataset to download."""
    dataset_input = ""
    while dataset_input not in ["gtzan", "msd", "all"]:
        dataset_input = input("Enter the dataset to download (gtzan|msd|all): ")
        if dataset_input not in ["gtzan", "msd", "all"]:
            print("Invalid input. Please enter 'gtzan', 'msd', or 'all'.")
    return dataset_input

# # Processing function wrapper
# def run_processing(function=None, input_path=None, output_path=None, 
#                      config=config_loader("config.yaml")):
#     """Wrapper function to call other functions."""
#     # Call download_data function
#     if function == "download":
#         dataset_input = get_download_dataset_input()
#         download_data_path = download_data.download_dataset(dataset_input)
#         print("Download data path:", download_data_path)
#         for name, download_path in download_data_path.items():
#             test_move_file.move_files(download_path)
#             print(f"Dataset {name} downloaded to: {download_path}")
#         return download_data_path
#     # Call normalize_data function
#     elif function == "normalize":
#         print("Normalizing data from", input_path, "to", output_path)
#         normalized_file_path = normalize_data.batch_normalize(input_path, output_path)
#         return normalized_file_path
#     # Call extract_features function
#     elif function == "extract":
#         print("Extracting features from", input_path, "to", output_path)
#         features_file_path = extract_features.extract_features(input_path, output_path, config)
#         return features_file_path
#     else:
#         return None

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
            elif new_path.is_file(): # check if a file
                # print("Found File:", new_path)
                isfile = True
                # Create directory in the input directory with the same name as the parent directory
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
    for dirpath, dirnames, filenames in os.walk(input_directory, topdown=False):
        for dirname in dirnames:
            dir_to_check = os.path.join(dirpath, dirname)
            if not os.listdir(dir_to_check):
                print("Removing empty directory:", dir_to_check)
                os.rmdir(dir_to_check)
    return input_directory

def download():
    dataset_input = get_download_dataset_input()
    download_data_path = download_data.download_dataset(dataset_input)
    print("Download data path:", download_data_path)
    for name, download_path in download_data_path.items():
        move_files(download_path)
        print(f"Dataset {name} downloaded to: {download_path}")
    return download_data_path

def normalize(input_path, output_path):
    print("Normalizing data from", input_path, "to", output_path)
    normalized_file_path = normalize_data.batch_normalize(input_path, output_path)
    return normalized_file_path

def extract(input_path, output_path, config):
    print("Extracting features from", input_path, "to", output_path)
    features_file_path = extract_features.extract_features(input_path, output_path, config)
    return features_file_path

# Gets directories in folder to determine input paths for normalize and extract functions    
def get_directories_in_folder(function="normalize") -> set:
    """Get list of directories in the current folder."""
    isfile = False
    input_directories = {}
    if function == "normalize":
        highest_directory = Path.cwd().parents[1]/"data"/"raw" # Get to download folder
        print("Highest Directory:", highest_directory)

    elif function == "extract":
        highest_directory = Path.cwd().parents[1]/"data"/"processed" # Get to normalize folder
        print("Highest Directory:", highest_directory)

    def recursive_search(directory):
        nonlocal isfile
        for new_path in directory.iterdir():
            if new_path.is_dir():
                recursive_search(new_path)
            elif new_path.suffix.lower() in {'.wav','.mp3','.m4a','.ogg','.flac','.aac'}:
                isfile = True
                
                name = os.path.basename(new_path.parents[1]) # Set the name as the parent directory name
                input_directories[name] = new_path.parents[1] # Add to input directory 
                return new_path.parents[1]
    
    recursive_search(highest_directory) 
    return input_directories
        
# Parse Arguments 
def argument_parser():
    parser = argparse.ArgumentParser(description="Processing tool to download, normalize, and extract data all at once.")
    parser.add_argument("--download", action="store_true", help="Run the download command")
    parser.add_argument("--normalize", action="store_true", help="Run the normalize command")
    parser.add_argument("--extract", action="store_true", help="Run the extract command")
    return parser.parse_args()

# Main function 
def main():
    args = argument_parser()
    if not any([args.download, args.normalize, args.extract]):
        print("No command provided. Please use --download, --normalize, or --extract.")
        return 
    
    if args.download:        
        # Download
        download_output_directories = download()
        print(f"Datasets downloaded: {download_output_directories.keys()}")
        
        final_directories = download_output_directories

    if args.normalize:
        # Normalize
        download_output_directories = get_directories_in_folder(function="normalize")
        normalized_output_directories = {}
        if download_output_directories == {}:
            print("No downloaded datasets found. Please run the download command first.")
        
        for name, download_output_directory in download_output_directories.items():
            # input_path = get_input_file_path("normalize", download_output_directory)
            input_path = download_output_directory
            output_path = "../../data/processed" + f"/{name}"
            normalized_output_path = normalize(input_path=input_path, output_path=output_path)
            normalized_output_directories[name] = normalized_output_path
            print(f"Data normalized for {name}: {normalized_output_path}")
            
        final_directories = normalized_output_directories

    if args.extract:
        #Extract
        normalized_output_directories = get_directories_in_folder(function="extract")
        extracted_output_directories = {}
        if normalized_output_directories == {}:
            print("No normalized datasets found. Please run the normalize command first.")
        for name, normalized_output_path in normalized_output_directories.items():
            # input_path = get_input_file_path("extract", normalized_output_path)
            input_path = normalized_output_path
            output_path = "../../data/features" + f"/{name}"
            extract_output_directory = extract(input_path=input_path, 
                                                output_path=output_path, config=config_loader("config.yaml"))
            extracted_output_directories[name] = extract_output_directory
            print(f"Features extracted for {name}: {extract_output_directory}")
        
        final_directories = extracted_output_directories
    
    return final_directories

# We may not need this function, we are passing paths directly, but saving for later 
# def get_input_file_path(path_input_type, input_path=""):
#     """Get user input for file path."""
#     normalize_path = "data/raw"
#     extract_path = "data/processed"
#     if input_path != "":
#         return input_path
#     parent_directory = Path.cwd().parents[1]
#     while True:
#         if path_input_type == "normalize":
#             approved_input_path = input(f"Use default normalize path {normalize_path}? (y/n): ")
#         elif path_input_type == "extract":
#             approved_input_path = input(f"Use default extract path {extract_path}? (y/n): ")
#         else:
#             print("No valid path input type provided.")
#             return
#         if approved_input_path.lower() == "y":
#             input_path = parent_directory/normalize_path if path_input_type == "normalize" else parent_directory/extract_path
#             return input_path
#         elif approved_input_path.lower() == "n":
#             while True:
#                 file_path = input("Enter the input file path: ")
#                 file_path = parent_directory/file_path
#                 if os.path.isdir(file_path):
#                     approve_path = input(f"Use {file_path} as the input path? (y/n): ")
#                     if approve_path.lower() == "y":
#                         break
#                 else:
#                     print("The provided path does not exist or is not a directory. Please try again.")
#             return file_path
#         else:
#             print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()