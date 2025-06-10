from typing import Any, Dict
from agents.agents import (
    InputDetectionAgent,
    SpeechToTextAgent,
    ContentAcquisitionAgent,
    QueryUnderstandingAgent,
    RetrievalAgent,
    AnswerGenerationAgent,
    VerificationAgent,
    VisualGenerationAgent,
    FormattingAgent,
    TTSAgent,
)
# from agents.tts_agent import TTSAgent

class MultiAgentOrchestrator:
    """
    Orchestrates the flow through all agents.
    """
    def __init__(self):
        print("Initializing MultiAgentOrchestrator...")
        self.input_detector = InputDetectionAgent()
        self.content_agent = ContentAcquisitionAgent()
        self.tts_agent = TTSAgent()
        print("Orchestrator initialized successfully")

    def run(self, user_input: Any, request_tts: bool = False) -> Dict[str, Any]:
        print("\n=== Starting Pipeline ===")
        print(f"Input: {user_input}")
        print(f"TTS requested: {request_tts}")

        # Initialize context with user input
        context: Dict[str, Any] = {
            "user_input": user_input,
            "request_tts": request_tts,
        }

        # Detect input type
        print("\n=== Detecting Input Type ===")
        context = self.input_detector(context)
        print(f"Detected input type: {context['input_descriptor']['type']}")
        
        # Get content from PDF
        print("\n=== Acquiring Content ===")
        context = self.content_agent(context)
        if context.get("fetched_content"):
            print("Content successfully fetched")
            print(f"Content length: {len(context['fetched_content'])} characters")
        else:
            print("WARNING: No content was fetched!")

        # Generate podcast and audio
        if request_tts:
            print("\n=== Generating Podcast ===")
            context = self.tts_agent(context)
            if context.get("audio_output"):
                print("Audio generation completed successfully")
            else:
                print("WARNING: Audio generation failed!")

        print("\n=== Pipeline Complete ===")
        return context
