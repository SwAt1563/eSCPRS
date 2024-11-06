# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from .config import settings





# support await for chat
def get_ollama_chat(temperature: float = 0.7):
    chat_ollama = ChatOllama(
        model=settings.LLM_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        num_ctx=settings.LLM_MODEL_CTX,
        num_predict=settings.LLM_MODEL_PREDICT,
        temperature=temperature
    )
    return chat_ollama
