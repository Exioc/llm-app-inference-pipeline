# Project Description

This project was developed as part of my bachelor's thesis and consists of a prototype for a modular, LLM-based pipeline. Through a multi-step process, the pipeline analyzes app metadata to systematically infer the required permissions and potential data collection practices of an app.

---

# Setting Up the Project and Running the Pipeline

## Prerequisites

* **Python:** Version `>= 3.10`

## 1. Setup & Installation

### 1.1 Create and Activate a Virtual Environment

It is highly recommended to set up an isolated environment to prevent dependency conflicts. Run the following commands based on your operating system:

* **Linux / macOS:**

  ```
  python3 -m venv .venv
  source .venv/bin/activate
  ```

* **Windows:**

  ```
  python -m venv .venv
  .venv\Scripts\activate
  ```

### 1.2 Install Dependencies

Once the virtual environment is activated, install all required packages from the `requirements.txt` file:

```
pip install -r requirements.txt
```

### 1.3 Configure Environment Variables

In order to send LLM requests to an external Ollama server, the pipeline requires an authentication token and a base URL. Create a file named **`.env`** in the root directory of the project and populate it with your specific credentials:

```
OLLAMA_BASE_URL=<YOUR_API_URL>
AUTH_TOKEN=<YOUR_AUTH_TOKEN>
LANGSMITH_TRACING=false
```

**Note:** The environment variable `LANGSMITH_TRACING=false` is listed here because it was used for debugging purposes during development and must be included in the file.

## 2. Run the Application

To run the pipeline, use the following command:

```bash
python main.py <PATH_TO_JSONL> <LINE_NUMBER> <PATH_TO_APK> [PATH_TO_MD]
```

### Arguments

* `<PATH_TO_JSONL>`: The file path to the JSONL dataset containing the app metadata to be analyzed.

* `<LINE_NUMBER>`: The specific line number to read from the JSONL file (Note: indexing starts at **1**).

* `<PATH_TO_APK>`: The local file path to the APK file you intend to analyze.

* `[PATH_TO_MD]` *(optional)*: The path to a Markdown file containing two reference records consisting of permissions and formatted as JSON.

### Execution Examples

```
python main.py dataset/alarm_clock.jsonl 1 /desk/apks/alarm_clock.apk /ground_truth/alarm_clock.md

```

## 3. Output & Results

For each run, a dedicated subfolder is created within the results/ directory. This folder contains:

* **JSON Files:** Input data, intermediate outputs from each pipeline stage, and the final results.

* **Visualizations:** Generated plots for simple presentation of the results.

---

# Additional Data and Information

## Data for Testing 

To run the pipeline, you can use a JSONL file from the `dataset/` folder and an MD file from the `ground_truth/`   folder. Note that you must provide the APK file yourself.

## evalulation

* `pipeline_output_test_set`: Contains all pipeline results for the 15 tested apps.

* `pipeline_outputs_waze`: Contains all pipeline results for the 10 runs of the Waze app.

* `sq1_ tabular_comparison`: Contains a tabular mapping for each app, detailing the extracted features used to evaluate Subquestion 1 and make the process traceable.

* `jupyter_notebook_evaluation`: Contains a standalone project consisting of two Jupyter Notebooks, which were used to evaluate and visualize the pipeline results.