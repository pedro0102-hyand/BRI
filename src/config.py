from pathlib import Path

# Define the base directory and other relevant paths for the project
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

# Define paths for the PAN plagiarism corpus and its subdirectories
CORPUS_DIR = DATA_DIR / "pan-plagiarism-corpus-2011"
EXTERNAL_DIR = CORPUS_DIR / "external-detection-corpus"
SOURCE_DIR = EXTERNAL_DIR / "source-document"
SUSPICIOUS_DIR = EXTERNAL_DIR / "suspicious-document"

# Define paths for the JSON files containing paper data
PAPERS_JSON = CORPUS_DIR / "papers.json"