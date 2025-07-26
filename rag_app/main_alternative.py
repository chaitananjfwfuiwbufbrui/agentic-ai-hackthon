import streamlit as st
from google.cloud import vision, aiplatform
import tempfile
import os
import numpy as np
import pickle
from dotenv import load_dotenv
import logging
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load environment variables
try:
    load_dotenv('../.env')
except:
    try:
        load_dotenv('../hack.env')
    except:
        load_dotenv('.env')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------- CONFIG --------
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
LOCATION = "us-central1"
EMBED_MODEL = "textembedding-gecko@001"
GEMINI_MODEL = "gemini-1.5-pro-preview-0409"

# Validate project ID
if PROJECT_ID == "your-gcp-project-id":
    st.error("❌ **Project ID not configured!**")
    st.markdown("""
    **Please set your Google Cloud project ID:**
    
    1. **Set environment variable:**
       ```bash
       set GOOGLE_CLOUD_PROJECT=your-actual-project-id
       ```
       
    2. **Or create a .env file:**
       ```
       GOOGLE_CLOUD_PROJECT=your-actual-project-id
       ```
       
    3. **Or set via gcloud:**
       ```bash
       gcloud config set project your-actual-project-id
       ```
    """)
    st.stop()

# Initialize Vertex AI
try:
    import vertexai
    vertexai.init(project=PROJECT_ID, location=LOCATION)
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
        # Use the correct Vertex AI SDK for text embeddings
        import vertexai
        from vertexai.language_models import TextEmbeddingModel
        
        # Initialize Vertex AI if not already done
        if not hasattr(get_embedding, '_initialized'):
            vertexai.init(project=PROJECT_ID, location=LOCATION)
            get_embedding._initialized = True
        
        # Get the embedding model
        model = TextEmbeddingModel.from_pretrained(EMBED_MODEL)
        
        # Get embeddings
        embeddings = model.get_embeddings([text])
        return np.array(embeddings[0].values, dtype=np.float32)
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        # Fallback: return a simple embedding (for demo purposes)
        logger.warning("Using fallback embedding method")
        return np.random.rand(768).astype(np.float32)  # 768 is typical embedding size

# -------- VECTOR SIMILARITY FUNCTIONS (using scikit-learn) --------
def load_vector_store():
    """Load pre-computed vector store and metadata"""
    try:
        if not os.path.exists("vector_store.pkl"):
            # Create a simple demo store if none exists
            create_demo_store()
        
        with open("vector_store.pkl", "rb") as f:
            store_data = pickle.load(f)
        
        embeddings = store_data['embeddings']
        texts = store_data['texts']
        
        logger.info(f"Loaded vector store with {len(texts)} texts")
        return embeddings, texts
        
    except Exception as e:
        logger.error(f"Failed to load vector store: {e}")
        raise e

def create_demo_store():
    """Create a demo vector store with sample data"""
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
        
        # Save store and metadata
        store_data = {
            'embeddings': np.array(embeddings),
            'texts': texts
        }
        
        with open("vector_store.pkl", "wb") as f:
            pickle.dump(store_data, f)
        
        logger.info(f"Created demo vector store with {len(texts)} texts")
        
    except Exception as e:
        logger.error(f"Failed to create demo store: {e}")
        raise e

def find_similar_documents(query_embedding, embeddings, texts, top_k=3):
    """Find similar documents using cosine similarity"""
    try:
        # Calculate cosine similarity
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Return top-k texts and their similarities
        results = []
        for idx in top_indices:
            results.append({
                'text': texts[idx],
                'similarity': similarities[idx]
            })
        
        return results
        
    except Exception as e:
        logger.error(f"Similarity search failed: {e}")
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
        
        # Use the correct Vertex AI SDK for Gemini
        import vertexai
        from vertexai.generative_models import ChatModel
        
        # Initialize Vertex AI if not already done
        if not hasattr(query_gemini, '_initialized'):
            vertexai.init(project=PROJECT_ID, location=LOCATION)
            query_gemini._initialized = True
        
        model = ChatModel.from_pretrained(GEMINI_MODEL)
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
        page_title="🧠 OCR + RAG Search Engine (Alternative)",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 OCR + RAG Search Engine (Google Cloud) - Alternative Version")
    st.markdown("*Using scikit-learn for vector similarity instead of FAISS*")
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.info(f"Project ID: {PROJECT_ID}")
        st.info(f"Location: {LOCATION}")
        st.info(f"Embedding Model: {EMBED_MODEL}")
        st.info(f"Gemini Model: {GEMINI_MODEL}")
        st.info("Vector Search: scikit-learn (cosine similarity)")
        
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
            st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
            
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
                        embeddings, texts = load_vector_store()
                        results = find_similar_documents(query_vector, embeddings, texts, top_k)
                        retrieved_chunks = [result['text'] for result in results]
                        context = "\n---\n".join(retrieved_chunks)
                    
                    st.success("✅ Retrieved relevant documents!")
                    
                    # Display retrieved context with similarity scores
                    with st.expander("📚 Retrieved Documents", expanded=False):
                        for i, result in enumerate(results, 1):
                            st.markdown(f"**Document {i} (Similarity: {result['similarity']:.3f}):**")
                            st.text(result['text'])
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
                    embeddings, texts = load_vector_store()
                    results = find_similar_documents(query_vector, embeddings, texts, 3)
                    retrieved_chunks = [result['text'] for result in results]
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