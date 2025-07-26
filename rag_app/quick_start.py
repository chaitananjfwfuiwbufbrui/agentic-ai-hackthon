#!/usr/bin/env python3
"""
Quick Start Script for OCR + RAG Search Engine
Provides an easy way to run the application with minimal setup
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if main files exist
    required_files = ["main.py", "requirements.txt"]
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Missing required file: {file}")
            return False
    
    # Check if embeddings exist
    if not Path("embedding_store.faiss").exists():
        print("⚠️  No embedding store found. Will create demo embeddings...")
        return "create_embeddings"
    
    print("✅ All requirements met")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_demo_embeddings():
    """Create demo embeddings"""
    print("🧠 Creating demo embeddings...")
    try:
        subprocess.check_call([sys.executable, "generate_embeddings.py"])
        print("✅ Demo embeddings created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create embeddings: {e}")
        return False

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting Streamlit application...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")

def main():
    """Main quick start function"""
    print("🧠 OCR + RAG Search Engine - Quick Start")
    print("=" * 50)
    
    # Check requirements
    status = check_requirements()
    if status is False:
        print("❌ Cannot proceed due to missing requirements")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Create embeddings if needed
    if status == "create_embeddings":
        if not create_demo_embeddings():
            print("❌ Failed to create demo embeddings")
            return False
    
    # Run the application
    run_streamlit()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 