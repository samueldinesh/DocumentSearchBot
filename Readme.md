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
   git clone https://github.com/samueldinesh/DocumentSearchBot.git
   cd document-search-bot
