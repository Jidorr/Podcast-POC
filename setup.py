from podcastfy.client import generate_podcast

# Generate a tech debate podcast about artificial intelligence
generate_podcast(
    urls=["www.souzatharsis.com"],
    tts_model="edge",
    transcript_only=True,
    is_local=True  # Using a local LLM
)