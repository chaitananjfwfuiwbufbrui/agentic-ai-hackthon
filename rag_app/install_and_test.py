#!/usr/bin/env python3
"""
Installation and Test Script for RAG Application
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_simple.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from google.cloud import vision
        print("✅ Google Cloud Vision imported successfully")
    except ImportError as e:
        print(f"❌ Google Cloud Vision import failed: {e}")
        return False
    
    try:
        import vertexai
        print("✅ Vertex AI imported successfully")
    except ImportError as e:
        print(f"❌ Vertex AI import failed: {e}")
        return False
    
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        print("✅ Scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ Scikit-learn import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    return True

def test_vertex_ai():
    """Test Vertex AI functionality"""
    print("🧠 Testing Vertex AI functionality...")
    
    try:
        import vertexai
        from vertexai.language_models import TextEmbeddingModel
        
        # Test initialization
        vertexai.init(project="test-project", location="us-central1")
        print("✅ Vertex AI initialization successful")
        
        # Test model loading (this will fail without proper credentials, but we can catch the error)
        try:
            model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
            print("✅ Text embedding model loaded successfully")
        except Exception as e:
            print(f"⚠️  Model loading failed (expected without credentials): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Vertex AI test failed: {e}")
        return False

def main():
    """Main installation and test function"""
    print("🚀 RAG Application Installation and Test")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Installation failed")
        return False
    
    # Test imports
    if not test_imports():
        print("❌ Import tests failed")
        return False
    
    # Test Vertex AI
    if not test_vertex_ai():
        print("❌ Vertex AI test failed")
        return False
    
    print("\n🎉 All tests passed!")
    print("\n📋 Next steps:")
    print("1. Set up Google Cloud credentials:")
    print("   gcloud auth application-default login")
    print("2. Set your project ID:")
    print("   gcloud config set project YOUR_PROJECT_ID")
    print("3. Enable required APIs:")
    print("   gcloud services enable vision.googleapis.com")
    print("   gcloud services enable aiplatform.googleapis.com")
    print("4. Run the application:")
    print("   python quick_start_alternative.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 