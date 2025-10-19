# Dataset Sources and Layout

This project uses two datasets and stores them under `data/raw/` for preprocessing.
Run all commands from the `top-n-music-classification` directory (project root).

## GTZAN (Kaggle)
- Source: andradaolteanu/gtzan-dataset-music-genre-classification (Kaggle)
- Contains ~30s audio clips and matching spectrogram images
- Download via: `python download_data.py gtzan`
- Layout (after extraction, depending on archive):
  - `data/raw/Data/genres_original/<genre>/...` or `data/raw/genres_original/<genre>/...`
  - Genres (.wav): blues, classical, country, disco, hiphop, jazz, metal, pop, reggae, rock
  - Images: .png; spectrograms

## Million Song Dataset (10k subset)
- Source: external tarball (subset); handled by the script.
- Contains metadata about songs
- Relevant MSD fields for CNN features:
  - segments_pitches: 12 × N_segments (used as channel 0)
  - segments_timbre: 12 × N_segments (used as channel 1)
  - beats_start: N_beats (optional; for beat-synchronous averaging)
  - segments_start: N_segments (align segments to beats when beat-sync is enabled)
  - duration: seconds (sanity checks)
  - tempo: BPM (optional sanity/analysis)
- Download via: `python download_data.py msd`
- Layout: `data/raw/MillionSongSubset/` with lettered directories `A/` and `B/`.
- Optional metadata: `data/raw/MillionSongSubset/AdditionalFiles/subset_track_metadata.db`
  - To fetch automatically, set `MSD_ADDITIONAL_URL` to a direct archive URL and re-run `python download_data.py msd`.
    - Still need to test functionality of optional metadata

## Combined Download
- Download both (skips ones already present): `python download_data.py all`

## Notes
- The downloader skips re-downloading if extracted folders already exist.
- Feature export for CNNs: `python export_features.py --outdir data/features/msd`
- Can add other datasets in `EXTERNAL_DATASETS` or `KAGGLE_DATASETS` if you update guard logic (example below)

## Adding Datasets
- Add an entry in `download_data.py` under `KAGGLE_DATASETS` (Kaggle ID) or `EXTERNAL_DATASETS` (direct URL).
- Update `download_dataset(name)` with a new branch:
  - Choose an extracted folder layout under `data/raw/<dataset_name>/...`.
  - Add a guard that checks those folders and skips if present.
  - Call the existing download/extract helpers (Kaggle or external).
- If you support `all`, include the dataset there with the same guard logic.
- Document the expected folder layout here so preprocessors know where to look.
- If the dataset needs extra files (e.g., annotations/SQLite), add an `ensure_...` helper and note any env vars.