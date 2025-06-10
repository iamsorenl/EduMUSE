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
    parser.add_argument(
        "--host-voice", default="tom", 
        help="Voice to use for the host (options: tom, emma, daniel, william, sarah, olivia, charlotte, matthew, james, michelle)"
    )
    parser.add_argument(
        "--guest-voice", default="emma",
        help="Voice to use for the guest (options: tom, emma, daniel, william, sarah, olivia, charlotte, matthew, james, michelle)"
    )
    parser.add_argument(
        "--preset", "-p", default="fast",
        choices=["ultra_fast", "fast", "standard", "high_quality"],
        help="Quality preset for TTS generation"
    )
    args = parser.parse_args()

    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.run(
        args.input, 
        request_tts=args.tts,
        host_voice=args.host_voice,
        guest_voice=args.guest_voice,
        preset=args.preset
    )

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