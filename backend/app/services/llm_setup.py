from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from app.config import OPENAI_API_KEY,GOOGLE_API_KEY,GOOGLE_MODEL

class LLMManager:
    def __init__(self):
        """self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model_name="gpt-4o-mini",
            temperature=0.3
        )"""
        self.llm = ChatGoogleGenerativeAI(
            model=GOOGLE_MODEL, #"gemini-2.0-flash-thinking-exp-01-21", #"gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
        self.prompt_template = ChatPromptTemplate.from_template("""
        You are a knowledgeable assistant skilled in extracting and synthesizing information from diverse document types such as PDFs, Word documents, Excel sheets, and PowerPoint presentations.
        Context:
        {context}
        Question:
        {question}
        Instructions:
        - Use only the information provided in the context to answer the question.
        - Clearly reference or mention the source document type if applicable (e.g., "According to the PDF content..." or "Based on the Excel data...").
        - Provide a clear, concise, and well-reasoned answer.
        - If the context does not contain sufficient information to answer the question, state that explicitly.

        Answer:
        """)

    def generate_response(self, context: str, question: str) -> str:
        formatted_prompt = self.prompt_template.format(
            context=context,
            question=question
        )
        return self.llm.invoke(formatted_prompt).content