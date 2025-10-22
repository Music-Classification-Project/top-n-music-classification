import argparse
import random
import sys
import time
import download_data as download_data
import extract_features as extract_features
import normalize_data as normalize_data # Does not exist yet 
import yaml

#!/usr/bin/env python3
"""

"""
def config_loader(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def download_data_main():
    """Run download_data function."""
    # Call the actual download function here
    dataset_input = ""
    while dataset_input not in ["gtzan", "msd", "all"]:
        dataset_input = input("Enter the dataset to download (gtzan|msd|all): ")
        if dataset_input not in ["gtzan", "msd", "all"]:
            print("Invalid input. Please enter 'gtzan', 'msd', or 'all'.")
    new_file_path = download_data.download_dataset(dataset_input)
    # Return file path of downloaded data
    return new_file_path

def normalize_data_main(file_path=""):
    """Run normalize_data function."""
    # If file path is empty, request a path 
    if not file_path:
        file_path = input("Enter the file path to normalize data: ")
        return file_path
    # Normalize data 
    # Pass in file path from download_data function
    # Output: Normalized data file path

def extract_data_main(input_filepath="../../data/processed", output_filepath = "../../data/features", config={}): 
    """Run extract_data function."""
    # If file path is empty, request a path 
    if not file_path:
        file_path = input("Enter the file path to extract features from: ")
        return file_path
    output_filepath = extract_features(input_filepath, output_filepath, config)
    print(output_filepath)
    return output_filepath
    # Extract features from normalized data
    # Pass in normalized data file path from normalize_data function
    # Output: Extracted features file path

def argument_parser():
    parser = argparse.ArgumentParser(description="Processing tool to download, normalize, and extract data all at once.")
    parser.add_argument("--download", action="store_true", help="Run the download command")
    parser.add_argument("--normalize", action="store_true", help="Run the normalize command")
    parser.add_argument("--extract", action="store_true", help="Run the extract command")
    return parser.parse_args()

def main():
    args = argument_parser()
    download_output_directory = ""
    # Do we ever run extract without normalize?
    normalized_output_directory = ""
    extract_output_directory = ""
    final_directory = ""
    config = config_loader("src/preprocess/config.yaml")
    if args.download:
        print("Downloading data...")
        download_output_directory = download_data_main()
        final_directory = download_output_directory
    if args.normalize:
        print("Normalizing data...")
        if download_output_directory == "":
            download_output_directory = input("Enter the file path to normalize data: ")   
        normalized_output_directory = normalize_data_main(download_output_directory)
        final_directory = normalized_output_directory
    if args.extract:
        print("Extracting features...")
        if normalized_output_directory == "":
            normalized_output_directory = input("Enter the file path to extract features from: ") 
        extract_output_directory = extract_data_main(normalized_output_directory, config)
        final_directory = extract_output_directory

    return final_directory # Path of final output files for next step 

if __name__ == "__main__":
    main()