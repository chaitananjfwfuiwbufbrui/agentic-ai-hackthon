# google_genai_utils.py
from vertex_init import init_vertex_ai
init_vertex_ai()
from langchain_google_genai import ChatGoogleGenerativeAI
from vertexai.generative_models import GenerativeModel

def get_chat_google_generative_ai(model_name="gemini-pro", **kwargs):
    """
    Returns an instance of ChatGoogleGenerativeAI.
    Optionally accepts a model_name and other keyword arguments.
    """
    return ChatGoogleGenerativeAI(model=model_name, **kwargs)

def get_vertexai_generative_model(model_name="gemini-1.5-pro-preview-0409", **kwargs):
    """
    Returns an instance of VertexAI GenerativeModel.
    Optionally accepts a model_name and other keyword arguments.
    """
    return GenerativeModel(model_name, **kwargs)
