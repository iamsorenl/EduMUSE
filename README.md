# EduMUSE - AI-Powered Educational Assistant

EduMUSE is a comprehensive AI tutoring system that transforms study materials into personalized learning experiences. The platform combines document processing, knowledge retrieval, and interactive tutoring through a modular multi-agent architecture.

## System Architecture

```
EduMUSE Platform
├── Frontend/              # React + Vite document viewer with Material-UI
├── edumuse/              # CrewAI multi-agent knowledge system
├── file_upload.py        # Flask file handling service
└── uploads/              # PDF document storage
```

## Features

- 📄 **Interactive PDF Viewer**: Smart document rendering with text selection and highlighting using `react-pdf-highlighter`
- 🔍 **Multi-Modal Knowledge Retrieval**: Web search, LLM synthesis, and hybrid approaches via CrewAI agents
- 🤖 **AI-Powered Analysis**: Text summarization, academic source discovery, and educational content generation
- 📊 **Modular Flow System**: Extensible educational processing flows (quiz, summary, study plans)
- 🎨 **Modern UI**: Material-UI components with responsive design and dark/light themes

## Prerequisites

- **Python**: >= 3.10, < 3.13
- **Node.js**: >= 16.x
- **npm**: >= 7.x

## Quick Start

### 1. Clone and Setup Environment

```bash
git clone <your-repo-url>
cd EduMUSE

# Create environment file (or use existing .env)
touch .env  # if .env doesn't exist
```

### 2. Add API Keys to `.env`

Your `.env` file should contain:

```bash
MODEL=gpt-4o
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

**Required API Keys:**

- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Serper API Key**: Get from [Serper.dev](https://serper.dev/) for web search functionality

### 3. Backend Setup

```bash
# Install Flask dependencies for file upload service
pip install -r requirements.txt

# Setup CrewAI knowledge system
cd edumuse
pip install -e .
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

Start all services in **3 separate terminals**:

### Terminal 1: File Upload Service

```bash
# Start Flask file upload server (port 5000)
python file_upload.py
```

### Terminal 2: CrewAI Knowledge System

```bash
cd edumuse
crewai run
# Alternative: python src/edumuse/main.py
```

### Terminal 3: Frontend Development Server

```bash
cd Frontend
npm run dev
# Opens on http://localhost:5173
```

## Verify Setup

1. **File Upload Service**: Visit `http://localhost:5000/health` → `{"status": "healthy"}`
2. **Frontend**: Visit `http://localhost:5173` → Document viewer loads
3. **Upload Test**: Try uploading a PDF through the interface

## Project Structure

```
EduMUSE/
├── Frontend/                     # React + Vite Application
│   ├── src/
│   │   ├── App.jsx              # Main app with grid layout
│   │   ├── main.jsx             # React entry point
│   │   └── components/          # Modular React components
│   │       ├── Layout/          # Header and layout components
│   │       ├── PDFViewer/       # PDF rendering and interaction
│   │       ├── FileList/        # File management and upload
│   │       └── ResultsPanel/    # AI results display
│   ├── package.json             # Dependencies (React 19, Material-UI, PDF libs)
│   ├── vite.config.js           # Vite configuration
│   └── index.html               # HTML template
├── edumuse/                     # CrewAI Knowledge System
│   ├── src/edumuse/
│   │   ├── main.py              # Entry point for educational flows
│   │   ├── crew.py              # CrewAI coordination
│   │   ├── flows/               # Educational processing flows
│   │   │   ├── flow_registry.py # Flow management system
│   │   │   ├── web_search_flow.py
│   │   │   ├── llm_knowledge_flow.py
│   │   │   └── hybrid_retrieval_flow.py
│   │   ├── config/              # Agent and task configurations
│   │   │   ├── agents.yaml
│   │   │   └── tasks.yaml
│   │   └── tools/               # Custom CrewAI tools
│   ├── test_*.py               # Comprehensive testing framework
│   ├── evaluate_*.py           # Quality evaluation system
│   ├── *.json                  # Evaluation results and data
│   └── pyproject.toml          # CrewAI project configuration
├── file_upload.py              # Flask upload service with CORS
├── uploads/                    # PDF document storage
├── requirements.txt            # Python dependencies (Flask, CORS)
├── .env                       # API keys and configuration
└── README.md                  # This file
```

## Usage Workflow

1. **Start Services**: Run all 3 terminals as shown above
2. **Upload Documents**: Use the file upload panel to add PDF study materials
3. **View & Navigate**: Browse documents with the interactive PDF viewer
4. **Select Text**: Highlight text sections you want to analyze
5. **AI Processing**: Click action buttons (Summarize, Search, Quiz Me)
6. **Review Results**: View AI-generated content in the results panel
7. **Manage Content**: Clear highlights, delete results, switch between documents

## Available Knowledge Flows

### Current Implementation (edumuse/)

- **Web Search Flow**: Real-time academic source discovery using SerperDev API
- **LLM Knowledge Flow**: Knowledge synthesis from training data
- **Hybrid Retrieval Flow**: Combined web + LLM approach for comprehensive coverage

### Planned Educational Flows

- **Quiz Flow**: Generate practice questions and assessments
- **Summary Flow**: Create concept explanations and summaries
- **Study Plan Flow**: Organize learning sequences and roadmaps
- **Citation Flow**: Format academic references and bibliographies

## API Endpoints

### File Upload Service (localhost:5000)

- **POST** `/upload` - Upload PDF documents
- **GET** `/files` - List uploaded files
- **GET** `/files/<filename>` - Serve specific file
- **GET** `/health` - Service health check

### Future CrewAI Integration

- **POST** `/agents/summarize` - Text summarization
- **POST** `/agents/search` - Academic source discovery
- **POST** `/agents/quiz` - Question generation

## Development Features

### Frontend Components

- **Layout**: Header navigation and responsive grid system
- **PDFViewer**: Complete PDF rendering with `react-pdf` and highlighting
- **FileList**: File management with upload and selection
- **ResultsPanel**: AI results display with individual result management
- **Material-UI Integration**: Modern design with theming support

### Backend Capabilities

- **Flask CORS**: Configured for frontend communication
- **CrewAI Flows**: Modular educational processing system
- **Evaluation Framework**: Comprehensive quality assessment
- **Performance Metrics**: Response time and quality tracking

## Tech Stack

- **Frontend**: React 19, Vite, Material-UI, react-pdf-highlighter
- **Backend**: Flask (file handling), CrewAI (AI agents)
- **AI Models**: GPT-4o via OpenAI API
- **Search**: SerperDev API for academic sources
- **Storage**: Local filesystem with plans for cloud integration

## Testing & Evaluation

The knowledge system includes comprehensive testing:

```bash
cd edumuse

# Test flow registration
python test_flows_registration.py

# Evaluate retrieval quality
python evaluate_retrieval_quality.py

# Test knowledge retrieval comparison
python test_knowledge_retrieval.py
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure Flask (5000) and Vite (5173) are running
2. **File Upload Fails**: Check `uploads/` directory exists and has write permissions
3. **API Key Errors**: Verify `.env` file contains valid OpenAI and Serper keys
4. **PDF Not Loading**: Check file was uploaded successfully via `/files` endpoint
5. **CrewAI Installation**: Ensure Python 3.10-3.13 and run `pip install -e .` in edumuse/

### Port Configuration

- **Frontend (Vite)**: `http://localhost:5173`
- **File Upload (Flask)**: `http://localhost:5000`
- **CrewAI System**: Runs locally, outputs to terminal and files

## Development Roadmap

### Current Status ✅

- Complete React frontend with PDF viewer and Material-UI
- Working Flask file upload service with CORS
- **Functional CrewAI system generating educational content**
- Comprehensive evaluation and testing framework
- **Mock flow implementations ready for real AI integration**

### In Progress 🔄

- Frontend ↔ Backend API integration for AI processing
- Text selection → CrewAI flow pipeline
- Real-time results display from AI agents

### Planned 📋

- Quiz generation and interactive assessments
- Advanced educational content flows
- Audio content generation (TTS)
- Cloud storage and deployment
- User authentication and progress tracking

## Contributing

1. Fork the repository
2. Create feature branches for new components or flows
3. Follow the modular architecture patterns
4. Add comprehensive testing for new features
5. Update documentation for new components

## License

MIT License - see [`LICENSE`](LICENSE) for details.

---

_EduMUSE: Transforming study materials into personalized AI-powered learning experiences_

## Quick Reference

```bash
# Complete setup
pip install -r requirements.txt
cd edumuse && pip install -e . && cd ..
cd Frontend && npm install && cd ..

# Run all services (3 terminals)
python file_upload.py                          # Terminal 1 (Flask)
cd edumuse && python src/edumuse/main.py       # Terminal 2 (CrewAI)
cd Frontend && npm run dev                      # Terminal 3 (React)

# Access application
open http://localhost:5173
```

### Generated Content Examples

Recent CrewAI runs generate structured educational content:

- `educational_content_[timestamp].json` - Complete flow results with metadata
- `quiz_output_[timestamp].md` - Educational quiz content
- `summary_output_[timestamp].md` - Summary and analysis outputs

Example from recent run:

```json
{
  "topic": "machine learning neural networks",
  "educational_content": {
    "quiz": {
      "type": "quiz",
      "content": "Mock quiz output - flow not implemented yet"
    },
    "summary": {
      "type": "summary",
      "content": "Mock summary output - flow not implemented yet"
    }
  },
  "metadata": { "source_count": 1, "flows_executed": ["quiz", "summary"] }
}
```


Curl Commands for file_upload.py:

curl -X POST -H "Content-Type: application/json" \
-d '{"action": "summarize", "filename": "AttentionIsAllYouNeed.pdf"}' \
http://localhost:5000/process

curl -X POST -H "Content-Type: application/json" \
-d '{"action": "assess", "filename": "AttentionIsAllYouNeed.pdf"}' \
http://localhost:5000/process