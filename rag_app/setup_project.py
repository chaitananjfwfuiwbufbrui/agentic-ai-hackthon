#!/usr/bin/env python3
"""
Setup script to configure Google Cloud project and authentication
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

def check_gcloud_auth():
    """Check if gcloud is authenticated"""
    try:
        result = subprocess.run(["gcloud", "auth", "list"], capture_output=True, text=True)
        if "ACTIVE" in result.stdout:
            print("✅ Google Cloud authentication found")
            return True
        else:
            print("❌ Google Cloud authentication not found")
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
            print("❌ No Google Cloud project configured")
            return None
    except FileNotFoundError:
        print("❌ gcloud CLI not found")
        return None

def set_project_id():
    """Set project ID interactively"""
    print("\n🔧 Project Configuration")
    print("=" * 30)
    
    # Get current project
    current_project = check_project_config()
    
    if current_project:
        print(f"Current project: {current_project}")
        change = input("Do you want to change the project? (y/n): ").lower()
        if change != 'y':
            return current_project
    
    # Get new project ID
    while True:
        project_id = input("Enter your Google Cloud project ID: ").strip()
        if project_id:
            try:
                subprocess.run(["gcloud", "config", "set", "project", project_id], check=True)
                print(f"✅ Project set to: {project_id}")
                return project_id
            except subprocess.CalledProcessError:
                print("❌ Failed to set project. Please check your project ID.")
        else:
            print("❌ Project ID cannot be empty.")

def create_env_file(project_id):
    """Create .env file with project configuration"""
    env_content = f"""# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT={project_id}
GOOGLE_APPLICATION_CREDENTIALS=

# Optional: Set specific location
GOOGLE_CLOUD_LOCATION=us-central1
"""
    
    env_file = ".env"
    with open(env_file, "w") as f:
        f.write(env_content)
    print(f"✅ Created {env_file} with project ID: {project_id}")

def enable_apis():
    """Enable required Google Cloud APIs"""
    apis = [
        "vision.googleapis.com",
        "aiplatform.googleapis.com",
        "compute.googleapis.com"
    ]
    
    print("\n🔧 Enabling required APIs...")
    for api in apis:
        try:
            subprocess.run(["gcloud", "services", "enable", api], check=True)
            print(f"✅ Enabled {api}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to enable {api}: {e}")
    
    print("✅ API setup completed")

def test_connection(project_id):
    """Test connection to Google Cloud"""
    print(f"\n🧪 Testing connection to project: {project_id}")
    
    try:
        # Test Vision API
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        print("✅ Vision API connection successful")
        
        # Test Vertex AI
        import vertexai
        vertexai.init(project=project_id, location="us-central1")
        print("✅ Vertex AI connection successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Google Cloud Project Setup")
    print("=" * 40)
    
    # Check authentication
    if not check_gcloud_auth():
        print("\n🔐 Please authenticate with Google Cloud:")
        print("Run: gcloud auth application-default login")
        return False
    
    # Set project ID
    project_id = set_project_id()
    if not project_id:
        print("❌ Failed to set project ID")
        return False
    
    # Create .env file
    create_env_file(project_id)
    
    # Enable APIs
    enable_apis()
    
    # Test connection
    if test_connection(project_id):
        print("\n🎉 Setup completed successfully!")
        print(f"📁 Project ID: {project_id}")
        print("📁 Environment file: .env")
        print("\n🚀 You can now run:")
        print("   python quick_start_alternative.py")
        return True
    else:
        print("\n⚠️  Setup completed with warnings")
        print("Please check your Google Cloud configuration")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 