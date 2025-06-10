import os
import io
import sys
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from pydub import AudioSegment
from pdfminer.high_level import extract_text
from openai import OpenAI

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

HOST_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
GUEST_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

def safe_extract_text(pdf_path):
    if not os.path.isfile(pdf_path):
        # Try to resolve relative to the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(script_dir, pdf_path)
        if os.path.isfile(abs_path):
            pdf_path = abs_path
        else:
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    return extract_text(pdf_path)

# Helper to call OpenAI and get podcast-style conversation
def generate_podcast_dialogue(pdf_text):
    prompt = (
        "You are a podcast script writer. Given the following document text, "
        "generate a podcast-style conversation between a Host and a Guest. "
        "The conversation should be informative, engaging, and cover the main points of the document. "
        f"Use this exact format for each turn: {{'speaker': 'Host' or 'Guest', 'text': '...', 'voice_id': '{HOST_VOICE_ID}' or '{GUEST_VOICE_ID}'}}. "
        f"Use '{HOST_VOICE_ID}' for Host and '{GUEST_VOICE_ID}' for Guest. "
        "Return a Python list of such dictionaries, no extra text.\n\n"
        f"Document:\n{pdf_text[:3000]}\n\n"
        "Podcast Dialogue:"
    )
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=1500,
    )
    import json
    import re
    try:
        raw_output = response.choices[0].message.content.strip()
        match = re.search(r"dialogue\s*=\s*(\[\s*{.*?}\s*\])", raw_output, re.DOTALL)
        if match:
            parsed_list = json.loads(match.group(1).replace("'", '"'))
            return parsed_list
        else:
            raise ValueError("No valid dialogue list found in output.")
    except Exception as e:
        print("⚠️ Could not parse OpenAI output. Raw output:")
        print(response.choices[0].message.content.strip())
        print(f"Error: {e}")
        return [
            {"speaker": "Host", "text": "Sorry, could not parse podcast dialogue.", "voice_id": HOST_VOICE_ID},
            {"speaker": "Guest", "text": "Please check the prompt or formatting of the response.", "voice_id": GUEST_VOICE_ID},
        ]

# Main logic
if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
    print(f"PDF argument received: {pdf_path}")
    # Extract text from PDF (robust path)
    pdf_text = safe_extract_text(pdf_path)
    # Generate podcast dialogue using OpenAI
    dialogue = generate_podcast_dialogue(pdf_text)
else:
    # Default fallback dialogue
    dialogue = [
        {"speaker": "Host", "text": "Welcome to the EduMUSE podcast. Today we're diving into one of the coolest applications of AI – planning your dream vacation using large language models.", "voice_id": HOST_VOICE_ID},
        {"speaker": "Guest", "text": "Thanks for having me! I'm thrilled to talk about our project – an AI-powered travel planning agent built at UC Santa Cruz.", "voice_id": GUEST_VOICE_ID},
        {"speaker": "Host", "text": "Fantastic! Let's start with the basics. What exactly does this AI Travel Agent do?", "voice_id": HOST_VOICE_ID},
        {"speaker": "Guest", "text": "It helps users plan trips end-to-end – from booking flights and hotels to recommending activities – all through a conversational interface powered by LLaMA 3 and the AutoGen framework.", "voice_id": GUEST_VOICE_ID},
        {"speaker": "Host", "text": "That sounds amazing. So, how is this different from something like Google Travel?", "voice_id": HOST_VOICE_ID},
        {"speaker": "Guest", "text": "Great question. Unlike static tools, our system uses multiple specialized AI agents. Each one handles a different part of the planning – like a Dialog Agent for user input, a Search Agent for live travel data, a Recommendation Agent for activities, and so on.", "voice_id": GUEST_VOICE_ID},
        {"speaker": "Host", "text": "So it's like a team of AI experts working behind the scenes. I love it. And how does it personalize trips?", "voice_id": HOST_VOICE_ID},
        {"speaker": "Guest", "text": "Exactly! The system stores user preferences and trip history using Redis. That means we can customize suggestions based on whether someone's on a solo trip or traveling with family, and even stay within a given budget or vibe.", "voice_id": GUEST_VOICE_ID},
        {"speaker": "Host", "text": "Nice. What about real-world integration? Does it actually work with live data?", "voice_id": HOST_VOICE_ID},
        {"speaker": "Guest", "text": "Yep! We connect to TripAdvisor and Amadeus APIs to fetch real-time flight and hotel options. That makes the recommendations accurate and actionable.", "voice_id": GUEST_VOICE_ID},
        {"speaker": "Host", "text": "Let's talk performance. How well did it do in practice?", "voice_id": HOST_VOICE_ID},
        {"speaker": "Guest", "text": "We achieved an 86% success rate in generating complete, budget-friendly itineraries. We also used GPT-4 as a judge to rate the quality, and it scored us above 4.5 out of 5 across various metrics like delivery, commonsense logic, and adherence to constraints.", "voice_id": GUEST_VOICE_ID},
        {"speaker": "Host", "text": "That's impressive! Were there any limitations?", "voice_id": HOST_VOICE_ID},
        {"speaker": "Guest", "text": "Some, yes. Sequential execution introduces latency, and despite prompt tuning, LLMs occasionally hallucinate. Also, handling multiple users simultaneously is still a challenge.", "voice_id": GUEST_VOICE_ID},
        {"speaker": "Host", "text": "Every system has room to grow. Any plans for the future?", "voice_id": HOST_VOICE_ID},
        {"speaker": "Guest", "text": "We're considering a feedback loop so users can rate suggestions, caching popular destinations to reduce latency, and making it even more interactive and scalable.", "voice_id": GUEST_VOICE_ID},
        {"speaker": "Host", "text": "This could really revolutionize how people plan trips. Thanks for sharing all of this!", "voice_id": HOST_VOICE_ID},
        {"speaker": "Guest", "text": "Absolutely, and thanks again for having me. It's an exciting time for AI and real-world applications.", "voice_id": GUEST_VOICE_ID},
    ]

segments = []
for i, line in enumerate(dialogue):
    audio = client.text_to_speech.convert(
        text=line["text"],
        voice_id=line["voice_id"],
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(chunk for chunk in audio)
    segments.append(AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3"))

# Combine all audio segments into one
final_audio = sum(segments)
final_audio.export("dialogue_podcast.mp3", format="mp3")

# Optional: play the result
play(open("dialogue_podcast.mp3", "rb").read())
