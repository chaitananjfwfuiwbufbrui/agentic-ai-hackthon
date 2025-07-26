import streamlit as st
from google.cloud import vision, aiplatform
import tempfile
import os
import faiss
import numpy as np
import pickle
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv('../hack.env')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------- CONFIG --------
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
LOCATION = "us-central1"
EMBED_MODEL = "textembedding-gecko@001"
GEMINI_MODEL = "gemini-1.5-pro-preview-0409"

# Initialize Vertex AI
try:
    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    logger.info("Vertex AI initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Vertex AI: {e}")
    st.error(f"Failed to initialize Vertex AI: {e}")

# -------- OCR FUNCTION --------
def extract_text_from_image(image_path):
    """Extract text from image using Google Cloud Vision API"""
    try:
        client = vision.ImageAnnotatorClient()
        
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)

        if response.error.message:
            raise Exception(f'OCR Error: {response.error.message}')

        texts = response.text_annotations
        extracted_text = texts[0].description if texts else ""
        
        logger.info(f"Successfully extracted {len(extracted_text)} characters from image")
        return extracted_text
        
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        raise e

# -------- EMBEDDING FUNCTION --------
def get_embedding(text):
    """Generate embeddings using Vertex AI"""
    try:
        model = aiplatform.TextEmbeddingModel.from_pretrained(EMBED_MODEL)
        embedding = model.get_embeddings([text])[0].values
        return np.array(embedding, dtype=np.float32)
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise e

# -------- FAISS FUNCTIONS --------
def load_faiss_index():
    """Load pre-computed FAISS index and metadata"""
    try:
        if not os.path.exists("embedding_store.faiss"):
            # Create a simple demo index if none exists
            create_demo_index()
        
        index = faiss.read_index("embedding_store.faiss")
        with open("embedding_metadata.pkl", "rb") as f:
            metadata = pickle.load(f)
        
        logger.info(f"Loaded FAISS index with {index.ntotal} vectors")
        return index, metadata
        
    except Exception as e:
        logger.error(f"Failed to load FAISS index: {e}")
        raise e

def create_demo_index():
    """Create a demo FAISS index with sample data"""
    try:
        # Sample texts for demo
        texts = [
            "The capital of France is Paris, a beautiful city known for its art and culture.",
            "Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.",
            "Google Cloud Platform provides various services including compute, storage, and AI/ML capabilities.",
            "OCR (Optical Character Recognition) is a technology that converts images of text into machine-readable text.",
            "RAG (Retrieval-Augmented Generation) combines information retrieval with text generation for more accurate responses.",
            "Vertex AI is Google Cloud's unified ML platform for building, deploying, and managing ML models.",
            "Streamlit is a Python library that makes it easy to create web applications for data science and machine learning.",
            "Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language.",
            "Computer vision is a field of AI that trains computers to interpret and understand visual information from the world.",
            "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model complex patterns."
        ]
        
        # Generate embeddings
        embeddings = []
        for text in texts:
            embedding = get_embedding(text)
            embeddings.append(embedding)
        
        # Create FAISS index
        dim = len(embeddings[0])
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings))
        
        # Save index and metadata
        faiss.write_index(index, "embedding_store.faiss")
        with open("embedding_metadata.pkl", "wb") as f:
            pickle.dump(texts, f)
        
        logger.info(f"Created demo FAISS index with {len(texts)} texts")
        
    except Exception as e:
        logger.error(f"Failed to create demo index: {e}")
        raise e

# -------- GEMINI FUNCTION --------
def query_gemini(user_question, retrieved_text, extracted_text=""):
    """Query Gemini with retrieved context and user question"""
    try:
        prompt = f"""
You are a helpful AI assistant. Use the following information to answer the user's question accurately and comprehensively.

Context from Knowledge Base:
{retrieved_text}

Extracted Text from Image (if applicable):
{extracted_text}

User Question: {user_question}

Please provide a clear, accurate answer based on the available information. If the information is not sufficient, please state that clearly.
"""
        
        model = aiplatform.generation_models.ChatModel.from_pretrained(GEMINI_MODEL)
        chat = model.start_chat()
        response = chat.send_message(prompt)
        
        logger.info("Successfully generated response from Gemini")
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini query failed: {e}")
        raise e

# -------- STREAMLIT UI --------
def main():
    st.set_page_config(
        page_title="🧠 OCR + RAG Search Engine",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 OCR + RAG Search Engine (Google Cloud)")
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.info(f"Project ID: {PROJECT_ID}")
        st.info(f"Location: {LOCATION}")
        st.info(f"Embedding Model: {EMBED_MODEL}")
        st.info(f"Gemini Model: {GEMINI_MODEL}")
        
        # File upload
        st.header("📁 Upload Document")
        uploaded_image = st.file_uploader(
            "Upload an image to extract text",
            type=["jpg", "png", "jpeg", "bmp", "tiff"],
            help="Upload an image containing text to extract and search"
        )
        
        # Query input
        st.header("❓ Ask a Question")
        user_query = st.text_area(
            "Enter your question:",
            height=100,
            placeholder="Ask a question based on the document content..."
        )
        
        # Search parameters
        st.header("🔍 Search Settings")
        top_k = st.slider("Number of relevant documents to retrieve", 1, 10, 3)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📄 Document Processing")
        
        if uploaded_image:
            # Display uploaded image
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            
            # Extract text
            if st.button("🔍 Extract Text", type="primary"):
                with st.spinner("🔍 Extracting text with OCR..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                            tmp.write(uploaded_image.read())
                            image_path = tmp.name
                        
                        extracted_text = extract_text_from_image(image_path)
                        
                        # Clean up temp file
                        os.unlink(image_path)
                        
                        st.success("✅ Text extracted successfully!")
                        st.text_area(
                            "📄 Extracted Text",
                            extracted_text,
                            height=200,
                            disabled=True
                        )
                        
                        # Store extracted text in session state
                        st.session_state.extracted_text = extracted_text
                        
                    except Exception as e:
                        st.error(f"❌ OCR extraction failed: {str(e)}")
                        logger.error(f"OCR error: {e}")
        
        # Show extracted text if available
        if hasattr(st.session_state, 'extracted_text'):
            st.text_area(
                "📄 Current Extracted Text",
                st.session_state.extracted_text,
                height=150,
                disabled=True
            )
    
    with col2:
        st.header("🔎 Search & Answer")
        
        if user_query and (uploaded_image or hasattr(st.session_state, 'extracted_text')):
            if st.button("🤖 Generate Answer", type="primary"):
                try:
                    # Get extracted text
                    extracted_text = getattr(st.session_state, 'extracted_text', "")
                    
                    with st.spinner("📐 Generating embedding..."):
                        query_vector = get_embedding(extracted_text if extracted_text else user_query)
                    
                    with st.spinner("🔎 Retrieving relevant documents..."):
                        index, metadata = load_faiss_index()
                        D, I = index.search(query_vector.reshape(1, -1), k=top_k)
                        retrieved_chunks = [metadata[i] for i in I[0]]
                        context = "\n---\n".join(retrieved_chunks)
                    
                    st.success("✅ Retrieved relevant documents!")
                    
                    # Display retrieved context
                    with st.expander("📚 Retrieved Documents", expanded=False):
                        for i, chunk in enumerate(retrieved_chunks, 1):
                            st.markdown(f"**Document {i}:**")
                            st.text(chunk)
                            st.markdown("---")
                    
                    with st.spinner("🤖 Generating answer using Gemini..."):
                        answer = query_gemini(user_query, context, extracted_text)
                    
                    st.success("✅ Answer generated!")
                    
                    # Display answer
                    st.markdown("### 🤖 Answer:")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ Error during processing: {str(e)}")
                    logger.error(f"Processing error: {e}")
        
        elif user_query and not uploaded_image and not hasattr(st.session_state, 'extracted_text'):
            st.warning("⚠️ Please upload an image first to extract text, or use the demo mode below.")
    
    # Demo section
    st.markdown("---")
    st.header("🎯 Demo Mode")
    st.markdown("Try these sample questions with our demo knowledge base:")
    
    demo_questions = [
        "What is the capital of France?",
        "What is machine learning?",
        "What is OCR technology?",
        "What is RAG?",
        "What is Vertex AI?"
    ]
    
    col1, col2, col3 = st.columns(3)
    
    for i, question in enumerate(demo_questions):
        col = col1 if i < 2 else col2 if i < 4 else col3
        if col.button(f"❓ {question}", key=f"demo_{i}"):
            try:
                with st.spinner("🔎 Searching demo knowledge base..."):
                    query_vector = get_embedding(question)
                    index, metadata = load_faiss_index()
                    D, I = index.search(query_vector.reshape(1, -1), k=3)
                    retrieved_chunks = [metadata[i] for i in I[0]]
                    context = "\n---\n".join(retrieved_chunks)
                
                with st.spinner("🤖 Generating answer..."):
                    answer = query_gemini(question, context)
                
                st.success("✅ Demo answer generated!")
                st.markdown(f"**Question:** {question}")
                st.markdown(f"**Answer:** {answer}")
                
            except Exception as e:
                st.error(f"❌ Demo error: {str(e)}")

if __name__ == "__main__":
    main() 