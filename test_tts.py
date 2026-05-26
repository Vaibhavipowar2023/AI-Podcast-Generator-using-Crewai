import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

url = "https://api.sarvam.ai/text-to-speech"

payload = {
    "inputs": ["Hello! Welcome to our AI podcast. Today we discuss artificial intelligence."],
    "target_language_code": "en-IN",
    "speaker": "abhilash",        # ← male voice for Alex
    "model": "bulbul:v2",
    "pitch": 0,
    "pace": 1.0,
    "loudness": 1.5,
    "speech_sample_rate": 22050,
    "enable_preprocessing": True,
}

headers = {
    "api-subscription-key": os.getenv("SARVAM_API_KEY"),
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("Keys in response:", list(data.keys()))

    if "audios" in data:
        audio_data = base64.b64decode(data["audios"][0])
    elif "audio" in data:
        audio_data = base64.b64decode(data["audio"][0])
    else:
        print("Full response:", data)
        exit()

    with open("test_alex.wav", "wb") as f:
        f.write(audio_data)
    print("Audio saved as test_alex.wav — open and play it!")

else:
    print("Error:", response.text)