# 🛠️ Troubleshooting Guide

## Common Issues and Solutions

### 1. FAISS Installation Issues (Windows)

**Problem**: `faiss-cpu` fails to install on Windows due to compilation requirements.

**Solutions**:

#### Option A: Use Alternative Version (Recommended)
```bash
# Use the alternative version that uses scikit-learn instead of FAISS
python quick_start_alternative.py
```

#### Option B: Install FAISS via Conda
```bash
# Install Miniconda first, then:
conda install -c conda-forge faiss-cpu
```

#### Option C: Use Pre-compiled Wheels
```bash
# Try installing from a different source
pip install faiss-cpu --index-url https://pypi.org/simple/
```

### 2. Google Cloud Authentication Issues

**Problem**: Authentication errors when accessing Google Cloud services.

**Solutions**:

```bash
# 1. Install Google Cloud SDK
# Download from: https://cloud.google.com/sdk/docs/install

# 2. Authenticate
gcloud auth application-default login

# 3. Set project
gcloud config set project YOUR_PROJECT_ID

# 4. Enable APIs
gcloud services enable vision.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### 3. API Not Enabled Errors

**Problem**: "API not enabled" errors when using Google Cloud services.

**Solutions**:

```bash
# Enable required APIs
gcloud services enable vision.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable compute.googleapis.com
```

### 4. Memory Issues

**Problem**: Out of memory errors when processing large documents.

**Solutions**:

- **Reduce batch size**: Process documents in smaller chunks
- **Use smaller embeddings**: Consider using different embedding models
- **Increase system memory**: Add more RAM to your system
- **Use cloud resources**: Consider running on Google Cloud Compute Engine

### 5. Rate Limiting

**Problem**: API quota exceeded or rate limiting errors.

**Solutions**:

- **Implement retry logic**: Add exponential backoff
- **Monitor quotas**: Check Google Cloud Console for quota usage
- **Request quota increase**: Contact Google Cloud support
- **Use batch processing**: Process multiple items together

### 6. Python Version Issues

**Problem**: Compatibility issues with Python version.

**Solutions**:

```bash
# Check Python version
python --version

# Should be Python 3.8 or higher
# If not, install a newer version from python.org
```

### 7. Dependency Conflicts

**Problem**: Package conflicts during installation.

**Solutions**:

```bash
# Create a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies in clean environment
pip install -r requirements_simple.txt
```

### 8. Streamlit Issues

**Problem**: Streamlit app won't start or has display issues.

**Solutions**:

```bash
# Update Streamlit
pip install --upgrade streamlit

# Clear Streamlit cache
streamlit cache clear

# Run with debug mode
streamlit run main_alternative.py --logger.level debug
```

### 9. File Permission Issues

**Problem**: Cannot read/write files in the application directory.

**Solutions**:

- **Check file permissions**: Ensure read/write access
- **Run as administrator**: On Windows, run command prompt as admin
- **Check antivirus**: Some antivirus software may block file operations

### 10. Network Connectivity Issues

**Problem**: Cannot connect to Google Cloud services.

**Solutions**:

- **Check internet connection**: Ensure stable internet access
- **Check firewall**: Ensure ports are not blocked
- **Use VPN**: If behind corporate firewall
- **Check proxy settings**: Configure proxy if needed

## Quick Fixes

### For FAISS Issues (Windows)
```bash
# Use the alternative version
cd rag_app
python quick_start_alternative.py
```

### For Authentication Issues
```bash
# Re-authenticate
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### For Dependency Issues
```bash
# Clean install
pip uninstall -r requirements_simple.txt -y
pip install -r requirements_simple.txt
```

### For Streamlit Issues
```bash
# Clear cache and restart
streamlit cache clear
streamlit run main_alternative.py
```

## Alternative Setup Methods

### Method 1: Minimal Setup
```bash
# Install only essential packages
pip install streamlit google-cloud-vision google-cloud-aiplatform scikit-learn numpy

# Run alternative version
python main_alternative.py
```

### Method 2: Cloud Setup
```bash
# Use Google Cloud Shell
# All dependencies are pre-installed
git clone <your-repo>
cd rag_app
python quick_start_alternative.py
```

### Method 3: Docker Setup
```dockerfile
# Create Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements_simple.txt .
RUN pip install -r requirements_simple.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "main_alternative.py"]
```

## Getting Help

### 1. Check Logs
```bash
# Enable debug logging
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
```

### 2. Common Error Messages

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'faiss'` | Use alternative version with scikit-learn |
| `Authentication failed` | Run `gcloud auth application-default login` |
| `API not enabled` | Enable APIs with `gcloud services enable` |
| `Out of memory` | Reduce batch size or use cloud resources |
| `Rate limit exceeded` | Implement retry logic or request quota increase |

### 3. Support Resources

- **Google Cloud Documentation**: https://cloud.google.com/docs
- **Streamlit Documentation**: https://docs.streamlit.io
- **Scikit-learn Documentation**: https://scikit-learn.org
- **GitHub Issues**: Check for similar issues in the repository

## Performance Tips

### For Large Datasets
- Use batch processing
- Implement caching
- Consider using cloud resources
- Optimize text chunking

### For Better Accuracy
- Use larger embedding models
- Increase top-k retrieval
- Fine-tune similarity thresholds
- Add more training data

### For Faster Processing
- Use GPU acceleration (if available)
- Implement parallel processing
- Cache embeddings
- Use optimized data structures

---

**Still having issues?** Try the alternative version with scikit-learn, which is much easier to install and use on Windows! 