# test_backend.py
import io
import os
import shutil
import pytest

from fastapi.testclient import TestClient
from app.main import app  # Assuming your FastAPI app is created in app/main.py
from app.config import DOCUMENT_PATH, MAX_FILE_SIZE
from app.services.document_processor import DocumentProcessor

client = TestClient(app)

# Ensure a clean documents directory before and after tests
@pytest.fixture(autouse=True)
def cleanup_documents_dir():
    if DOCUMENT_PATH.exists():
        shutil.rmtree(DOCUMENT_PATH)
    DOCUMENT_PATH.mkdir(parents=True, exist_ok=True)
    yield
    if DOCUMENT_PATH.exists():
        shutil.rmtree(DOCUMENT_PATH)

# Patch DocumentProcessor methods to avoid processing real files
@pytest.fixture(autouse=True)
def patch_document_processor(monkeypatch):
    monkeypatch.setattr(DocumentProcessor, "extract_text", lambda file_path, filename: "dummy text")
    monkeypatch.setattr(DocumentProcessor, "chunk_text", lambda text, chunk_size=3500: ["dummy chunk"])

def test_upload_valid_file():
    """
    Test uploading a valid PDF file (supported type and size).
    """
    file_content = b"%PDF-1.4 dummy pdf content"
    response = client.post(
        "/documents/upload",
        files={
            "file": ("test.pdf", io.BytesIO(file_content), "application/pdf")
        }
    )
    assert response.status_code == 200, response.text
    json_data = response.json()
    assert "processed successfully" in json_data["message"]

def test_upload_unsupported_file_type():
    """
    Test uploading a file with an unsupported content type.
    """
    file_content = b"print('Hello World')"
    response = client.post(
        "/documents/upload",
        files={
            "file": ("test.py", io.BytesIO(file_content), "text/x-python")
        }
    )
    # Expecting 415 Unsupported Media Type error
    assert response.status_code == 415, response.text
    json_data = response.json()
    assert json_data["detail"] == "Unsupported file type"

def test_upload_file_too_large():
    """
    Test uploading a file that exceeds the maximum allowed size.
    """
    file_content = b"a" * (MAX_FILE_SIZE + 1)
    response = client.post(
        "/documents/upload",
        files={
            "file": ("large.pdf", io.BytesIO(file_content), "application/pdf")
        }
    )
    # Expecting 413 Payload Too Large error
    assert response.status_code == 413, response.text
    json_data = response.json()
    assert json_data["detail"] == "File size exceeds 2MB limit"

def test_get_files_empty():
    """
    Test GET /documents/getfile returns an empty list when no files are uploaded.
    """
    response = client.get("/documents/getfile")
    assert response.status_code == 200, response.text
    json_data = response.json()
    assert json_data["files"] == []

def test_get_files_after_upload():
    """
    Test that after uploading a file, GET /documents/getfile returns the filename.
    """
    file_content = b"%PDF-1.4 dummy pdf content"
    filename = "test_get.pdf"
    upload_response = client.post(
        "/documents/upload",
        files={
            "file": (filename, io.BytesIO(file_content), "application/pdf")
        }
    )
    assert upload_response.status_code == 200, upload_response.text

    response = client.get("/documents/getfile")
    assert response.status_code == 200, response.text
    json_data = response.json()
    assert filename in json_data["files"]

def test_delete_file_not_found():
    """
    Test DELETE /documents/{filename} returns a 404 error when the file does not exist.
    """
    response = client.delete("/documents/nonexistent.pdf")
    # We expect a 404 Not Found error rather than a 500 error.
    assert response.status_code == 404, response.text
    json_data = response.json()
    assert json_data["detail"] == "File not found"

def test_delete_file_success():
    """
    Test that a file can be successfully deleted.
    """
    file_content = b"%PDF-1.4 dummy pdf content"
    filename = "test_delete.pdf"
    # Upload the file first
    upload_response = client.post(
        "/documents/upload",
        files={
            "file": (filename, io.BytesIO(file_content), "application/pdf")
        }
    )
    assert upload_response.status_code == 200, upload_response.text

    # Now delete the file
    delete_response = client.delete(f"/documents/{filename}")
    assert delete_response.status_code == 200, delete_response.text
    json_data = delete_response.json()
    assert f"File {filename} deleted successfully" in json_data["message"]

def test_chat_endpoint(monkeypatch):
    """
    Test the /chat/ endpoint by overriding the LLMManager.generate_response
    to return a fixed string.
    """
    from app.routers.chat import llm_manager

    def fake_generate_response(context, user_message):
        return "Fake response from LLM."

    monkeypatch.setattr(llm_manager, "generate_response", fake_generate_response)

    response = client.post("/chat/", json={"user_message": "What is the status?"})
    assert response.status_code == 200, response.text
    json_data = response.json()
    assert json_data["response"] == "Fake response from LLM."
