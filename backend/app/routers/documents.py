from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStoreManager
from app.config import DOCUMENT_PATH,ALLOWED_FILE_TYPES
import shutil
import os

router = APIRouter(prefix="/documents", tags=["documents"])
vector_manager = VectorStoreManager()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # File validation
        if file.content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                              detail="Unsupported file type")
        
        # Save file
        file_path = DOCUMENT_PATH / file.filename
        with file_path.open("wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document
        text = DocumentProcessor.extract_text(str(file_path), file.filename)
        chunks = DocumentProcessor.chunk_text(text)
        
        # Update vector store
        vector_manager.update_index(chunks, {"filename": file.filename})
        
        return {"message": f"File {file.filename} processed successfully"}
    
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail=str(e))

@router.get("/getfile")  # Add this endpoint
async def get_files():
    try:
        if not DOCUMENT_PATH.exists():
            return {"files": []}
        
        files = [f for f in os.listdir(DOCUMENT_PATH) if os.path.isfile(os.path.join(DOCUMENT_PATH, f))]
        return {"files": files}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail=str(e))
    
@router.delete("/{filename}")
async def delete_file(filename: str):
    try:
        # Delete file
        print("delete")
        file_path = DOCUMENT_PATH / filename
        if not file_path.exists():
            raise HTTPException(status.HTTP_404_NOT_FOUND, 
                              detail="File not found")
        file_path.unlink()
        print("file exisit")

        # Retrieve remaining files
        remaining_files = [f for f in os.listdir(DOCUMENT_PATH) if os.path.isfile(os.path.join(DOCUMENT_PATH, f))]
        
        # Clear vector store
        vector_manager.clear_index()

        # Remove only the embeddings related to the deleted file
        #vector_manager.remove_from_index({"filename": filename})

        if remaining_files:  # Re-embed if other documents are present
            all_chunks = []
            metadata_list = []
            try:
                for file in remaining_files:
                    file_full_path = DOCUMENT_PATH / file
                    text = DocumentProcessor.extract_text(str(file_full_path), file)
                    chunks = DocumentProcessor.chunk_text(text)
                    vector_manager.update_index(chunks, {"filename": file})
            except Exception as e:
                print(e)
                #all_chunks.extend(chunks)
                #metadata_list.extend([{"filename": file}] * len(chunks))
            
            #vector_manager.update_index(all_chunks, metadata_list)
        
        return {"message": f"File {filename} deleted successfully and embeddings updated"}

    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail=str(e))