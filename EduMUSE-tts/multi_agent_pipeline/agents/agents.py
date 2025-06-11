import os
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
import requests

from bs4 import BeautifulSoup
from io import BytesIO
from typing import Any, Dict, List, Optional

# pdfminer imports
from pdfminer.high_level import extract_text

# Make sure OPENAI_API_KEY is set in your environment


class InputDetectionAgent:
    """
    Determines whether the user input is a URL, a text query, a document path, or audio.
    """
    URL_PATTERN = re.compile(r"https?://[\w\-.]+(\.[\w\-.]+)+[/#?]?.*")

    def __init__(self):
        pass

    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raw_input = context.get("user_input")
        descriptor = {"type": None, "payload": None}

        # If it's a local file path
        if isinstance(raw_input, str) and os.path.isfile(raw_input):
            ext = os.path.splitext(raw_input)[1].lower()

            if ext in [".pdf", ".txt", ".docx"]:
                descriptor["type"] = "document"
                descriptor["payload"] = raw_input
            elif ext in [".wav", ".mp3", ".m4a"]:
                descriptor["type"] = "audio"
                descriptor["payload"] = raw_input
            else:
                # Unknown extension → treat as document
                descriptor["type"] = "document"
                descriptor["payload"] = raw_input

        # If it matches a URL pattern
        elif isinstance(raw_input, str) and re.match(self.URL_PATTERN, raw_input):
            descriptor["type"] = "url"
            descriptor["payload"] = raw_input

        # Otherwise, treat as plain text query
        else:
            descriptor["type"] = "query"
            descriptor["payload"] = raw_input

        context["input_descriptor"] = descriptor
        return context


class SpeechToTextAgent:
    """
    Converts audio payload to text via OpenAI Whisper API.
    """

    def __init__(self, model: str = "whisper-1"):
        self.model = model

    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        descriptor = context.get("input_descriptor", {})
        if descriptor.get("type") == "audio":
            audio_path = descriptor.get("payload")
            transcript = self._transcribe(audio_path)
            context["transcript"] = transcript
            context["input_descriptor"] = {"type": "query", "payload": transcript}
        return context

    def _transcribe(self, audio_path: str) -> str:
        """
        Calls OpenAI Whisper to transcribe the given audio file.
        Returns plain-text transcript.
        """
        try:
            with open(audio_path, "rb") as audio_file:
                resp = client.audio.transcribe(model=self.model,
                file=audio_file)
            return resp.get("text", "")
        except Exception as e:
            return f"<Whisper transcription failed: {str(e)}>"


class ContentAcquisitionAgent:
    """
    Fetches or loads content based on input_descriptor:
      - URL → scrape via requests+BeautifulSoup
      - PDF → extract via pdfminer.six
      - TXT/DOCX → simple file read
      - query  → no content
    """

    def __init__(self):
        pass

    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        descriptor = context.get("input_descriptor", {})
        content = None

        if descriptor.get("type") == "url":
            url = descriptor.get("payload")
            content = self._fetch_url(url)

        elif descriptor.get("type") == "document":
            path = descriptor.get("payload")
            ext = os.path.splitext(path)[1].lower()

            if ext == ".pdf":
                content = self._extract_pdf(path)
            elif ext in [".txt", ".docx"]:
                content = self._read_text_file(path)
            else:
                content = self._read_text_file(path)

        elif descriptor.get("type") == "query":
            content = None  # No content to load

        context["fetched_content"] = content
        return context

    def _fetch_url(self, url: str) -> str:
        """
        Uses requests + BeautifulSoup to pull out the main text from a webpage.
        """
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            for tag in soup(["script", "style"]):
                tag.decompose()

            paragraphs = [p.get_text(separator=" ", strip=True) for p in soup.find_all("p")]
            return "\n\n".join(paragraphs).strip()
        except Exception as e:
            return f"<Failed to fetch URL {url}: {str(e)}>"

    def _extract_pdf(self, path: str) -> str:
        """
        Uses pdfminer.six to extract text from a PDF.
        """
        try:
            text = extract_text(path)
            return text or "<PDF was empty>"
        except Exception as e:
            return f"<PDF extraction failed for {path}: {str(e)}>"

    def _read_text_file(self, path: str) -> str:
        """
        Reads a .txt or .docx (plain‐text) file. Docx support here is minimal:
        If you need real .docx → consider python-docx.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"<Failed to read {path}: {str(e)}>"


class QueryUnderstandingAgent:
    """
    Parses the user's question into a small 'Question Object':
      - text
      - entities (stubbed)
      - intent (keyword-based)
      - context_source (pointer to fetched_content)
    """

    def __init__(self):
        pass

    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        question = context.get("input_descriptor", {}).get("payload")
        if question:
            entities = self._extract_entities(question)
            intent = self._infer_intent(question)
            question_obj = {
                "text": question,
                "entities": entities,
                "intent": intent,
                "context_source": context.get("fetched_content")
            }
            context["question_object"] = question_obj
        return context

    def _extract_entities(self, text: str) -> List[str]:
        # (Optional) Use a lightweight approach or leave as empty list
        return []

    def _infer_intent(self, text: str) -> str:
        lowered = text.lower()
        if any(tok in lowered for tok in ["define", "what is", "who is", "explain"]):
            return "definition"
        return "fact_lookup"


class RetrievalAgent:
    """
    Retrieves relevant passages from `fetched_content` by a simple
    bag‐of‐words overlap. If no content exists, returns [] so that
    the LLM can answer freely.
    """

    def __init__(self, top_k: int = 3):
        self.top_k = top_k

    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        qobj = context.get("question_object", {})
        source = qobj.get("context_source")
        snippets: List[str] = []

        if source:
            snippets = self._retrieve_from_text(source, qobj.get("text"))
        else:
            snippets = []

        context["retrieved_snippets"] = snippets
        return context

    def _retrieve_from_text(self, text: str, query: str) -> List[str]:
        """
        Splits `text` into paragraphs, ranks by number of shared words
        with query, and returns top_k paragraphs.
        """
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        query_words = set(re.findall(r"\w+", query.lower()))

        scored = []
        for para in paragraphs:
            words = set(re.findall(r"\w+", para.lower()))
            overlap = len(words & query_words)
            scored.append((overlap, para))

        # Sort descending by overlap, take top_k
        scored.sort(key=lambda x: x[0], reverse=True)
        top_paras = [para for score, para in scored if score > 0][: self.top_k]
        return top_paras


class AnswerGenerationAgent:
    """
    Uses OpenAI ChatCompletion to generate an answer based on question + snippets.
    """

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model

    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        qobj = context.get("question_object", {})
        snippets = context.get("retrieved_snippets", [])
        prompt = self._build_prompt(qobj.get("text"), snippets)

        answer = self._call_llm(prompt)
        needs_visual = self._detect_visual_requirement(answer)

        context["raw_answer"] = answer
        context["needs_visual"] = needs_visual
        return context

    def _build_prompt(self, question: str, snippets: List[str]) -> str:
        """
        If snippets exist, include them in the system prompt. Otherwise,
        just ask the question directly.
        """
        if snippets:
            context_block = "\n\n---\n\n".join(snippets)
            return (
                f"You are an expert assistant. Use the following context to answer:\n\n"
                f"{context_block}\n\n"
                f"Question: {question}\n"
                f"Answer:"
            )
        else:
            return f"You are an expert assistant.\nQuestion: {question}\nAnswer:"

    def _call_llm(self, prompt: str) -> str:
        try:
            response = client.chat.completions.create(model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=512)
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"<LLM call failed: {str(e)}>"

    def _detect_visual_requirement(self, answer: str) -> bool:
        """
        Naively check if the LLM's answer mentions needing a chart/graph.
        (This is a stub; you can refine later.)
        """
        lowered = answer.lower()
        for kw in ["chart", "graph", "plot", "diagram", "figure"]:
            if kw in lowered:
                return True
        return False


class VerificationAgent:
    """
    Verifies the LLM-generated answer by re-asking the model to double-check
    against the retrieved context.
    """

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model

    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        answer = context.get("raw_answer", "")
        snippets = context.get("retrieved_snippets", [])

        if not snippets:
            context["verification"] = {"verdict": True, "notes": None}
            return context

        verdict, notes = self._verify(answer, snippets)
        context["verification"] = {"verdict": verdict, "notes": notes}
        return context

    def _verify(self, answer: str, snippets: List[str]) -> (bool, Optional[str]):
        """
        Prompt the model: "Given these context paragraphs, is the following answer
        factually consistent? If not, list discrepancies." If the model says it's inconsistent,
        we mark verdict = False and include the model's notes.
        """

        combined_context = "\n\n---\n\n".join(snippets)
        verification_prompt = (
            f"You are a fact-check assistant.\nContext:\n{combined_context}\n\n"
            f"Answer to verify:\n{answer}\n\n"
            f"Is the answer fully supported by the context? If yes, just respond 'YES'. "
            f"If not, respond 'NO' and briefly explain which part is not supported."
        )
        try:
            resp = client.chat.completions.create(model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful fact-checking assistant."},
                {"role": "user", "content": verification_prompt},
            ],
            temperature=0.0,
            max_tokens=150)
            verdict_text = resp.choices[0].message.content.strip()
            if verdict_text.upper().startswith("YES"):
                return True, None
            else:
                return False, verdict_text
        except Exception as e:
            return False, f"<Verification failed: {str(e)}>"


class VisualGenerationAgent:
    """
    Stub: If needs_visual == True, we could generate a chart/graph here.
    For now, we just return a placeholder. 
    """

    def __init__(self):
        pass

    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if context.get("needs_visual"):
            context["visual_output"] = "<VISUAL_PLACEHOLDER>"
        return context


class FormattingAgent:
    """
    Packages final answer text, visuals, and metadata into a response payload.
    """

    def __init__(self):
        pass

    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        answer = context.get("raw_answer", "")
        visual = context.get("visual_output")
        verification = context.get("verification", {})

        formatted = {
            "answer_text": answer,
            "visuals": visual if visual else None,
            "verified": verification.get("verdict"),
            "verification_notes": verification.get("notes"),
            "sources": context.get("retrieved_snippets", []),
        }
        if context.get("request_tts"):
            formatted["tts_text"] = answer

        context["formatted_response"] = formatted
        return context

#TODO: need to figure this
class TTSAgent:

    def __init__(self):
        pass

    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Always call example.py and pass the input file as an argument
        user_input = context.get('user_input', '')
        os.system('python3 "' + os.path.join(os.path.dirname(__file__), 'example.py') + '" "' + str(user_input) + '"')
        return context
