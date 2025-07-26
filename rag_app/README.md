# 🧠 OCR + RAG Search Engine (Google Cloud)

A complete Streamlit application that performs the full RAG (Retrieval-Augmented Generation) workflow using Google Cloud services:

1. **Uploads image** (or loads from GCS)
2. **Extracts text** using Google Cloud Vision API
3. **Embeds text** using Vertex AI Embeddings API
4. **Retrieves top matching docs** from a stored embedding database
5. **Sends results + user query** to Gemini for final answer

## 🚀 Features

- **OCR Processing**: Extract text from images using Google Cloud Vision API
- **Vector Search**: FAISS-based similarity search for document retrieval
- **AI Generation**: Gemini-powered answer generation with context
- **Modern UI**: Beautiful Streamlit interface with real-time feedback
- **Demo Mode**: Try sample questions without uploading images
- **Configurable**: Adjustable search parameters and model settings

## 📋 Prerequisites

### 🔧 Google Cloud Setup

1. **Enable Required APIs**:
   ```bash
   gcloud services enable vision.googleapis.com
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable compute.googleapis.com
   ```

2. **Set up Authentication**:
   ```bash
   gcloud auth application-default login
   ```

3. **Set Project ID**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

### 📦 Python Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

## 🏗️ Installation

1. **Clone/Download** the project files
2. **Navigate** to the `rag_app` directory
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   - Update `PROJECT_ID` in `main.py` with your Google Cloud project ID
   - Ensure your Google Cloud credentials are properly set up

## 🚀 Quick Start

### Option 1: Run with Demo Data (Recommended)

1. **Generate demo embeddings**:
   ```bash
   python generate_embeddings.py
   ```

2. **Start the Streamlit app**:
   ```bash
   streamlit run main.py
   ```

3. **Open your browser** to `http://localhost:8501`

### Option 2: Use Custom Data

1. **Create custom text file** (`custom_texts.txt`):
   ```
   Your first text chunk here.
   Your second text chunk here.
   Your third text chunk here.
   ```

2. **Generate embeddings**:
   ```bash
   python generate_embeddings.py
   ```

3. **Run the app**:
   ```bash
   streamlit run main.py
   ```

## 📁 Project Structure

```
rag_app/
├── main.py                    # Main Streamlit application
├── generate_embeddings.py     # Script to create FAISS embeddings
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── embedding_store.faiss     # Generated FAISS index (created by script)
├── embedding_metadata.pkl    # Generated metadata (created by script)
└── custom_texts.txt          # Optional: Custom text chunks
```

## 🎯 Usage Guide

### 1. Document Processing
- **Upload an image** containing text (JPG, PNG, JPEG, BMP, TIFF)
- **Click "Extract Text"** to perform OCR
- **Review extracted text** in the text area

### 2. Question Answering
- **Enter your question** in the sidebar
- **Click "Generate Answer"** to perform RAG search
- **View results** including retrieved documents and AI-generated answer

### 3. Demo Mode
- **Try sample questions** without uploading images
- **Test the system** with predefined knowledge base
- **Understand the workflow** before using your own data

## ⚙️ Configuration

### Environment Variables
Create a `.env` file or set environment variables:
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
```

### Model Settings
Update in `main.py`:
```python
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"
EMBED_MODEL = "textembedding-gecko@001"
GEMINI_MODEL = "gemini-1.5-pro-preview-0409"
```

## 🔧 Advanced Usage

### Custom Embedding Generation

1. **Prepare your text chunks** in `custom_texts.txt`:
   ```
   First text chunk for embedding.
   Second text chunk for embedding.
   Third text chunk for embedding.
   ```

2. **Generate embeddings**:
   ```bash
   python generate_embeddings.py
   ```

3. **The script will automatically**:
   - Load your custom texts
   - Generate embeddings using Vertex AI
   - Create FAISS index
   - Save metadata

### Integration with Google Cloud Storage

To load images from GCS instead of file upload:

```python
# In main.py, modify the image loading section
from google.cloud import storage

def load_image_from_gcs(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        blob.download_to_filename(tmp.name)
        return tmp.name
```

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Errors**:
   ```bash
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **API Not Enabled**:
   ```bash
   gcloud services enable vision.googleapis.com
   gcloud services enable aiplatform.googleapis.com
   ```

3. **Memory Issues with Large Datasets**:
   - Use smaller text chunks
   - Consider using FAISS GPU version
   - Implement batch processing

4. **Rate Limiting**:
   - Implement retry logic
   - Use exponential backoff
   - Monitor API quotas

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance Tips

1. **Text Chunking**: Keep chunks between 100-500 words for optimal retrieval
2. **Batch Processing**: Process multiple documents in batches
3. **Caching**: Cache embeddings for frequently accessed documents
4. **Index Optimization**: Use appropriate FAISS index type for your use case

## 🔒 Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Service Accounts**: Use least-privilege service accounts
3. **Data Privacy**: Ensure compliance with data protection regulations
4. **Access Control**: Implement proper access controls for your application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Cloud Platform for Vision API and Vertex AI
- FAISS for efficient similarity search
- Streamlit for the web interface
- The open-source community for various libraries used

---

**Happy RAG-ing! 🧠✨** 