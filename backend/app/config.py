import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Path configurations
BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENT_PATH = BASE_DIR / "storage"
FAISS_INDEX_PATH = BASE_DIR / "faiss_index"

# Create directories if they don't exist
DOCUMENT_PATH.mkdir(exist_ok=True)
FAISS_INDEX_PATH.mkdir(exist_ok=True)

# App settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
ALLOWED_FILE_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-powerpoint": ".ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx"
}