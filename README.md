# EduMUSE
EduMUSE is an AI-powered tutoring system that turns study materials into personalized sessions with summaries, key terms, practice questions, and audio content. It aims to enhance learning through multimodal, adaptive support tailored to each student’s pace and style.

## Keys
Add these keys in the .env  
OPENAI_API_KEY  
ELEVENLABS_API_KEY  

## Setup
cd multi_agent_pipeline  
source .venv/bin/activate  
pip install -r requirements.txt  
python main.py -i "path/to/pdf/document" --tts  

python main.py -i "../uploads/CrewAI.pdf" --tts
