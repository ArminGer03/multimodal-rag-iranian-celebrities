# Mashahir RAG v5 — Reproduction Guide

This repository contains a multi-stage pipeline to prepare data (Part 1), train an encoder model (Part 2), and run an end-to-end model (Part 3) for a RAG-style workflow.

### Repository layout
- `Mashahir_rag_5/part 1 - data preparation/`
  - `part1-crawler/` → crawl raw data
  - `part2-json/` → convert to structured JSON
  - `part3-filler/` → fill/clean/normalize fields
  - `part4-stat/` → dataset stats/QA checks
  - `part5-bio generation/` → generate bios/summaries
  - `part6-face describer/` → describe facial attributes (if applicable)
  - `part7- merge/` → merge final dataset artifacts
  - Each subfolder uses the pattern: `code/`, `input/`, `output/`
- `Mashahir_rag_5/part 2 - encoder model/`
  - `data/` → input data for encoder training/eval
- `Mashahir_rag_5/part 3 - end to end model/`
  - `code/`, `data/`, `eval_result/`

Note: individual `code/` folders contain scripts; `input/` is where you place upstream outputs; `output/` is where stage results are written.

## Prerequisites

- OS: Windows 10/11 (PowerShell)
- Python: 3.9–3.11 recommended (use one version across all parts)
- Git
- Optional but recommended: Anaconda/Miniconda

If you rely on GPU acceleration, install the correct CUDA/cuDNN stack and a GPU-enabled PyTorch/TensorFlow build as needed by your scripts.

## Environment setup

Use conda (recommended):

```powershell
# Create and activate environment
conda create -y -n mashahir-rag5 python=3.10
conda activate mashahir-rag5

# Upgrade pip
python -m pip install --upgrade pip
```

Install dependencies:

- If a `requirements.txt` or `pyproject.toml` exists inside a given `code/` folder, install from there before running that stage.
- If none are present, install packages as required by the scripts (inspect imports).

Example:

```powershell
# Example: install per-stage requirements if present
# Data prep stages
Get-ChildItem "Mashahir_rag_5\part 1 - data preparation\*\code\requirements.txt" -ErrorAction SilentlyContinue | ForEach-Object {
  pip install -r $_.FullName
}

# Encoder / end-to-end
Get-ChildItem "Mashahir_rag_5\part 2 - encoder model\code\requirements.txt" -ErrorAction SilentlyContinue | ForEach-Object {
  pip install -r $_.FullName
}
Get-ChildItem "Mashahir_rag_5\part 3 - end to end model\code\requirements.txt" -ErrorAction SilentlyContinue | ForEach-Object {
  pip install -r $_.FullName
}
```

## Configuration

- Each stage typically reads configs from:
  - a `.env` file (environment variables)
  - a YAML/JSON config in its `code/` directory
  - command-line arguments
- Common knobs:
  - input/output directories
  - language/codecs/tokenizers
  - model names/checkpoints
  - batch sizes, sequence lengths
  - random seeds
- On Windows/PowerShell, set env vars like:

```powershell
$env:PYTHONHASHSEED="0"
$env:WANDB_DISABLED="true" # if scripts integrate with wandb and you want it off
```

If a stage includes a sample config (e.g., `config.yaml`, `config.json`, `.env.example`), copy and adjust:

```powershell
Copy-Item ".env.example" ".env" -ErrorAction SilentlyContinue
Copy-Item "config.example.yaml" "config.yaml" -ErrorAction SilentlyContinue
```

**Recommendation**: keep default configs as-is for reproducibility; only change when necessary, do it in local copies, and record the exact changes (commit or save diffs).

## Reproduction — Part 1: Data preparation

Run stages in order (each subfolder under `part 1 - data preparation`):

1) `part1-crawler`
   - Place any seed lists/API keys in `input/` or `.env` as required by the scripts.
   - Outputs go to `output/`.

2) `part2-json`
   - Set `input/` to the previous stage’s `output/`.
   - Produces normalized JSON in `output/`.

3) `part3-filler`
   - Reads JSON, fills missing fields, cleans text.
   - Writes results to `output/`.

4) `part4-stat`
   - Generates dataset statistics and sanity checks.

5) `part5-bio generation`
   - Generates bios/summaries per record.

6) `part6-face describer`
   - If images are available, describes facial features.

7) `part7- merge`
   - Merges artifacts into a final dataset suitable for modeling.

Generic run pattern for each stage:

```powershell
# Replace STAGE with: part1-crawler, part2-json, ..., part7- merge
$stage = "part1-crawler"
$root = "Mashahir_rag_5\part 1 - data preparation\$stage"

# 1) Activate env (if not already)
conda activate mashahir-rag5

# 2) Install per-stage deps if present
if (Test-Path "$root\code\requirements.txt") { pip install -r "$root\code\requirements.txt" }

# 3) Set paths (adjust as needed)
$env:INPUT_DIR = "$root\input"
$env:OUTPUT_DIR = "$root\output"

# 4) Run the stage entrypoint (check the files in code\ for the correct script)
# Examples you might see: main.py, run.py, pipeline.py, crawl.py
python "$root\code\main.py" --input "$env:INPUT_DIR" --output "$env:OUTPUT_DIR"
```

If the script uses different CLI flags, run `python <script>.py --help`.

## Reproduction — Part 2: Encoder model

Inputs: final merged dataset from Part 1. Place the final artifact(s) in `Mashahir_rag_5\part 2 - encoder model\data\`.

Typical steps:

```powershell
$root = "Mashahir_rag_5\part 2 - encoder model"
conda activate mashahir-rag5
if (Test-Path "$root\code\requirements.txt") { pip install -r "$root\code\requirements.txt" }

# Common env/configs
$env:DATA_DIR = "$root\data"
$env:OUTPUT_DIR = "$root\output"   # create if your scripts expect it
New-Item -ItemType Directory -Force $env:OUTPUT_DIR | Out-Null

# Run training/eval (check code\ for the actual entrypoint and flags)
python "$root\code\train.py" --data "$env:DATA_DIR" --out "$env:OUTPUT_DIR" --seed 42
python "$root\code\eval.py"  --data "$env:DATA_DIR" --ckpt "$env:OUTPUT_DIR\best.ckpt" --out "$root\eval_result"
```

If the encoder expects a Hugging Face model or local checkpoint, set it via CLI (`--model_name_or_path`) or env var (e.g., `$env:MODEL_NAME`).

## Reproduction — Part 3: End-to-end model

Inputs: artifacts from Part 1 (processed data) and/or Part 2 (encoder checkpoints). Place inputs in `Mashahir_rag_5\part 3 - end to end model\data\`.

```powershell
$root = "Mashahir_rag_5\part 3 - end to end model"
conda activate mashahir-rag5
if (Test-Path "$root\code\requirements.txt") { pip install -r "$root\code\requirements.txt" }

$env:DATA_DIR = "$root\data"
$env:EVAL_DIR = "$root\eval_result"
New-Item -ItemType Directory -Force $env:EVAL_DIR | Out-Null

# Run pipeline/inference/eval (check the correct entrypoint and flags)
python "$root\code\run.py" --data "$env:DATA_DIR" --encoder_ckpt "..\part 2 - encoder model\output\best.ckpt" --eval_out "$env:EVAL_DIR"
```

## Data paths and handoffs

- Each stage’s `output/` should become the next stage’s `input/`.
- For clarity, copy or symlink outputs:
  - On Windows you can use junctions:
    ```powershell
    # Example: link Part 1 merged output to Part 2 data
    cmd /c mklink /J "Mashahir_rag_5\part 2 - encoder model\data\prepared" "Mashahir_rag_5\part 1 - data preparation\part7- merge\output"
    ```
- Keep a manifest (CSV/JSON) of produced files to verify completeness between stages.

## Reproducibility

- Fix seeds across frameworks:
  - `--seed 42` (CLI)
  - `$env:PYTHONHASHSEED="0"`
  - Set seeds in NumPy/PyTorch/TensorFlow inside scripts.
- Pin versions:
  - Export an env lock after success:
    ```powershell
    conda env export --no-builds > environment.lock.yml
    pip freeze > requirements.lock.txt
    ```
- Log configs:
  - Save the exact CLI and config files used per run alongside outputs.

## Troubleshooting

- Import/module errors: install missing packages in the active env.
- File-not-found: verify `input/` paths and that prior `output/` exists.
- GPU issues: confirm compatible driver/CUDA with your PyTorch/TensorFlow build.
- CLI usage: run `python <script>.py --help` in each `code/` folder.

## Quick checklist

- [ ] Python env created and activated
- [ ] Per-stage requirements installed
- [ ] `.env`/config files copied and customized
- [ ] Stage `input/` populated from previous `output/`
- [ ] Seeds and versions pinned
- [ ] Final artifacts produced in `eval_result/` (Part 3)

### Minimal config templates

- .env (copy near each stage that needs it):
```dotenv
INPUT_DIR=./input
OUTPUT_DIR=./output
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
SEED=42
WANDB_DISABLED=true
```

- YAML (if a stage uses YAML config):
```yaml
paths:
  input: ./input
  output: ./output
model:
  name_or_path: sentence-transformers/all-MiniLM-L6-v2
train:
  seed: 42
  batch_size: 32
  lr: 2e-5
  epochs: 3
```

### Dataset conventions

- Naming: prefer snake_case filenames; include split names: `train.jsonl`, `dev.jsonl`, `test.jsonl`.
- Formats:
  - JSONL records with stable fields: `id`, `text`, `title`, `meta`.
  - For retrieval: `query`, `positive_passages`, `negative_passages`.
  - For bios/faces: keep image paths relative to the stage root.
- Encoding: UTF-8, normalized newlines (\n).

### Expected outputs by part

- Part 1:
  - `part7- merge/output/` contains the final consolidated dataset (e.g., `merged.jsonl`, `metadata.json`).
- Part 2:
  - `output/` with checkpoints (`best.ckpt` or `pytorch_model.bin`), tokenizer files, and a `config.json`.
  - Optional `metrics.json` for train/eval summaries.
- Part 3:
  - `eval_result/` with evaluation tables (`scores.json`, `report.csv`) and optional predictions/runs.

### Common commands (PowerShell)

```powershell
# Validate Python and CUDA
python -V
python -c "import torch,sys;print(torch.__version__, torch.cuda.is_available())"

# Lint a stage (if ruff/flake8 installed)
pip install ruff -q
ruff check "Mashahir_rag_5/part 3 - end to end model/code"

# Quick run help
python "Mashahir_rag_5/part 3 - end to end model/code/run.py" --help
```

### FAQ

- Paths with spaces?
  - Quote all paths in commands. The repo already contains spaces in some folder names; keep quoting consistent.
- Out-of-memory on GPU?
  - Lower `batch_size`, `max_length`, or enable gradient accumulation if supported.
- Different Python per part?
  - Use a single env for reproducibility; if unavoidable, create separate envs and document versions.
- No `requirements.txt`?
  - Inspect `code/` imports and install missing libs; then freeze with `pip freeze > requirements.lock.txt`.