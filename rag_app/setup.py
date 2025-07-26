#!/usr/bin/env python3
"""
Setup Script for OCR + RAG Search Engine
Automates the initial setup and configuration process
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_gcloud_auth():
    """Check if gcloud is authenticated"""
    try:
        result = subprocess.run(["gcloud", "auth", "list"], capture_output=True, text=True)
        if "ACTIVE" in result.stdout:
            print("✅ Google Cloud authentication found")
            return True
        else:
            print("⚠️  Google Cloud authentication not found")
            return False
    except FileNotFoundError:
        print("❌ gcloud CLI not found. Please install Google Cloud SDK")
        return False

def check_project_config():
    """Check and configure Google Cloud project"""
    try:
        result = subprocess.run(["gcloud", "config", "get-value", "project"], capture_output=True, text=True)
        project_id = result.stdout.strip()
        
        if project_id and project_id != "(unset)":
            print(f"✅ Google Cloud Project: {project_id}")
            return project_id
        else:
            print("⚠️  No Google Cloud project configured")
            return None
    except FileNotFoundError:
        print("❌ gcloud CLI not found")
        return None

def enable_apis():
    """Enable required Google Cloud APIs"""
    apis = [
        "vision.googleapis.com",
        "aiplatform.googleapis.com",
        "compute.googleapis.com"
    ]
    
    print("🔧 Enabling required APIs...")
    for api in apis:
        try:
            subprocess.run(["gcloud", "services", "enable", api], check=True)
            print(f"✅ Enabled {api}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to enable {api}: {e}")
    
    print("✅ API setup completed")

def create_env_file():
    """Create .env file with configuration"""
    env_content = """# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id-here
GOOGLE_APPLICATION_CREDENTIALS=

# Optional: Set specific location
GOOGLE_CLOUD_LOCATION=us-central1
"""
    
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("📝 Please update the .env file with your project ID")
    else:
        print("✅ .env file already exists")

def check_files():
    """Check if required files exist"""
    required_files = ["main.py", "generate_embeddings.py", "requirements.txt"]
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files found")
        return True

def run_embedding_generation():
    """Run the embedding generation script"""
    print("🧠 Generating demo embeddings...")
    try:
        subprocess.run([sys.executable, "generate_embeddings.py"], check=True)
        print("✅ Embeddings generated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate embeddings: {e}")
        return False

def main():
    """Main setup function"""
    print("🧠 OCR + RAG Search Engine Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check required files
    if not check_files():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check Google Cloud setup
    gcloud_ok = check_gcloud_auth()
    project_id = check_project_config()
    
    if not gcloud_ok:
        print("\n🔧 Google Cloud Setup Required:")
        print("1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install")
        print("2. Run: gcloud auth application-default login")
        print("3. Run: gcloud config set project YOUR_PROJECT_ID")
        return False
    
    # Enable APIs
    enable_apis()
    
    # Create environment file
    create_env_file()
    
    # Generate embeddings
    if project_id:
        print(f"\n🎯 Ready to generate embeddings for project: {project_id}")
        if input("Generate demo embeddings now? (y/n): ").lower() == 'y':
            if run_embedding_generation():
                print("\n🚀 Setup completed successfully!")
                print("\nNext steps:")
                print("1. Update .env file with your project ID")
                print("2. Run: streamlit run main.py")
                print("3. Open http://localhost:8501 in your browser")
                return True
            else:
                print("❌ Setup completed with warnings")
                return False
        else:
            print("\n✅ Setup completed!")
            print("Run 'python generate_embeddings.py' when ready")
            return True
    else:
        print("\n⚠️  Setup completed with warnings")
        print("Please configure your Google Cloud project:")
        print("gcloud config set project YOUR_PROJECT_ID")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 