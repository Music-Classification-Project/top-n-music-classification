# Model Performance Summary (Week 2)

- Model evaluated: `src/preprocess/final_model_4.keras`
- Note: Saved checkpoints are 6‑class models. Evaluation is on these 6 genres: `blues`, `classical`, `country`, `disco`, `hiphop`, `jazz`.
- Split: 80/20 stratified (random_state=27), matching the training validation split.
- Features: Mel spectrograms shaped `(128, 431, 1)`.


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

 Key insight: Jazz samples are most often misclassified (frequently as Country). For Jazz, the model got 0 out of 20 songs correct. Classical, Country, and Hiphop show strong recall.

## Visuals
- `confusion_matrix.png` (counts)
- `confusion_matrix_norm.png` (row‑normalized)
- `per_class_accuracy.png` (bar chart)

## Which Model Performs Best?

Based on validation metrics and our evaluation workflow, `final_model_4.keras` performs best overall. You can test other models by chaning MODEL_PATH in cell 2.

## How to Run the Evaluation Notebook

1) Create and activate a virtual environment (Windows PowerShell):
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
2) Open and run the notebook:
- VS Code: open `notebooks/model_evaluation.ipynb` → Select Kernel → choose your venv (e.g., Python (music‑eval)) → Run All.
- JupyterLab: `jupyter lab` → open the notebook → select the same kernel → Run All.

## Package Requirements for the Notebook

Added new packages to `requirements.txt` so be sure to run pip install -r requirements.txt again


