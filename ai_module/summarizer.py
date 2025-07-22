import os
import getpass
from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from google import genai

client = genai.Client()

template_prompt = """
You are a AI summarizer who helps teachers for summarizing the lessons and long context and give meaningful summaries which can be understandable by students
You should also understand other languages and try to summarize them and dont give Here is the prefixes
Please summarize this context
-----
{content}
-----


"""
prompt = template_prompt.format(content = """LangChain provides several methods to build a text summarizer using Google's Gemini Flash model. One approach is to use the create_stuff_documents_chain which allows summarizing text in a single LLM call.
This method is suitable for models with larger context windows, such as Gemini-2.0-Flash. The process involves loading a chat model, preparing the documents, and then using a prompt to generate a summary.

Another approach is to use the load_summarize_chain function, which can be configured with different chain types such as "stuff", "map_reduce", or "refine".
 For instance, the "stuff" chain type is useful when the context window of the model is large enough to handle the entire document.

Additionally, LangChain supports parallelization through map-reduce workflows, which can be effective for larger volumes of text.
 This method involves mapping each document to an individual summary and then reducing those summaries into a single global summary.

For a practical implementation, you can use the GoogleGenerativeAI model from the langchain-google-genai package to load the Gemini-1.5-flash model and create a summarization chain.
 This involves defining a prompt, instantiating the chain, and then invoking it with the document content."""
                                )
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

print(response.text)