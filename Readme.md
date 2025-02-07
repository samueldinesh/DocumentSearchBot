
# Document Search Bot

## Overview

Document Search Bot is a proof-of-concept (POC) AI-powered application that allows users to search through a set of uploaded documents (PDF, DOC/DOCX, Excel, and PowerPoint) by leveraging advanced document processing, embedding, and retrieval techniques. The system supports two types of users:

- **Admin**: Can upload and delete documents.
- **Normal User**: Can query the system for information extracted from the documents.

The bot uses GoogleGenerativeAIEmbeddings (configured for Gemini 2.0) for generating embeddings and ChatGoogleGenerativeAI for generating responses to queries.

## Features

- **Document Upload**: Supports multiple file types (PDF, Word, Excel, PPT) up to 2MB.
- **File Validation**: Checks file type and file size before processing.
- **Document Processing**: Extracts text from various document formats and splits it into manageable chunks.
- **Vector Search**: Uses FAISS as the vector store to index text chunks.
- **AI Chat Interface**: Allows users to ask questions; the system retrieves relevant document excerpts and generates AI-powered responses.
- **Role-Based Access**: Admins can manage documents (upload, view, delete), while both Admins and Normal Users can interact with the chat bot.
- **Frontend UI**: Built with React (using Vite) for a responsive and intuitive user experience.

## Table of Contents

- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Architecture

The application is divided into two main layers:

- **Backend** (FastAPI):
  - Document processing and validation.
  - Embedding generation using GoogleGenerativeAIEmbeddings.
  - Vector store management using FAISS.
  - Chat API using ChatGoogleGenerativeAI for generating responses.
  
- **Frontend** (React with Vite):
  - Login & role-based navigation.
  - Admin dashboard for document management (upload, view, delete).
  - Chat interface for querying documents.
  - Axios for communicating with backend APIs.

## Installation

### Prerequisites

- Python 3.10+
- Node.js 14+
- Git

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/document-search-bot.git
   cd document-search-bot
   ```

2. **Create a virtual environment and install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Environment Variables**:  
   Create a `.env` file in the project root with the following keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   GOOGLE_MODEL=gemini-2.0-flash-thinking-exp-01-21
   GOOGLE_EMBEDDING_MODEL=models/text-embedding-004
   ```

4. **Run the Backend**:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Navigate to the frontend directory** (if separate) or use the provided Vite template:
   ```bash
   cd frontend
   npm install
   ```

2. **Update API Base URL** in `src/api.jsx` if necessary.

3. **Run the Frontend**:
   ```bash
   npm run dev
   ```

## Configuration

The project configuration is managed through `app/config.py` and the `.env` file. Key settings include:

- **Directories**:  
  - `DOCUMENT_PATH`: Directory where uploaded documents are stored.
  - `FAISS_INDEX_PATH`: Directory for persisting the FAISS vector store.

- **API Keys & Models**:
  - `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY`
  - `GOOGLE_MODEL` and `GOOGLE_EMBEDDING_MODEL`

- **File Constraints**:
  - `MAX_FILE_SIZE`: Maximum allowed file size (2MB).
  - `ALLOWED_FILE_TYPES`: Supported MIME types for document uploads.

## Usage

### Backend

- **Upload Document**:  
  POST to `/documents/upload` with a file parameter (multipart/form-data). The API validates the file type and size, processes the document, and updates the FAISS index.

- **Get Files**:  
  GET `/documents/getfile` returns the list of uploaded document filenames.

- **Delete Document**:  
  DELETE `/documents/{filename}` deletes the specified file and updates the embeddings for remaining documents.

- **Chat Query**:  
  POST `/chat` with a JSON body containing `user_message` to receive an AI-generated response based on the uploaded document context.

### Frontend

- **Login**:  
  Users can log in using mock credentials (e.g., Admin: `admin/adminpass`, User: `user/userpass`).

- **Admin Dashboard**:  
  Provides file upload functionality, displays the list of uploaded documents, and allows deletion with confirmation.

- **Chat Interface**:  
  Enables both Admins and Normal Users to query the system and view AI responses.

## API Endpoints

| **Endpoint**               | **Method** | **Description**                                   |
|----------------------------|------------|---------------------------------------------------|
| `/documents/upload`        | POST       | Upload a document (validates type and size).      |
| `/documents/getfile`       | GET        | Retrieve the list of uploaded documents.          |
| `/documents/{filename}`    | DELETE     | Delete a document and update the vector store.    |
| `/chat`                    | POST       | Submit a query; returns AI-generated response.    |

## Testing

Automated tests have been implemented using Pytest and FastAPI's TestClient. To run the tests:

1. **Install Test Dependencies**:
   ```bash
   pip install pytest
   ```

2. **Run the tests**:
   ```bash
   pytest
   ```

The tests cover scenarios for file upload (valid, unsupported types, oversized files), file retrieval, deletion, and the chat endpoint response.

## Future Enhancements

- **Authentication & Authorization**:  
  Implement robust JWT-based authentication for secure access control.
  
- **Granular Vector Store Updates**:  
  Instead of re-embedding on deletion, enhance the vector store to remove only the embeddings associated with the deleted document.
  
- **Scalability & Performance**:  
  Optimize processing for large files and high query loads using asynchronous processing and caching.
  
- **UI/UX Improvements**:  
  Further refine the frontend for a more intuitive and responsive user experience.
  
- **Deployment**:  
  Containerize the application with Docker and deploy on cloud infrastructure.

## License

This project is released under the [MIT License](LICENSE).

---
