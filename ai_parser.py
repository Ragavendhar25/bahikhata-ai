import os, json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT = """You extract shop ledger data from text.
The text may be English, Tamil, Hindi or mixed.
Return ONLY JSON: {"item": "<item name in English>", "quantity": <number>, "price": <price per unit>}
If the text gives one total amount for the quantity, divide it to get the price per unit."""

def parse_entry(text: str) -> dict:
    r = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "system", "content": PROMPT},
                  {"role": "user", "content": text}],
        response_format={"type": "json_object"},
    )
    return json.loads(r.choices[0].message.content)

def transcribe(filename: str, audio_bytes: bytes, language: str | None = None) -> str:
    r = client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model="whisper-large-v3",
        language=language,
    )
    return r.text