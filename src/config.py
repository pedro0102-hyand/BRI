from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

CORPUS_DIR = DATA_DIR / "pan-plagiarism-corpus-2011"
EXTERNAL_DIR = CORPUS_DIR / "external-detection-corpus"
SOURCE_DIR = EXTERNAL_DIR / "source-document"
SUSPICIOUS_DIR = EXTERNAL_DIR / "suspicious-document"

PAPERS_JSON = CORPUS_DIR / "papers.json"