import requests
from speech_generation import generate_podcast
from functions import convert_to_script_lines

# Try llama.cpp style first
def call_local_llama_cpp(prompt):
    try:
        response = requests.post("http://127.0.0.1:8080/completion", json={
            "prompt": prompt,
            "temperature": 0.7,
            "top_p": 0.95,
            "n_predict": 500  # llama.cpp uses n_predict, not max_tokens
        })

        if response.ok:
            print("✅ Response from /completion:")
            print(response.json()['content'])
            with open("response.txt", "w") as file:
                file.write(response.json()['content'])
            return response.json()['content']
        else:
            print("❌ /completion gave:", response.status_code)
    except Exception as e:
        print("Error with /completion:", e)


def build_dialogue_prompt(news_summary):
    prompt = f"""
        You are writing a podcast script for two hosts, Alex and Sam.

        Alex is laid-back, curious, and occasionally witty, while Sam is enthusiastic, well-informed, and loves to share fun facts. They are discussing today's news in a casual, entertaining way — think friendly banter mixed with insightful commentary. Add reactions, a touch of humor, and keep it engaging and relatable.

        Here's the news summary they’re discussing:
        \"\"\"
        {news_summary}
        \"\"\"

        Write the conversation, alternating between Alex and Sam, in natural spoken English. Keep it under 10 lines, and make sure it flows like a real conversation. Use contractions, informal language, and sprinkle in some personality quirks to make it sound authentic and lively.

        Ensure the response is ALWAYS encoded in "utf-8" and follows this format:

        Sam: (smiling) Hey Alex, so what do you think of the US having a rare earths mine?

        Alex: (smirking) Yeah, that’s interesting. It was a surprise.

        Sam: (interested) I heard China responded to Trump’s tariffs by limiting exports of rare earths.

        Alex: (nodding) Yeah, that sounds like a big deal.
    """
    return prompt.strip()

def load_news():
    file_path = "top_headlines1.txt"
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")


transcript = call_local_llama_cpp(build_dialogue_prompt(load_news()))
script_lines = convert_to_script_lines(transcript)
print("Script lines:", script_lines)
generate_podcast(script_lines, output_file="episode_output1.mp3")    





