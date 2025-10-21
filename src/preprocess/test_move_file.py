from pathlib import Path

CURRENT_DIRECTORY = Path.cwd()
print("Current directory:", CURRENT_DIRECTORY)
OUTPUT_PATH = CURRENT_DIRECTORY.parents[1] 
print(f"Output path set to: {OUTPUT_PATH}")
DATA_DIR = OUTPUT_PATH / "data"
print(f"Data directory set to: {DATA_DIR}")
RAW_DIR = DATA_DIR / "raw"
print(f"Raw data directory set to: {RAW_DIR}")
#DATA_DIR = Path("data")
#RAW_DIR = DATA_DIR / "raw"