#!/usr/bin/env python3
"""
Test script to verify embedding functionality
"""

import os
import numpy as np
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

def test_embedding():
    """Test embedding generation"""
    try:
        # Initialize Vertex AI
        import vertexai
        from vertexai.language_models import TextEmbeddingModel
        
        PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
        LOCATION = "us-central1"
        
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        logger.info("Vertex AI initialized successfully")
        
        # Test embedding generation
        model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
        test_text = "This is a test sentence for embedding generation."
        
        embeddings = model.get_embeddings([test_text])
        embedding_vector = np.array(embeddings[0].values, dtype=np.float32)
        
        logger.info(f"✅ Embedding generation successful!")
        logger.info(f"📊 Embedding shape: {embedding_vector.shape}")
        logger.info(f"📊 Embedding sample values: {embedding_vector[:5]}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Embedding test failed: {e}")
        return False

def test_google_auth():
    """Test Google Cloud authentication"""
    try:
        from google.cloud import vision
        
        # Try to create a client (this will test authentication)
        client = vision.ImageAnnotatorClient()
        logger.info("✅ Google Cloud authentication successful!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Google Cloud authentication failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing RAG Application Components")
    print("=" * 50)
    
    # Test Google Cloud authentication
    print("\n🔐 Testing Google Cloud Authentication...")
    auth_ok = test_google_auth()
    
    # Test embedding generation
    print("\n🧠 Testing Embedding Generation...")
    embedding_ok = test_embedding()
    
    # Summary
    print("\n📊 Test Results:")
    print(f"   Authentication: {'✅ PASS' if auth_ok else '❌ FAIL'}")
    print(f"   Embedding Generation: {'✅ PASS' if embedding_ok else '❌ FAIL'}")
    
    if auth_ok and embedding_ok:
        print("\n🎉 All tests passed! The application should work correctly.")
        print("🚀 You can now run: python quick_start_alternative.py")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
        print("💡 Common solutions:")
        print("   - Run: gcloud auth application-default login")
        print("   - Set project: gcloud config set project YOUR_PROJECT_ID")
        print("   - Enable APIs: gcloud services enable aiplatform.googleapis.com")

if __name__ == "__main__":
    main() 