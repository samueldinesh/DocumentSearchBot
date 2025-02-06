from fastapi import APIRouter, Body, HTTPException
from app.services.vector_store import VectorStoreManager
from app.services.llm_setup import LLMManager

router = APIRouter(prefix="/chat", tags=["chat"])
vector_manager = VectorStoreManager()
llm_manager = LLMManager()

@router.post("/")
async def chat_with_bot(user_message: str = Body(..., embed=True)):
    try:
        # Retrieve relevant context
        if vector_manager.retriever is None:
            context = "No documents have been uploaded yet."
        else:
            retrieved_docs = vector_manager.retriever.invoke(user_message)
            context = "\n".join([doc.page_content for doc in retrieved_docs[:3]])
        
        # Generate AI response
        response = llm_manager.generate_response(context, user_message)
        
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )