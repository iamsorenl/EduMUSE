# EduMUSE: Modular Educational AI Assistant

Welcome to EduMUSE, a modular educational AI assistant powered by [CrewAI](https://crewai.com). This system helps students discover academic sources and generate personalized learning content through pluggable educational flows.

## Features

- **Academic Source Discovery**: Find credible educational resources and research papers
- **Pluggable Learning Flows**: Modular system supporting quizzes, summaries, study plans, and citations
- **Educational Content Generation**: AI-powered content tailored to learning objectives
- **Multi-Agent Coordination**: Specialized agents for discovery and content orchestration

## Installation

Ensure you have Python >=3.10 <3.13 installed. Install dependencies:

```bash
crewai install
```

**Add your API keys to `.env` file:**

```bash
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
```

## Usage

### Run Educational Content Generation

```bash
crewai run
```

### Custom Educational Request

```python
from edumuse.crew import EduMUSE

edumuse = EduMUSE()
result = edumuse.process_educational_request(
    topic="machine learning fundamentals",
    requested_flows=["quiz", "summary"],
    context={"user_level": "intermediate"}
)
```

## Architecture

EduMUSE uses a modular flow architecture:

```
Academic Source Discovery → Educational Flow Orchestration → Learning Content
```

### Available Flows

- **Quiz Flow**: Generate practice questions and assessments
- **Summary Flow**: Create concept explanations and summaries
- **Study Plan Flow**: Organize learning sequences and roadmaps
- **Citation Flow**: Format academic references and bibliographies

## Configuration

- Modify `src/edumuse/config/agents.yaml` to customize agent behaviors
- Modify `src/edumuse/config/tasks.yaml` to adjust task descriptions
- Add new flows in `src/edumuse/flows/` directory

## Educational Focus

EduMUSE is designed specifically for educational use cases:

- Finding credible academic sources
- Supporting student learning objectives
- Creating structured educational content
- Adapting to different learning levels and styles

Let's enhance education through AI! 🎓
