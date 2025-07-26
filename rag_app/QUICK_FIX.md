# 🚀 Quick Fix: Project ID and Authentication Issues

## Problem
You're getting "Permission denied on resource project your-gcp-project-id" because the application is using a placeholder project ID instead of your actual Google Cloud project ID.

## ✅ Solution Steps

### Step 1: Find Your Project ID
```bash
# Check your current project
gcloud config get-value project

# If no project is set, list available projects
gcloud projects list
```

### Step 2: Set Your Project ID
```bash
# Set your project ID (replace with your actual project ID)
gcloud config set project YOUR-ACTUAL-PROJECT-ID
```

### Step 3: Authenticate
```bash
# Login to Google Cloud
gcloud auth application-default login
```

### Step 4: Enable APIs
```bash
# Enable required APIs
gcloud services enable vision.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### Step 5: Create Environment File
Create a `.env` file in the `rag_app` directory:
```
GOOGLE_CLOUD_PROJECT=YOUR-ACTUAL-PROJECT-ID
```

### Step 6: Run Setup Script (Recommended)
```bash
cd rag_app
python setup_project.py
```

This script will:
- ✅ Check your authentication
- ✅ Set your project ID
- ✅ Create the .env file
- ✅ Enable required APIs
- ✅ Test the connection

## 🔧 Alternative Methods

### Method 1: Environment Variable
```bash
# Windows
set GOOGLE_CLOUD_PROJECT=YOUR-ACTUAL-PROJECT-ID

# Linux/Mac
export GOOGLE_CLOUD_PROJECT=YOUR-ACTUAL-PROJECT-ID
```

### Method 2: Direct in Code
Edit `main_alternative.py` and change:
```python
PROJECT_ID = "YOUR-ACTUAL-PROJECT-ID"  # Replace with your project ID
```

### Method 3: Using gcloud
```bash
# Set project via gcloud
gcloud config set project YOUR-ACTUAL-PROJECT-ID

# Verify it's set
gcloud config get-value project
```

## 🧪 Test Your Setup

Run the test script to verify everything works:
```bash
cd rag_app
python test_embeddings.py
```

## 🚀 Run the Application

Once everything is configured:
```bash
cd rag_app
python quick_start_alternative.py
```

## ❓ Common Issues

### "Project not found"
- Make sure you're using the correct project ID
- Check that you have access to the project
- Verify you're logged in with the right account

### "Permission denied"
- Ensure you have the necessary roles (Editor, Owner, or specific API permissions)
- Check that APIs are enabled for your project

### "Authentication failed"
- Run `gcloud auth application-default login`
- Make sure you're logged in with the correct account

## 📋 Complete Setup Checklist

- [ ] Google Cloud SDK installed
- [ ] Authenticated with `gcloud auth application-default login`
- [ ] Project ID set with `gcloud config set project YOUR-PROJECT-ID`
- [ ] APIs enabled (Vision API, Vertex AI)
- [ ] Environment file created with correct project ID
- [ ] Test script passes
- [ ] Application runs successfully

## 🎯 Quick Commands

```bash
# Complete setup in one go
cd rag_app
python setup_project.py
python test_embeddings.py
python quick_start_alternative.py
```

---

**Need help?** The setup script will guide you through the entire process automatically! 