"""
Automates downloading and extraction of music datasets: GTZAN (Kaggle) and the Million Song Dataset (10k subset).

- GTZAN: downloads the curated dataset from Kaggle (audio tracks, spectrogram images, and CSV metadata).
- MSD: downloads the 10k Million Song Subset. Optional AdditionalFiles (SQLite) can be fetched via MSD_ADDITIONAL_URL.

Large files: add to .gitignore (examples below).
- data/raw/*.zip
- data/raw/*.tar.gz
- data/raw/MillionSongSubset/
- data/raw/Data/genres_original/

Usage:
    python download_data.py [dataset_name]

Examples:
    python download_data.py gtzan
    python download_data.py msd
    python download_data.py all

Setup requirements:
    1. Install Kaggle CLI:  pip install kaggle
    2. Create a Kaggle API key:
        - Kaggle profile > Settings > Account > Create New API Token
        - Either place kaggle.json at ~/.kaggle/kaggle.json (chmod 600) or set KAGGLE_USERNAME and KAGGLE_KEY
"""

import os
import sys
import subprocess
import zipfile
import tarfile
from pathlib import Path

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
    _env_local = Path(__file__).resolve().parent / ".env"
    if _env_local.exists():
        load_dotenv(_env_local, override=False)
except Exception:
    # Optional dependency; safe to continue without it
    pass

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"

# might add more datasets in the future
KAGGLE_DATASETS = {
    "gtzan": "andradaolteanu/gtzan-dataset-music-genre-classification",
}

EXTERNAL_DATASETS = {
    "msd": "http://labrosa.ee.columbia.edu/~dpwe/tmp/millionsongsubset.tar.gz",
    # For AdditionalFiles (SQLite metadata) provide a URL via env var MSD_ADDITIONAL_URL
    # Example (user-provided): http(s)://.../MillionSongSubset_additional.tgz
}

# ----------------- Helper Functions ----------------- #

def check_kaggle_auth():
    """Check for Kaggle API credentials via kaggle.json or env vars."""
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    user = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_KEY")
    if os.getenv("DEBUG_KAGGLE_AUTH") == "1":
        print(f"DEBUG: ~/.kaggle/kaggle.json exists? {kaggle_json.exists()}")
        print(f"DEBUG: KAGGLE_USERNAME={user!r}, KAGGLE_KEY set? {bool(key)}")
    if kaggle_json.exists() or (user and key):
        print("Kaggle credentials available (json or env).")
        return
    print(
        "Kaggle credentials not found. Add ~/.kaggle/kaggle.json or set "
        "KAGGLE_USERNAME and KAGGLE_KEY (e.g., via .env)."
    )
    sys.exit(1)


def download_kaggle_dataset(name: str, dataset_id: str, file_name: str = None):
    """Download a dataset from Kaggle. If a specific filename is provided and fails, 
    falls back to downloading the full dataset. Extracts either .zip or .tar.gz archives.
    """
    print(f"Downloading {name.upper()} dataset from Kaggle...")

    base_args = ["kaggle", "datasets", "download", "-d", dataset_id, "-p", str(RAW_DIR)]

    # Extract dataset name from Kaggle dataset_id and normalize it
    slug = dataset_id.split("/")[-1].lower()

    def _pick_latest(paths):
        return sorted(paths, key=lambda p: p.stat().st_mtime)[-1] if paths else None

    def _extract_latest():
        # Prefer a zip whose name contains the dataset slug, otherwise newest zip; fallback to .tar.gz
        zips_slug = list(RAW_DIR.glob(f"*{slug}*.zip"))
        zips_all = list(RAW_DIR.glob("*.zip"))
        tars = list(RAW_DIR.glob("*.tar.gz"))
        candidate = _pick_latest(zips_slug) or _pick_latest(zips_all) or _pick_latest(tars)
        if not candidate:
            print(f"No archive file found for {name} in {RAW_DIR}.")
            return False
        ok = extract_archive(candidate, RAW_DIR)
        if ok:
            candidate.unlink(missing_ok=True)
            print(f"{name.upper()} dataset downloaded and extracted.")
            return True
        else:
            print(f"Failed to extract {candidate.name} for {name}.")
            return False

    # Try targeted file first, if provided
    if file_name:
        try:
            subprocess.run(base_args + ["-f", file_name], check=True)
            if _extract_latest():
                return
        except subprocess.CalledProcessError:
            print(f"Could not download specified file '{file_name}'. Falling back to full download.")

    # Fallback: download full dataset
    try:
        subprocess.run(base_args, check=True)
        if _extract_latest():
            return
    except subprocess.CalledProcessError:
        print(f"Failed to download {name} from Kaggle using dataset id '{dataset_id}'.")
        try:
            print("Listing available files for the dataset:")
            subprocess.run(["kaggle", "datasets", "files", "-d", dataset_id], check=False)
        except Exception:
            pass
        sys.exit(1)


def download_external_dataset(name: str, url: str):
    """Download a dataset from a non-Kaggle URL and extract it into data/raw."""
    import requests
    from tqdm import tqdm

    print(f"Downloading {name.upper()} dataset from external source...")
    local_path = RAW_DIR / f"{name}.tar.gz"

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192

    with open(local_path, 'wb') as file, tqdm(
        total=total_size, unit='B', unit_scale=True, desc=name
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)

    ok = extract_archive(local_path, RAW_DIR)
    if ok:
        local_path.unlink(missing_ok=True)
        print(f"{name.upper()} dataset downloaded and extracted.")
    else:
        print(f"Failed to extract {local_path.name}.")


def extract_archive(file_path: Path, target_dir: Path) -> bool:
    """Extract a .zip or .tar.gz archive into target_dir. Returns True on success, False on failure."""
    print(f"Extracting {file_path.name} ...")
    try:
        if file_path.suffix == ".zip":
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(target_dir)
        elif file_path.suffixes[-2:] == [".tar", ".gz"]:
            with tarfile.open(file_path, "r:gz") as tar:
                tar.extractall(target_dir)
        else:
            print(f"Unsupported archive type for {file_path.name}")
            return False
        print("Extraction complete.")
        return True
    except Exception as e:
        print(f"Extraction failed: {e}")
        return False


def ensure_msd_additional_files():
    """Ensure MillionSongSubset AdditionalFiles (SQLite metadata) are present.

    Looks for data/raw/MillionSongSubset/AdditionalFiles/subset_track_metadata.db.
    If missing, it tries to extract a locally downloaded "additional" archive in data/raw,
    or downloads from MSD_ADDITIONAL_URL if set.
    """
    target_dir = RAW_DIR / "MillionSongSubset" / "AdditionalFiles"
    db_path = target_dir / "subset_track_metadata.db"
    if db_path.exists():
        print("MSD AdditionalFiles present (subset_track_metadata.db found).")
        return

    # Try to locate a likely archive already present
    candidates = [
        p for p in RAW_DIR.iterdir()
        if p.is_file() and any(s in p.name.lower() for s in ["additional", "add", "subset_add"]) and (
            p.suffix == ".zip" or p.suffixes[-2:] == [".tar", ".gz"]
        )
    ]
    if candidates:
        # Extract the most recent candidate
        archive_path = sorted(candidates, key=lambda p: p.stat().st_mtime)[-1]
        extract_archive(archive_path, RAW_DIR)
        if db_path.exists():
            print("MSD AdditionalFiles extracted from existing archive.")
            return

    # Download from URL if provided via the MSD_ADDITIONAL_URL environment variable
    add_url = os.getenv("MSD_ADDITIONAL_URL")
    if add_url:
        print("Downloading MSD AdditionalFiles from MSD_ADDITIONAL_URL...")
        try:
            download_external_dataset("Million Song Dataset AdditionalFiles", add_url)
            if db_path.exists():
                print("MSD AdditionalFiles downloaded and ready (subset_track_metadata.db found).")
                return
        except Exception as e:
            print(f"Failed to download AdditionalFiles: {e}")

    # Fallback: provide guidance
    print(
        "MSD AdditionalFiles not found. Provide 'subset_track_metadata.db' under \n"
        "data/raw/MillionSongSubset/AdditionalFiles, or set MSD_ADDITIONAL_URL to a valid archive."
    )


# ----------------- Dataset Manager ----------------- #


def download_dataset(name: str):
    """Main function to handle dataset downloading. Checks if files are already downloaded, if not
    the function downloads the provided dataset"""
    name = name.lower()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # check if  already downloaded and repreat for msd/all

    if name == "gtzan":
        dir_path = "data/raw/genres_original"
        alt_dir_path = "data/raw/Data/genres_original"
        if os.path.isdir(dir_path) or os.path.isdir(alt_dir_path):
            print(f"The directory {dir_path} or {alt_dir_path} already exists! No need to download :)")
            return False  # dataset already exists
        check_kaggle_auth()
        download_kaggle_dataset("GTZAN", KAGGLE_DATASETS["gtzan"])
        return True  # dataset downloaded
    
    elif name == "msd":
        dir_path = "data/raw/MillionSongSubset"
        if os.path.isdir(dir_path):
            print(f"The directory {dir_path} already exists! No need to download :)")
            ensure_msd_additional_files()
            return False
        download_external_dataset("Million Song Dataset", EXTERNAL_DATASETS["msd"])
        ensure_msd_additional_files()
        return True

    elif name == "all":
        gtzan_path = "data/raw/genres_original"
        gtzan_alt_path = "data/raw/Data/genres_original"
        msd_path = "data/raw/MillionSongSubset"

        gtzan_exists = os.path.isdir(gtzan_path) or os.path.isdir(gtzan_alt_path)
        msd_exists = os.path.isdir(msd_path)

        if gtzan_exists and msd_exists:
            print(f"Both {gtzan_path} (or {gtzan_alt_path}) and {msd_path} already exist! No need to download :)")
            ensure_msd_additional_files()
            return False

        if not gtzan_exists:
            print("Downloading GTZAN dataset...")
            check_kaggle_auth()
            download_kaggle_dataset("GTZAN", KAGGLE_DATASETS["gtzan"])

        if not msd_exists:
            print("Downloading Million Song Dataset...")
            download_external_dataset("Million Song Dataset", EXTERNAL_DATASETS["msd"])
            ensure_msd_additional_files()
        else:
            ensure_msd_additional_files()

        return True

    else:
        print("Unknown dataset name. Options: gtzan, msd, all")
        sys.exit(1)

# ----------------- Main Entry ----------------- #

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_data.py [gtzan|msd|all]")
        sys.exit(1)

    dataset_name = sys.argv[1]
    print(f"Starting download for {dataset_name.upper()}...\n")
    download_dataset(dataset_name)
    print(f"\n{dataset_name.upper()} dataset setup complete!\n")
