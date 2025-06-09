# EduMUSE - AI-Powered Educational Assistant

EduMUSE is a comprehensive AI tutoring system that transforms study materials into personalized learning experiences. The platform combines document processing, knowledge retrieval, and interactive tutoring through a modular multi-agent architecture.

## System Architecture

```
EduMUSE Platform
├── Frontend/              # React document viewer & UI
├── Knowledge_Agent/       # CrewAI multi-agent system
├── file_upload.py        # Flask file handling service
└── uploads/              # Document storage
```

## Features

- 📄 **Smart Document Viewer**: PDF rendering with interactive highlighting using `react-pdf-highlighter`
- 🔍 **Academic Source Discovery**: Multi-modal knowledge retrieval via CrewAI agents
- 🤖 **AI-Powered Analysis**: Text summarization, question generation, and content enhancement
- 📊 **Quality Evaluation**: Systematic assessment of AI outputs
- 🔧 **Modular Architecture**: Extensible agent framework for educational tasks

## Prerequisites

- **Python**: >= 3.10, < 3.13
- **Node.js**: >= 16.x
- **npm**: >= 7.x

## Setup Instructions

### 1. Clone and Navigate

```bash
git clone <your-repo-url>
cd EduMUSE
```

### 2. Environment Configuration

Create a [`.env`](.env) file in the root directory:

```bash
# Copy from the template or create manually
cp .env.example .env
```

Add your API keys to [`.env`](.env):

```bash
MODEL=gpt-4o
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

**Required API Keys:**

- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Serper API Key**: Get from [Serper.dev](https://serper.dev/) for web search functionality

### 3. Backend Setup

#### Install Python Dependencies

```bash
# Install Flask dependencies for file upload service
pip install -r requirements.txt
```

#### Setup CrewAI Knowledge Agent

```bash
cd Knowledge_Agent
crewai install
cd ..
```

### 4. Frontend Setup

```bash
cd Frontend
npm install
cd ..
```

### 5. Create Upload Directory

```bash
mkdir -p uploads
```

## Running EduMUSE

### Start All Services

You'll need **3 terminal windows** to run the complete system:

#### Terminal 1: File Upload Service

```bash
# Start Flask file upload server (runs on port 5000)
python file_upload.py
```

#### Terminal 2: CrewAI Knowledge Agent

```bash
cd Knowledge_Agent
python src/edumuse/main.py
```

#### Terminal 3: Frontend Development Server

```bash
cd Frontend
npm run dev
# Typically runs on http://localhost:5173
```

### Verify Setup

1. **File Upload Service**: Visit `http://localhost:5000/health` - should return `{"status": "healthy"}`
2. **Frontend**: Visit `http://localhost:5173` - should load the document viewer
3. **Upload Test**: Try uploading a PDF through the frontend interface

## Usage Workflow

1. **Upload Documents**: Use the frontend to upload PDF study materials
2. **View & Interact**: Navigate documents with the interactive PDF viewer
3. **Select Text**: Highlight text sections you want to analyze
4. **AI Processing**: Click action buttons (Summarize, Search, Quiz Me) to trigger AI analysis
5. **Review Results**: View AI-generated summaries, sources, or questions in the results panel

## Project Structure

```
EduMUSE/
├── Frontend/                 # React document viewer
│   ├── src/                 # React components
│   ├── package.json         # Node dependencies
│   └── README.md           # Frontend documentation
├── Knowledge_Agent/         # CrewAI AI agents
│   ├── src/edumuse/        # Main agent implementation
│   ├── test_*.py           # Testing frameworks
│   └── README.md           # Agent documentation
├── file_upload.py          # Flask upload service
├── uploads/                # Document storage
├── requirements.txt        # Python dependencies
├── .env                   # API keys (create this)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## API Endpoints

### File Upload Service (Port 5000)

- **POST** `/upload` - Upload PDF documents
- **GET** `/files` - List uploaded files
- **GET** `/files/<filename>` - Serve specific file
- **GET** `/health` - Health check

### CrewAI Agent Integration (Future)

- **POST** `/agents/summarize` - Text summarization
- **POST** `/agents/search` - Academic source discovery
- **POST** `/agents/quiz` - Question generation

## Development Features

### Knowledge Agent Capabilities

- **Web Search Flow**: Real-time academic source discovery using SerperDev
- **LLM Knowledge Flow**: Knowledge synthesis from training data
- **Hybrid Retrieval**: Combined approach for comprehensive coverage
- **Evaluation Framework**: Quality assessment with performance metrics

### Frontend Features

- **PDF Rendering**: Interactive document viewer with highlighting
- **Text Selection**: Highlight and interact with document content
- **Action Buttons**: Trigger AI analysis on selected text
- **File Management**: Upload and switch between documents
- **CORS Support**: Configured for local development

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure all services are running on correct ports (Frontend: 5173, Flask: 5000)
2. **File Upload Fails**: Check that `uploads/` directory exists and has write permissions
3. **API Key Errors**: Verify [`.env`](.env) file exists and contains valid API keys
4. **CrewAI Installation**: Ensure Python version is between 3.10 and 3.13

### Port Configuration

- **Frontend**: `http://localhost:5173` (Vite default)
- **File Upload**: `http://localhost:5000` (Flask)
- **Alternative Frontend**: `http://localhost:3000` (if using Create React App)

### Logs

- **Flask Logs**: Check terminal running [`file_upload.py`](file_upload.py)
- **CrewAI Logs**: Check terminal running Knowledge Agent
- **Frontend Logs**: Check browser console and Vite terminal

## Development Roadmap

### Current Status ✅

- File upload and storage system working
- Knowledge retrieval agent with evaluation framework
- Basic frontend structure implemented
- PDF document viewer functional

### In Progress 🔄

- Frontend-backend integration for AI processing
- Text selection → AI agent pipeline
- Results display in frontend

### Planned 📋

- Quiz generation agent
- Summary and explanation agent
- Audio content generation (TTS)
- Advanced document formats (DOCX support)
- Cloud storage integration

## Contributing

1. Fork the repository
2. Create feature branches for new components
3. Follow the modular architecture patterns
4. Add comprehensive testing for new features
5. Update documentation for new components

## Tech Stack

- **Frontend**: React, react-pdf-highlighter, Vite
- **Backend**: Flask (file handling), CrewAI (AI agents)
- **AI Models**: GPT-4o via OpenAI API
- **Search**: SerperDev API for academic sources
- **Storage**: Local filesystem (cloud migration planned)

## License

MIT License - see [`LICENSE`](LICENSE) for details.

---

_EduMUSE: Transforming study materials into personalized AI-powered learning experiences_

## Quick Start Summary

```bash
# 1. Setup environment
cp .env.example .env  # Add your API keys

# 2. Install dependencies
pip install -r requirements.txt
cd Knowledge_Agent && crewai install && cd ..
cd Frontend && npm install && cd ..

# 3. Run services (3 terminals)
python file_upload.py                    # Terminal 1
cd Knowledge_Agent && python src/edumuse/main.py  # Terminal 2
cd Frontend && npm run dev               # Terminal 3

# 4. Open http://localhost:5173 and start learning!
```
