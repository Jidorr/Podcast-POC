import edge_tts
from pydub import AudioSegment
import os

# Function to generate podcast audio
def generate_podcast(script_lines, output_file="episode_output.mp3"):
    # Choose voices
    voices = {
        "Alex": "en-US-GuyNeural",     # Male voice
        "Sam": "en-US-JennyNeural"     # Female voice
    }

    # Create output folder
    os.makedirs("audio_lines", exist_ok=True)

    # TTS function
    async def generate_voice(speaker, text, out_path):
        communicate = edge_tts.Communicate(text=text, voice=voices[speaker])
        await communicate.save(out_path)

    # Generate all audio files
    import asyncio

    async def process_audio():
        for i, (speaker, text) in enumerate(script_lines):
            filename = f"audio_lines/line_{i+1}_{speaker}.mp3"
            await generate_voice(speaker, text, filename)

    asyncio.run(process_audio())

    # Combine audio into one file
    final = AudioSegment.silent(duration=500)
    for i in range(len(script_lines)):
        speaker = script_lines[i][0]
        path = f"audio_lines/line_{i+1}_{speaker}.mp3"
        audio = AudioSegment.from_mp3(path)
        final += audio + AudioSegment.silent(duration=300)

    final.export(output_file, format="mp3")
    print(f"✅ Podcast episode saved as: {output_file}")
