import argparse
from orchestrator.orchestrator import MultiAgentOrchestrator

def main():
    print("\n=== Starting EduMUSE Podcast Generator ===")
    parser = argparse.ArgumentParser(description="Run Multi-Agent QA Pipeline")
    parser.add_argument(
        "--input", "-i", required=True, help="User input: URL, file path, or text query"
    )
    parser.add_argument(
        "--tts", action="store_true", help="Whether to synthesize speech output"
    )
    # parser.add_argument(
    #     "--host-voice", default="tom", 
    #     help="Voice to use for the host (options: tom, emma, daniel, william, sarah, olivia, charlotte, matthew, james, michelle)"
    # )
    # parser.add_argument(
    #     "--guest-voice", default="emma",
    #     help="Voice to use for the guest (options: tom, emma, daniel, william, sarah, olivia, charlotte, matthew, james, michelle)"
    # )
    # parser.add_argument(
    #     "--preset", "-p", default="fast",
    #     choices=["ultra_fast", "fast", "standard", "high_quality"],
    #     help="Quality preset for TTS generation"
    # )
    args = parser.parse_args()

    print(f"\nInput file: {args.input}")
    print(f"TTS requested: {args.tts}")

    print("\nInitializing orchestrator...")
    orchestrator = MultiAgentOrchestrator()
    
    print("\nStarting pipeline...")
    result = orchestrator.run(
        args.input, 
        request_tts=args.tts
    )

    if args.tts and result.get("audio_output"):
        print("\n=== Final Output ===")
        print(f"Audio file saved to: {result.get('audio_output')}")
    else:
        print("\nWARNING: No audio output was generated!")

    print("\n=== Process Complete ===")

if __name__ == "__main__":
    main()