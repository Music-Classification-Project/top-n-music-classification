# Model Performance Summary (Week 2)

- Model evaluated: `src/preprocess/final_model_4.keras`
- Note: Saved checkpoints are 6‑class models. Evaluation is on these 6 genres: `blues`, `classical`, `country`, `disco`, `hiphop`, `jazz`.
- Split: 80/20 stratified (random_state=27), matching the training validation split.
- Features: Mel spectrograms shaped `(128, 431, 1)`.
- Scripts/Notebook:
  - Notebook: `notebooks/model_evaluation.ipynb`
  - Script (reproducible CLI): `notebooks/test.py`

## Headline Metrics (current 6‑class evaluation)

- Top‑1 accuracy: ~0.725
- Top‑3 accuracy: ~0.817
- Macro precision/recall/F1: ~0.650 / ~0.725 / ~0.674 (balanced set)

Per‑class accuracy (row‑normalized confusion matrix diagonal):
- blues: ~0.80
- classical: ~0.95
- country: ~0.95
- disco: ~0.65
- hiphop: ~0.90
- jazz: ~0.00

Key insight: Jazz samples are most often misclassified (frequently as Country). Classical, Country, and Hiphop show strong recall; Disco shows moderate confusion.

Artifacts (saved by the script under `docs/visuals/`):
- `confusion_matrix.png` (counts)
- `confusion_matrix_norm.png` (row‑normalized)
- `per_class_accuracy.png` (bar chart)
- JSON summary: `eval_final_model_4.json` (when evaluating `final_model_4.keras`)

## Which Model Performs Best?

Team‑reported validation results indicate:
- `final_model_1.keras`: val loss ≈ 0.48, val acc ≈ 85%
- `final_model_4.keras`: val loss ≈ 0.50, val acc ≈ 87.5%

Based on validation metrics and our evaluation workflow, `final_model_4.keras` performs best overall. You can verify quickly with the CLI (see below) and compare accuracy/top‑3 across checkpoints.

## How to Run the Evaluation Notebook

1) Create and activate a virtual environment (Windows PowerShell):
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) Ensure Jupyter and kernel are available (if not using VS Code’s built‑in support):
```
pip install ipykernel jupyterlab seaborn matplotlib
python -m ipykernel install --user --name music-eval --display-name "Python (music-eval)"
```

3) Open and run the notebook:
- VS Code: open `notebooks/model_evaluation.ipynb` → Select Kernel → choose your venv (e.g., Python (music‑eval)) → Run All.
- JupyterLab: `jupyter lab` → open the notebook → select the same kernel → Run All.

Notes:
- Because the notebook lives under `notebooks/`, paths are set to resolve the project root; no manual `chdir` is required in the current cells.
- If you change kernels or environments, re‑run the first two cells and confirm the printed path checks are `True`.

## How to Run the Evaluation Script (CLI)

From the project root:
```
python notebooks/test.py -m src/preprocess/final_model_4.keras
```

Outputs:
- Overall accuracy and top‑3 accuracy printed to console
- Confusion matrices and per‑class accuracy saved to `docs/visuals/`
- JSON summary saved to `docs/visuals/eval_final_model_4.json`

You can swap the `-m` argument to compare other checkpoints:
```
python notebooks/test.py -m src/preprocess/final_model_1.keras
```

## Package Requirements for the Notebook

The notebook requires the following (already captured in `requirements.txt`):
- `tensorflow==2.20.0` (or `tensorflow-cpu==2.20.0` on CPU‑only systems)
- `scikit-learn==1.6.1`
- `numpy==2.0.2`
- `matplotlib==3.9.2`
- `seaborn==0.13.2`
- `ipykernel==6.29.5`
- One of: `jupyterlab==4.x` or `notebook==7.x` (VS Code can run notebooks without these via its UI)

Tip: If you see environment import errors, ensure the notebook kernel matches the venv where you installed packages (Kernel → Select Kernel). 

