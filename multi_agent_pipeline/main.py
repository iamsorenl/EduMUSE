import argparse
from orchestrator.orchestrator import MultiAgentOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Run Multi-Agent QA Pipeline")
    parser.add_argument(
        "--input", "-i", required=True, help="User input: URL, file path, or text query"
    )
    parser.add_argument(
        "--tts", action="store_true", help="Whether to synthesize speech output"
    )
    args = parser.parse_args()

    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.run(args.input, request_tts=args.tts)

    # Print formatted response
    print("Answer Text:")
    print(result.get("answer_text", ""))

    visuals = result.get("visuals")
    if visuals:
        print("\nVisuals:")
        print(visuals)

    if args.tts and result.get("audio_output"):
        print("\nAudio Output:")
        print(result.get("audio_output"))

if __name__ == "__main__":
    main()