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
    TTSAagent,
)
class MultiAgentOrchestrator:
    """
    Orchestrates the flow through all agents.
    """
    def __init__(self):
        # Initialize each agent
        self.input_detector = InputDetectionAgent()
        self.stt_agent = SpeechToTextAgent()
        self.content_agent = ContentAcquisitionAgent()
        self.query_agent = QueryUnderstandingAgent()
        self.retriever = RetrievalAgent()
        self.answer_agent = AnswerGenerationAgent()
        self.verifier = VerificationAgent()
        self.visual_agent = VisualGenerationAgent()
        self.formatter = FormattingAgent()
        self.tts_agent = TTSAagent()

    def run(self, user_input: Any, request_tts: bool = False) -> Dict[str, Any]:
        # Initialize context with user input
        context: Dict[str, Any] = {
            "user_input": user_input,
            "request_tts": request_tts,
        }

        # Detect input type
        context = self.input_detector(context)
        
        if context["input_descriptor"]["type"] == "audio":
            context = self.stt_agent(context)

        context = self.content_agent(context)

        # Parse question and extract intent/entities
        context = self.query_agent(context)

        # Retrieve relevant passages
        context = self.retriever(context)

        # Generate an answer using LLM
        context = self.answer_agent(context)

        # Verify the generated answer
        context = self.verifier(context)

        # If a visual is needed, create it
        if context.get("needs_visual", False):
            context = self.visual_agent(context)

        # Format the final response
        context = self.formatter(context)

        # If TTS was requested, synthesize speech
        if request_tts:
            context = self.tts_agent(context)

        return context.get("formatted_response")
