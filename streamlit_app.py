import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout


# Configuration
FASTAPI_BASE_URL = st.secrets["FASTAPI_BASE_URL"]
REQUEST_TIMEOUT = 300  # seconds

# Upload File helper function
def upload_file_to_api(file, pdf_processing_method=None):
    files = {"file": (file.name, file, file.type)}
    data = {}
    if pdf_processing_method:
        data["pdf_processing_method"] = pdf_processing_method.lower()
    return requests.post(f"{FASTAPI_BASE_URL}/upload-file", files=files, data=data, timeout=REQUEST_TIMEOUT)

# Generate Content helper function
def generate_content_from_api(user_query, task_type):
    return requests.post(
        f"{FASTAPI_BASE_URL}/generate-content",
        data={"user_query": user_query, "task_type": task_type.lower()}, timeout=REQUEST_TIMEOUT)


# Page UI
st.set_page_config(page_title="FinEduGuide", layout="centered")
st.markdown("<h1 style='text-align: center;'>🏦 FinEduGuide</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Banking Education Content Generator</h3>", unsafe_allow_html=True)

# Sidebar – Upload Section
st.sidebar.title("Settings")
st.sidebar.header("Upload Document")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "txt"])

pdf_processing_method = None
if uploaded_file and uploaded_file.type == "application/pdf":
    pdf_processing_method = st.sidebar.selectbox(
        "PDF Processing Method", 
        ("Standard Text Extraction", "OCR based Extraction")
        )

if st.sidebar.button("Upload & Process"):
    if not uploaded_file:
        st.sidebar.error("Please upload a file first")
    else:
        try:
            with st.spinner("Uploading & processing file..."):
                response = upload_file_to_api(
                    uploaded_file,
                    pdf_processing_method
                )
            if response.status_code == 200:
                st.sidebar.success("File uploaded & processed successfully")
                st.session_state["file_uploaded"] = True
            else:
                st.sidebar.error(response.json().get("error", "Upload failed"))
        except (ConnectionError, Timeout):
            st.sidebar.error("FastAPI server is not running. Start it using uvicorn." )

# Content Generation Section
content_type = st.selectbox("Select Content Type", ("Explain", "Quiz", "Summary"))

user_query = st.chat_input("Type your query or topic here...")

if user_query:
    st.chat_message("user").markdown(user_query)
    try:
        with st.chat_message("assistant"):
            with st.spinner("Generating content..."):
                response = generate_content_from_api(user_query=user_query, task_type=content_type)

            # Display generated content and download button
            if response.status_code == 200:
                generated_content = response.json()
                st.markdown(generated_content)
                st.download_button("Download Content", data=str(generated_content), file_name="generated_content.txt")
            else:
                st.error(response.json().get("error", "Failed to generate content"))
    except (ConnectionError, Timeout):
        st.error("FastAPI server is not reachable. Make sure it is running.")