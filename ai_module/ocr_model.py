import streamlit as st
from google.cloud import vision
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import tempfile

st.set_page_config(page_title="📷 Google AI OCR + Gemini", layout="wide")
st.title("📄 Google Vision OCR + Gemini Summary")

input_method = st.radio("Choose input method", ["Upload Image", "Camera"])
summarize = st.checkbox("Summarize extracted text with Gemini", value=True)

# --- OCR Function ---
def run_google_ocr(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ""

# --- Handle Input ---
image_path = None
if input_method == "Upload Image":
    uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.read())
            image_path = tmp_file.name
        st.image(image_path, caption="Uploaded Image", use_column_width=True)

elif input_method == "Camera":
    camera_image = st.camera_input("Take a photo")
    if camera_image:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(camera_image.read())
            image_path = tmp_file.name
        st.image(image_path, caption="Captured Image", use_column_width=True)

# --- OCR + Display ---
if image_path:
    st.subheader("🔍 Extracted Text")
    with st.spinner("Running OCR..."):
        extracted_text = run_google_ocr(image_path)
    st.text_area("Text from Image", value=extracted_text, height=300)

    # --- Gemini Summarization ---
    if summarize and extracted_text.strip():
        st.subheader("💬 Gemini Summary")

        prompt = PromptTemplate(
            input_variables=["content"],
            template="Summarize the following OCR-extracted text:\n\n{content}\n\nSummary:"
        )

        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        chain = LLMChain(prompt=prompt, llm=llm)

        with st.spinner("Using Gemini to summarize..."):
            summary = chain.run(content=extracted_text[:8000])  # avoid token overflow
            st.success("Summary complete.")
            st.write(summary)
