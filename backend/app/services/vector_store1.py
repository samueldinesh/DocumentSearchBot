import os
import logging
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import FAISS_INDEX_PATH, OPENAI_API_KEY

logger = logging.getLogger(__name__)

class VectorStoreManager:
    _instance = None
    _vectorstore = None
    _retriever = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize_vectorstore()
        return cls._instance

    @classmethod
    def _initialize_vectorstore(cls):
        #embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        try:
            if os.path.exists(FAISS_INDEX_PATH) and any(FAISS_INDEX_PATH.iterdir()):
                cls._vectorstore = FAISS.load_local(
                    FAISS_INDEX_PATH, 
                    embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Loaded existing FAISS index")
            else:
                cls._vectorstore = None
                logger.info("No existing FAISS index found")
        except Exception as e:
            logger.error(f"Error loading FAISS index: {str(e)}")
            cls._vectorstore = None

        if cls._vectorstore:
            cls._retriever = cls._vectorstore.as_retriever()

    def update_index(self, chunks: List[str], metadata: dict):
        try:
            #embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            if self._vectorstore is None:
                print("Make new vector")
                self._vectorstore = FAISS.from_texts(
                    chunks, 
                    embeddings, 
                    metadatas=[metadata]*len(chunks)
                )
            else:
                print("Update vector")
                try:
                    self._vectorstore.add_texts(chunks, metadatas=[metadata]*len(chunks))
                except Exception as e:
                    logger.error(f"Error updating FAISS index: {str(e)}")
                    raise
            print("save local")
            self._vectorstore.save_local(FAISS_INDEX_PATH)
            print("retriver")
            self._retriever = self._vectorstore.as_retriever()
            logger.info("FAISS index updated successfully")
        except Exception as e:
            logger.error(f"Error updating FAISS index: {str(e)}")
            raise

    def clear_index(self):
        try:
            if FAISS_INDEX_PATH.exists():
                for file in FAISS_INDEX_PATH.iterdir():
                    if file.is_file():
                        file.unlink()
                logger.info("Cleared FAISS index files")
            self._vectorstore = None
            self._retriever = None
        except Exception as e:
            logger.error(f"Error clearing FAISS index: {str(e)}")
            raise

    @property
    def retriever(self):
        return self._retriever