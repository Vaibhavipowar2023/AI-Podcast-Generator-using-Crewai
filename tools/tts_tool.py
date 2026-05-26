import requests
import base64
import os
import time
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_URL = "https://api.sarvam.ai/text-to-speech"

# Voice config
VOICES = {
    "ALEX": {"speaker": "abhilash", "pace": 0.95, "pitch": 0},
    "SAM":  {"speaker": "anushka",  "pace": 1.05, "pitch": 1},
}


def generate_speech(text: str, speaker_key: str, output_path: str) -> bool:
    """Call Sarvam TTS API and save WAV file."""
    voice = VOICES.get(speaker_key, VOICES["ALEX"])

    # Sarvam max input is 500 chars — chunk if needed
    chunks = [text[i:i+400] for i in range(0, len(text), 400)]
    all_audio = b""

    for chunk in chunks:
        payload = {
            "inputs": [chunk],
            "target_language_code": "en-IN",
            "speaker": voice["speaker"],
            "model": "bulbul:v2",
            "pitch": voice["pitch"],
            "pace": voice["pace"],
            "loudness": 1.5,
            "speech_sample_rate": 22050,
            "enable_preprocessing": True,
        }

        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json"
        }

        for attempt in range(3):
            try:
                response = requests.post(
                    SARVAM_URL,
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                if response.status_code == 200:
                    data = response.json()
                    audio_bytes = base64.b64decode(data["audios"][0])
                    all_audio += audio_bytes
                    break
                elif response.status_code == 429:
                    time.sleep(5 * (attempt + 1))
                else:
                    print(f"TTS error: {response.text}")
                    break
            except Exception as e:
                print(f"TTS exception: {e}")
                time.sleep(3)

    if all_audio:
        with open(output_path, "wb") as f:
            f.write(all_audio)
        return True
    return False

@tool("Generate Podcast Audio")
def generate_podcast_audio(script: str) -> str:
    """
    Takes a podcast script with ALEX: and SAM: labels and generates
    a merged MP3 audio file. Returns the output file path.
    """
    try:
        from pydub import AudioSegment
    except ImportError:
        return "Error: pydub not installed. Run: pip install pydub"

    os.makedirs("output/audio", exist_ok=True)
    os.makedirs("output/temp", exist_ok=True)

    # Parse script into lines
    lines = []
    for line in script.strip().split("\n"):
        line = line.strip()
        if line.startswith("ALEX:"):
            text = line[5:].strip()
            if text:
                lines.append(("ALEX", text))
        elif line.startswith("SAM:"):
            text = line[4:].strip()
            if text:
                lines.append(("SAM", text))

    if not lines:
        return "Error: No ALEX: or SAM: lines found in script."

    print(f"\n Generating audio for {len(lines)} lines...")

    # Generate audio per line
    audio_segments = []
    alex_count = 0
    sam_count = 0

    for i, (speaker, text) in enumerate(lines):
        temp_path = f"output/temp/line_{i:03d}_{speaker}.wav"
        print(f"  [{i+1}/{len(lines)}] {speaker}: {text[:50]}...")

        success = generate_speech(text, speaker, temp_path)

        if success and os.path.exists(temp_path):
            try:
                segment = AudioSegment.from_wav(temp_path)
                pause = AudioSegment.silent(duration=400)
                audio_segments.append(segment + pause)

                if speaker == "ALEX":
                    alex_count += 1
                else:
                    sam_count += 1
            except Exception as e:
                print(f"   Could not load segment {i}: {e}")

        time.sleep(0.5)  # avoid rate limiting

    if not audio_segments:
        return "Error: No audio segments were generated."

    # Merge all segments
    print("\nMerging audio segments...")
    final_audio = audio_segments[0]
    for seg in audio_segments[1:]:
        final_audio += seg

    # Export final MP3
    output_path = "output/audio/podcast.mp3"
    final_audio.export(output_path, format="mp3", bitrate="128k")

    # Cleanup temp files
    import shutil
    shutil.rmtree("output/temp", ignore_errors=True)

    return (
        f"Podcast generated successfully!\n"
        f"File: {output_path}\n"
        f"Duration: {len(final_audio)/1000:.1f} seconds\n"
        f"Alex lines: {alex_count} | Sam lines: {sam_count}"
    )