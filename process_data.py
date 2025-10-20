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
    new_file_path = download_data.download_dataset_alt(dataset_input)
    # download_data_function(dataset_input)
    print(f"Dataset downloaded successfully.")
    print(new_file_path)

    # Pass input from user in main function to download_data function
    # Output: File path (data/raw) 

def normalize_data():
    """Run normalize_data function."""
    # Normalize data 
    # Pass in file path from download_data function
    # Output: Normalized data file path

def extract_data(): 
    """Run extract_data function."""
    # Extract features from normalized data
    # Pass in normalized data file path from normalize_data function
    # Output: Extracted features file path

def main():
    parser = argparse.ArgumentParser(description="Simple command-line tool.")
    # parser.add_argument("command", choices=["print", "loop"], help="Command to run")
    # parser.add_argument("--interval", type=float, default=1.0,
    #                     help="Seconds to wait between loop iterations (only for 'loop')")
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