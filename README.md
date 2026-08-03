# Project Setup Instructions

## 1. Environment File

Create a file named **`.env`** in the project directory.

Add the following environment variables with their corresponding keys:

```env
LANGSMITH_TRACING=false
OLLAMA_API_KEY= <KEY>
OLLAMA_BASE_URL= <URL>
```

The `.env` file should be located in the root directory of the project.

---

## 2. Install Dependencies

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

---

## 3. Run the Application

Start the application using the following command:

```bash id="w7w4s2"
python main.py <PATH_TO_JSONL> <LINE_NUMBER> <PATH_TO_APK>
```

Example:

```bash id="m6x2yk"
python main.py scraped_apps/google_one.jsonl 1 /path/to/google_one.apk
```

**Information:**
The `LINE_NUMBER` parameter specifies which line from the JSONL file will be read and analyzed.
The line numbering starts at **1**.

There are already some scraped apps available in the `scraped_apps folder that can be used for testing and analysis.