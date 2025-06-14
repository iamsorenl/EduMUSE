import os
import io
import sys
import json
import re
import datetime
import time
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from pydub import AudioSegment
from pdfminer.high_level import extract_text
from openai import OpenAI

# Load .env from root directory (two levels up from this file)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

HOST_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
GUEST_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

def safe_extract_text(pdf_path):
    if not os.path.isfile(pdf_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(script_dir, pdf_path)
        if os.path.isfile(abs_path):
            pdf_path = abs_path
        else:
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    return extract_text(pdf_path)

def generate_podcast_dialogue(text_input):
    prompt = (
        "You are a podcast script writer. Given the following content, "
        "generate a podcast-style conversation between a Host and a Guest. "
        "The conversation should be informative, engaging, and cover the main points. "
        f"Return a **valid JSON list** of dictionaries. Each dictionary must have keys: 'speaker', 'text', 'voice_id'. "
        f"Use this voice_id for Host: {HOST_VOICE_ID}, and this for Guest: {GUEST_VOICE_ID}. "
        "Use only double quotes (\") for all keys and values. Do not wrap the output in markdown or code blocks.\n\n"
        f"Content:\n{text_input[:3000]}\n\n"
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

    try:
        raw_output = response.choices[0].message.content.strip()

        # Remove ``` or ```json wrappers if present
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`").strip()
            if raw_output.lower().startswith("json"):
                raw_output = raw_output[len("json"):].strip()

        parsed_list = json.loads(raw_output)
        return parsed_list

    except Exception as e:
        print("\n⚠️ Could not parse OpenAI output. Raw output:")
        print(response.choices[0].message.content.strip())
        print(f"Error: {e}\n")
        return [
            {"speaker": "Host", "text": "Sorry, could not parse podcast dialogue.", "voice_id": HOST_VOICE_ID},
            {"speaker": "Guest", "text": "Please check the formatting or prompt.", "voice_id": GUEST_VOICE_ID},
        ]

# === Main Script ===
if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
    print(f"Input received: {pdf_path}")
    print("Treating input as a PDF file.")
    
    print("Extracting text from PDF...")
    pdf_text = safe_extract_text(pdf_path)
    print(f"Extracted {len(pdf_text)} characters from PDF")
    
    print("Generating dialogue...")
    dialogue = generate_podcast_dialogue(pdf_text)
    print(f"Generated {len(dialogue)} dialogue lines")
    
else:
    print("No input provided, using default text.")
    dialogue = generate_podcast_dialogue("This is a test podcast about artificial intelligence.")

print("Starting audio generation...")
segments = []
for i, line in enumerate(dialogue):
    line_start = time.time()
    print(f"🔊 {line['speaker']}: {line['text']}")
    print(f"Converting line {i+1}/{len(dialogue)} to speech using voice_id: {line['voice_id']}")
    
    audio = client.text_to_speech.convert(
        text=line["text"],
        voice_id=line["voice_id"],
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(chunk for chunk in audio)
    segments.append(AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3"))

    line_end = time.time()
    print(f"✅ Line {i+1} completed in {line_end - line_start:.2f} seconds")

total_time = time.time() - start_time
print(f"🎵 Total audio generation completed in {total_time:.2f} seconds")

# Combine audio and export
final_audio = sum(segments)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"dialogue_podcast_{timestamp}.mp3"
final_audio.export(output_path, format="mp3")

print(f"\nPodcast generated and saved as {output_path}")

# Optional: play audio (requires ffmpeg installed)
# play(open("dialogue_podcast.mp3", "rb").read())