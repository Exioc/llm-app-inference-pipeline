# Project Setup Instructions

## Prerequisites

* **Python:** `>= 3.10`

---

## 1. Setup & Installation

### 1.1 Create and Activate a Virtual Environment

Set up an isolated environment:

* **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

* **Windows:**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

### 1.2 Install Dependencies

Install all required packages from `requirements.txt` into the activated environment:

```bash
pip install -r requirements.txt
```

### 1.3 Configure Environment Variables

Create a file named **`.env`** in the project root directory:

```env
LANGSMITH_TRACING=false
OLLAMA_API_KEY=<KEY>
OLLAMA_BASE_URL=<URL>
```

---

## 2. Run the Application

Start the analysis pipeline with the following command:

```bash
python main.py <PATH_TO_JSONL> <LINE_NUMBER> <PATH_TO_APK> [PATH_TO_MD]
```

### Arguments

* `<PATH_TO_JSONL>`: Path to the JSONL dataset file.
* `<LINE_NUMBER>`: Line number to read from the JSONL file (indexing starts at **1**).
* `<PATH_TO_APK>`: Path to your local APK file to be analyzed.
* `[PATH_TO_MD]` *(optional)*: Path to a Markdown file containing manually extracted information and 2 ground truth sets for pipeline validation. Reference examples are located in the `ground_truth/` directory.

### Datasets & Files

* **`dataset/`**: Contains JSON / JSONL files with app metadata and evaluation entries.
* **APK Files**: APK files are **not** tracked in this repository and must be provided locally.
* **`ground_truth/`**: Contains reference Markdown files with manually extracted ground-truth data for evaluation.

### Examples

**Standard execution:**
```bash
python main.py dataset/apps.jsonl 1 /path/to/your_app.apk
```

**With ground truth / validation Markdown file:**
```bash
python main.py dataset/apps.jsonl 1 /path/to/your_app.apk ground_truth/sample_gt.md
```

---

## 3. Output & Results

Every execution generates a dedicated output directory under **`results/`**. It contains:

* **JSON Files:** Intermediate outputs from each pipeline stage and the final evaluation result.
* **Plots & Visualizations:** Evaluation metrics, diagrams, and performance plots.