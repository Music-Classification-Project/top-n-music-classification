import argparse
import random
import sys
import time
import download_data

#!/usr/bin/env python3
"""

"""

# 1. User input: Which dataset to download? 
# 2. Config YAML for inputs that the user does not input. 
    # Potentially allow this to be editable via command line
# 3. 

def download_data_main():
    """Run download_data function."""
    # Call the actual download function here
    dataset_input = ""
    while dataset_input not in ["gtzan", "msd", "all"]:
        dataset_input = input("Enter the dataset to download (gtzan|msd|all): ")
        if dataset_input not in ["gtzan", "msd", "all"]:
            print("Invalid input. Please enter 'gtzan', 'msd', or 'all'.")
    new_file_path = download_data.download_dataset(dataset_input)
    # download_data_function(dataset_input)
    # Pass input from user in main function to download_data function
    # Output: File path (data/raw) 
    return new_file_path

def normalize_data_main(file_path=""):
    """Run normalize_data function."""
    # If file path is empty, request a path 
    if not file_path:
        file_path = input("Enter the file path to normalize data: ")
    # Normalize data 
    # Pass in file path from download_data function
    # Output: Normalized data file path

def extract_data_main(file_path): 
    """Run extract_data function."""
    # If file path is empty, request a path 
    if not file_path:
        file_path = input("Enter the file path to extract features from: ")
    # Extract features from normalized data
    # Pass in normalized data file path from normalize_data function
    # Output: Extracted features file path

def main():
    parser = argparse.ArgumentParser(description="Processing tool to download, normalize, and extract data all at once.")
    parser.add_argument("--download", action="store_true", help="Run the download command")
    parser.add_argument("--normalize", action="store_true", help="Run the normalize command")
    parser.add_argument("--extract", action="store_true", help="Run the extract command")
    args = parser.parse_args()  # Example argument for testing
    download_output_directory = ""
    normalize_output_directory = ""
    extract_output_directory = ""
    if args.download:
        download_output_directory = download_data_main()
    if args.normalize:
        if download_output_directory == "":
            normalized_output_directory = input("Enter the file path to normalize data: ")   
        else:
            normalized_output_directory = normalize_data_main(download_output_directory)
    if args.extract:
        
    
    


if __name__ == "__main__":
    main()