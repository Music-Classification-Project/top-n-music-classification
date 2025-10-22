import argparse
import random
import sys
import time
import download_data as download_data
import extract_features as extract_features
# import normalize_data as normalize_data # Does not exist yet 
import yaml
import os
from pathlib import Path


def config_loader(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def run_processing(function=None, input_path=None, output_path=None, 
                     config=config_loader("config.yaml")):
    """Wrapper function to call other functions."""
    # Call download_data function
    if function == "download":
        dataset_input = get_download_dataset_input()
        download_data_path = download_data.download_dataset(dataset_input)
        return download_data_path
    # Call normalize_data function
    elif function == "normalize":
        normalized_file_path = normalize_data.normalize_dataset(input_path)
        return normalized_file_path
    # Call extract_features function
    elif function == "extract":
        features_file_path = extract_features.extract_features(input_path, output_path, config)
        return features_file_path
    else:
        return None

def get_download_dataset_input():
    """Get user input for dataset to download."""
    dataset_input = ""
    while dataset_input not in ["gtzan", "msd", "all"]:
        dataset_input = input("Enter the dataset to download (gtzan|msd|all): ")
        if dataset_input not in ["gtzan", "msd", "all"]:
            print("Invalid input. Please enter 'gtzan', 'msd', or 'all'.")
    return dataset_input

def get_input_file_path(path_input_type, input_path=""):
    """Get user input for file path."""
    normalize_path = "data/raw"
    extract_path = "data/processed"
    
    if input_path != "":
        return input_path
    
    parent_directory = Path.cwd().parents[1]

    while True:
        if path_input_type == "normalize":
            approved_input_path = input(f"Use default normalize path {normalize_path}? (y/n): ")
        elif path_input_type == "extract":
            approved_input_path = input(f"Use default extract path {extract_path}? (y/n): ")
        else:
            print("No valid path input type provided.")
            return

        if approved_input_path.lower() == "y":
            input_path = parent_directory/normalize_path if path_input_type == "normalize" else parent_directory/extract_path
            return input_path
        elif approved_input_path.lower() == "n":
            while True:
                file_path = input("Enter the input file path: ")
                file_path = parent_directory/file_path
                if os.path.isdir(file_path):
                    approve_path = input(f"Use {file_path} as the input path? (y/n): ")
                    if approve_path.lower() == "y":
                        break
                else:
                    print("The provided path does not exist or is not a directory. Please try again.")
            return file_path
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
        
def argument_parser():
    parser = argparse.ArgumentParser(description="Processing tool to download, normalize, and extract data all at once.")
    parser.add_argument("--download", action="store_true", help="Run the download command")
    parser.add_argument("--normalize", action="store_true", help="Run the normalize command")
    parser.add_argument("--extract", action="store_true", help="Run the extract command")
    return parser.parse_args()

def main():
    # Initialize variables to hold output paths
    download_output_directory = ""
    normalized_output_directory = ""
    extract_output_directory = ""
    final_directory = ""
    # Get command line arguments
    args = argument_parser()
    # Load configuration
    config = config_loader("config.yaml")
    # Execute functions based on arguments
    # Download Function
    if args.download:
        print("Downloading data...")
        download_output_directory = run_processing("download")
        final_directory = download_output_directory
    # Normalize Function
    if args.normalize:
        print("Normalizing data...")
        input_path = get_input_file_path("normalize", download_output_directory)
        normalized_output_path = run_processing("normalize", input_path=input_path)
        final_directory = normalized_output_path
    # Extract Function
    if args.extract:
        print("Extracting features...")
        input_path = get_input_file_path("extract", normalized_output_directory)
        output_path = "../../data/features"
        extract_output_directory = run_processing("extract", input_path=input_path, 
                                                    output_path=output_path, config=config)
        final_directory = extract_output_directory

    return final_directory # Path of final output files for next step 

if __name__ == "__main__":
    main()