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

def normalize_data(file_path):
    """Run normalize_data function."""
    # Normalize data 
    # Pass in file path from download_data function
    # Output: Normalized data file path

def extract_data(file_path): 
    """Run extract_data function."""
    # Extract features from normalized data
    # Pass in normalized data file path from normalize_data function
    # Output: Extracted features file path

def main():
    parser = argparse.ArgumentParser(description="Processing tool to download, normalize, and extract data all at once.")
    parser.add_argument("--download", action="store_true", help="Run the download command")
    parser.add_argument("--loop", action="store_true", help="Run the loop command")
    parser.add_argument("--print", action="store_true", help="Run the print command")
    args = parser.parse_args()  # Example argument for testing
    if args.download:
        download_data_main()
    if args.loop:
        do_loop()
    if args.print:
        do_print()


if __name__ == "__main__":
    main()