# FinEduGuide - AI-Powered Financial Education Assistant 🎓

An open-source, AI-powered platform that transforms financial education content into personalized learning experiences. Users can upload banking/finance documents or input topics to receive tailored educational content, quizzes, and explanations powered by advanced RAG (Retrieval-Augmented Generation) technology.

## 📋 Table of Contents
- [Project Description](#project-description)
- [Project Links](#project-links)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [How to Run](#how-to-run)
- [Contributing](#contributing)
- [Author](#author)

## 🎯 Project Description

FinEduGuide is an intelligent educational platform designed for banking and finance learning. It combines the power of:
- **RAG (Retrieval-Augmented Generation)** for context-aware responses
- **Vector Database (Pinecone)** for efficient document storage and retrieval
- **Generative AI** (OpenAI, Llama, Gemini via EuriAI) for content generation
- **FastAPI** backend for robust API services
- **Streamlit** frontend for intuitive user interaction
- **AWS Cloud Infrastructure** for scalable deployment
- **CI/CD Pipeline** with GitHub Actions for automated deployments

**Target Users:**
- Students and educators in banking/finance
- Self-learners interested in financial topics
- Developers exploring AI in education

## 🔗 Project Links

- **📺 Demo Video**: [https://youtu.be/EQjH1oloHyc](https://youtu.be/EQjH1oloHyc)
- **🌐 Live Streamlit App**: [https://fineduguide-ai-assistant.streamlit.app/](https://fineduguide-ai-assistant.streamlit.app/)
- **🚀 FastAPI Swagger Docs**: [http://13.200.38.182:8080/docs](http://13.200.38.182:8080/docs)
- **📁 GitHub Repository**: [https://github.com/vineet416/FinEduGuide-AI-Assistant](https://github.com/vineet416/FinEduGuide-AI-Assistant)

## ✨ Features

- **📄 Document Upload**: Upload PDF and text files containing financial education content
- **🔍 Intelligent Q&A**: Ask questions and receive AI-generated answers based on uploaded documents
- **🧠 RAG-Powered Responses**: Context-aware answers using retrieval-augmented generation
- **💾 Cloud Storage**: Automatic file backup to AWS S3
- **🔢 Vector Embeddings**: Document content stored as embeddings in Pinecone for semantic search
- **🎨 Interactive UI**: User-friendly Streamlit interface for seamless interaction
- **⚡ Fast API Backend**: RESTful API with automatic Swagger documentation
- **🐳 Dockerized**: Containerized application for consistent deployments
- **🔄 CI/CD Pipeline**: Automated deployment using GitHub Actions
- **☁️ AWS Deployment**: Scalable cloud infrastructure with EC2 and ECR

## 🛠️ Technology Stack

### **Backend**
- Python 3.11
- FastAPI (API framework)
- Uvicorn (ASGI server)

### **Frontend**
- Streamlit (Web interface)

### **AI/ML**
- EuriAI (Generative AI API)
- Pinecone (Vector database)
- LangChain (LLM framework)
- PyTorch (ML operations)
- EasyOCR (Text extraction)
- PyMuPDF (PDF processing)

### **Cloud & DevOps**
- AWS EC2 (Compute)
- AWS S3 (Storage)
- AWS ECR (Container registry)
- Docker (Containerization)
- GitHub Actions (CI/CD)

### **Additional Libraries**
- Boto3 (AWS SDK)
- python-dotenv (Environment management)
- python-multipart (File upload handling)

## 📁 Project Structure

```
FinEduGuide/
│
├── main.py                      # FastAPI application entry point
├── streamlit_app.py             # Streamlit frontend application
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup configuration
├── Dockerfile                   # Docker configuration
├── README.md                    # Project documentation
├── LICENSE                      # License file
│
├── data/                        # Data directory
│   └── RBI_SEBI_Finance_Education_Content.txt
│
├── src/                         # Source code
│   ├── __init__.py
│   ├── logger.py                # Logging configuration
│   ├── exception.py             # Custom exception handling
│   │
│   ├── components/              # Core components
│   │   ├── __init__.py
│   │   ├── input_handler.py         # Input processing
│   │   ├── generative_ai.py         # AI model integration
│   │   ├── rag_engine.py            # RAG implementation
│   │   ├── vector_db_client.py      # Pinecone operations
│   │   ├── content_formatter.py     # Content formatting
│   │   └── S3_storage_service.py    # AWS S3 operations
│   │
│   ├── config/                  # Configuration modules
│   │   └── __init__.py
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── process_file_utils.py    # File processing utilities
│       └── prompt_templates.py      # AI prompt templates
│
└── logs/                        # Application logs
```

## 🔌 API Endpoints

The FastAPI backend provides the following endpoints:

### **Base URL**: `http://13.200.38.182:8080`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload-file` | Upload financial education documents (PDF/TXT) |
| POST | `/generate-content` | Generate AI responses based on user queries |
| GET | `/docs` | Interactive API documentation (Swagger UI) |
| GET | `/redoc` | Alternative API documentation (ReDoc) |

**Swagger Documentation**: Visit `/docs` endpoint for interactive API testing

## 🚀 Deployment

### **Production Deployment**

**Backend (FastAPI)**
- **Platform**: AWS EC2 (Ubuntu)
- **Container**: Docker image stored in AWS ECR
- **CI/CD**: GitHub Actions for automated deployments
- **Access**: [http://13.200.38.182:8080](http://13.200.38.182:8080)

**Frontend (Streamlit)**
- **Platform**: Streamlit Cloud
- **Access**: [https://fineduguide-ai-assistant.streamlit.app/](https://fineduguide-ai-assistant.streamlit.app/)

**Infrastructure**
- **Storage**: AWS S3 (Document storage)
- **Vector DB**: Pinecone Cloud
- **CI/CD**: GitHub Actions with self-hosted runner on EC2

## 🚀 How to Run

### Prerequisites
- Python 3.11
- Conda or venv
- AWS Account
- Pinecone Account
- EuriAI API Key

### Local Development Setup

**1. Clone the Repository**
```bash
git clone https://github.com/vineet416/FinEduGuide-AI-Assistant.git
cd FinEduGuide-AI-Assistant
```

**2. Create Virtual Environment**
```bash
conda create -p venv python==3.11 -y
conda activate venv/
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Set Up Pinecone**
- Create account at [https://www.pinecone.io/](https://www.pinecone.io/)
- Create an index named: `fineduguide-index`
- Copy your API key

**5. Set Up EuriAI**
- Get API key from [https://euron.one/euri](https://euron.one/euri)
- Note: This is a paid service

**6. Set Up AWS**
- Login to [AWS Console](https://aws.amazon.com/console/)
- Create IAM user with policies:
  - `AmazonS3FullAccess`
  - `AmazonEC2ContainerRegistryFullAccess`
  - `AmazonEC2FullAccess`
- Generate Access Key and Secret Access Key (CLI)
- Create S3 bucket: `fineduguide-bucket`

**7. Configure Environment Variables**

Create `.env` file in root directory:
```env
EURIAI_API_KEY=your_euriai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
```

**8. Run FastAPI Server**
```bash
uvicorn main:app --reload
```
API will be available at: `http://127.0.0.1:8000`

**9. Configure Streamlit**

Create `.streamlit/secrets.toml`:
```toml
FASTAPI_BASE_URL = "http://127.0.0.1:8000"
```

**10. Run Streamlit App**
```bash
streamlit run streamlit_app.py
```
App will open at: `http://localhost:8501`

**11. Start Using the App**
- Upload financial education documents via Streamlit UI
- Documents are processed and stored in Pinecone (vector embeddings) and AWS S3
- Ask questions in the chatbox to get AI-generated answers

---

### AWS CI/CD Deployment

**1. Create ECR Repository**
- Navigate to AWS ECR console
- Create a new repository
- Save the repository URI

**2. Launch EC2 Instance**
- Instance type: Minimum 8GB RAM, 2 vCPU
- OS: Ubuntu
- Configure security groups (allow ports 8080, 22)

**3. Install Docker on EC2**
```bash
sudo apt-get update -y
sudo apt-get upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

**4. Configure Self-Hosted Runner**
- Go to GitHub repo → Settings → Actions → Runners
- Click "New self-hosted runner"
- Select OS: Linux
- Run provided commands on EC2 instance

**5. Set Up GitHub Secrets**

Add the following secrets in: Settings → Secrets and variables → Actions
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION` (e.g., ap-south-1)
- `ECR_REPO` (your ECR repository name)
- `EURIAI_API_KEY`
- `PINECONE_API_KEY`

**6. Deploy to AWS**
```bash
git add .
git commit -m "Deploy to AWS"
git push origin main
```

**7. Monitor Deployment**
- Check Actions tab in GitHub repository
- Once successful, access FastAPI at: `http://<EC2-PUBLIC-IP>:8080/docs`

**8. Deploy Streamlit to Cloud**
- Go to [Streamlit Cloud](https://streamlit.io/cloud)
- Connect your GitHub repository
- Add secret in Streamlit dashboard:
```toml
FASTAPI_BASE_URL = "http://<EC2-PUBLIC-IP>:8080"
```

🎉 **Congratulations!** Your FinEduGuide AI Assistant is now deployed!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👤 Author

**Vineet Patel**

- 📧 Email: vineetpatel468@gmail.com
- 🐙 GitHub: [@vineet416](https://github.com/vineet416)
- 💼 LinkedIn: [@vineet416](https://linkedin.com/in/vineet416)

---

## 📄 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!