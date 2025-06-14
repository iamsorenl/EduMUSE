import os
import io
import json
import re
from typing import Dict, List, Any
from datetime import datetime
import elevenlabs
from elevenlabs import play
from pydub import AudioSegment
from openai import OpenAI
from edumuse.flows.flow_registry import EducationFlow, flow_registry

# Voice IDs for ElevenLabs
HOST_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # Default host voice
GUEST_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Default guest voice

class PodcastFlow(EducationFlow):
    """Flow for generating podcast-style audio content from educational materials"""
    
    def __init__(self):
        self.openai_client = OpenAI()
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        if not elevenlabs_api_key:
            print("❌ ELEVENLABS_API_KEY not found in environment variables")
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        print(f"✅ ELEVENLABS_API_KEY found: {elevenlabs_api_key[:5]}...{elevenlabs_api_key[-5:]}")
        elevenlabs.set_api_key(elevenlabs_api_key)
    
    @property
    def flow_type(self) -> str:
        return "podcast"
    
    def get_flow_info(self) -> Dict[str, Any]:
        return {
            "name": "podcast",
            "description": "Generates a podcast-style conversation between a host and guest based on educational content",
            "output_format": "audio",
            "requirements": ["elevenlabs_api_key", "openai_api_key"]
        }
    
    def process(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process sources to generate a podcast-style audio conversation"""
        
        try:
            print(f"🎙️ Starting podcast generation for topic: {context.get('topic', 'Educational Topic')}")
            
            # Extract content from sources
            content = ""
            for source in sources:
                content += source.get("content", "")
            
            print(f"📄 Extracted {len(content)} characters of content")
            
            # Generate podcast dialogue using OpenAI
            print("🤖 Generating podcast dialogue using OpenAI...")
            dialogue = self._generate_podcast_dialogue(content, context.get("topic", "Educational Topic"))
            print(f"✅ Generated dialogue with {len(dialogue)} segments")
            
            # Generate audio using ElevenLabs
            print("🔊 Generating audio using ElevenLabs...")
            audio_path = self._generate_audio(dialogue, context.get("topic", "Educational Topic"))
            
            if not audio_path:
                print("❌ Failed to generate audio")
                return {
                    "flow_type": "podcast",
                    "sources_found": self._format_dialogue_as_text(dialogue),
                    "error": "Failed to generate audio",
                    "dialogue_segments": len(dialogue),
                    "metadata": {
                        "format": "mp3",
                        "voices_used": [HOST_VOICE_ID, GUEST_VOICE_ID],
                        "generated_at": datetime.now().isoformat()
                    }
                }
            
            print(f"✅ Generated audio saved to: {audio_path}")
            
            # Return the result
            return {
                "flow_type": "podcast",
                "sources_found": self._format_dialogue_as_text(dialogue),
                "audio_output": audio_path,
                "dialogue_segments": len(dialogue),
                "metadata": {
                    "duration_seconds": self._get_audio_duration(audio_path),
                    "format": "mp3",
                    "voices_used": [HOST_VOICE_ID, GUEST_VOICE_ID],
                    "generated_at": datetime.now().isoformat()
                }
            }
        except Exception as e:
            print(f"❌ Error in podcast generation: {e}")
            import traceback
            traceback.print_exc()
            
            # Return error information
            return {
                "flow_type": "podcast",
                "error": f"Error in podcast generation: {str(e)}",
                "sources_found": "Failed to generate podcast",
                "metadata": {
                    "error_details": traceback.format_exc(),
                    "generated_at": datetime.now().isoformat()
                }
            }
    
    def _generate_podcast_dialogue(self, content: str, topic: str) -> List[Dict[str, Any]]:
        """Generate a podcast-style dialogue using OpenAI"""
        
        prompt = (
            "You are a podcast script writer. Given the following content, "
            "generate a podcast-style conversation between a Host and a Guest. "
            "The conversation should be informative, engaging, and cover the main points. "
            f"The topic is: {topic}. "
            f"Return a **valid JSON list** of dictionaries. Each dictionary must have keys: 'speaker', 'text', 'voice_id'. "
            f"Use this voice_id for Host: {HOST_VOICE_ID}, and this for Guest: {GUEST_VOICE_ID}. "
            "Use only double quotes (\") for all keys and values. Do not wrap the output in markdown or code blocks.\n\n"
            f"Content:\n{content[:3000]}\n\n"
            "Podcast Dialogue:"
        )

        response = self.openai_client.chat.completions.create(
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
            print(f"Could not parse OpenAI output. Error: {e}")
            # Return a fallback dialogue
            return [
                {"speaker": "Host", "text": f"Welcome to this educational podcast about {topic}.", "voice_id": HOST_VOICE_ID},
                {"speaker": "Guest", "text": "Thank you for having me. I'm excited to discuss this topic.", "voice_id": GUEST_VOICE_ID},
                {"speaker": "Host", "text": "Let's start with the basics. Could you give our listeners an overview?", "voice_id": HOST_VOICE_ID},
                {"speaker": "Guest", "text": f"Certainly. {content[:200]}...", "voice_id": GUEST_VOICE_ID},
                {"speaker": "Host", "text": "That's fascinating. What are some practical applications of this knowledge?", "voice_id": HOST_VOICE_ID},
                {"speaker": "Guest", "text": "There are several applications worth discussing...", "voice_id": GUEST_VOICE_ID},
            ]
    
    def _generate_audio(self, dialogue: List[Dict[str, Any]], topic: str) -> str:
        """Generate audio from dialogue using ElevenLabs"""
        
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"podcast_{topic.replace(' ', '_')}_{timestamp}.mp3"
        
        # Use absolute path for the output file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..', '..'))
        uploads_dir = os.path.join(base_dir, "uploads")
        
        # Ensure the uploads directory exists
        os.makedirs(uploads_dir, exist_ok=True)
        
        output_path = os.path.join(uploads_dir, output_filename)
        print(f"🎙️ Generating podcast to: {output_path}")
        
        try:
            # Generate audio segments
            segments = []
            for line in dialogue:
                print(f"🔊 {line['speaker']}: {line['text']}")
                try:
                    audio_bytes = elevenlabs.generate(
                        text=line["text"],
                        voice=line["voice_id"],
                        model="eleven_multilingual_v2",
                    )
                    segments.append(AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3"))
                    print(f"✅ Generated audio for: {line['speaker']}")
                except Exception as e:
                    print(f"❌ Error generating audio for {line['speaker']}: {e}")
                    # Create a silent segment as a fallback
                    segments.append(AudioSegment.silent(duration=500))

            # Combine audio and export
            if segments:
                print(f"🔄 Combining {len(segments)} audio segments...")
                final_audio = sum(segments)
                final_audio.export(output_path, format="mp3")
                print(f"✅ Podcast saved to: {output_path}")
                return output_path
            else:
                print("❌ No audio segments were generated")
                return ""
        except Exception as e:
            print(f"❌ Error in audio generation: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _format_dialogue_as_text(self, dialogue: List[Dict[str, Any]]) -> str:
        """Format the dialogue as readable text"""
        
        formatted_text = "# Podcast Transcript\n\n"
        
        for line in dialogue:
            formatted_text += f"**{line['speaker']}**: {line['text']}\n\n"
        
        return formatted_text
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """Get the duration of an audio file in seconds"""
        
        try:
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0  # Convert milliseconds to seconds
        except Exception as e:
            print(f"Error getting audio duration: {e}")
            return 0.0

# Register the flow
flow_registry.register_flow("podcast", PodcastFlow(), "content")
