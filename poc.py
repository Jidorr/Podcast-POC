import os
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from config.config import API_KEY

# Load your NewsAPI key from env or hardcode it
NEWS_API_KEY = API_KEY
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
COUNTRY = "es"  # Spain
ARTICLE_LIMIT = 5




# === Step 1: Fetch News ===
def fetch_spanish_news():
    params = {
        "country": COUNTRY,
        "language": "es",
        "pageSize": ARTICLE_LIMIT,
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()

    articles = data.get("articles", [])
    summaries = []
    for article in articles:
        content = f"{article['title']}. {article.get('description', '')}"
        summaries.append(content)
    print(summaries)
    return summaries

# === Step 2: Build Prompt for Podcast Dialogue ===
def build_podcast_prompt(news_bullets):
    news_text = "\n".join(f"- {item}" for item in news_bullets)
    prompt = f"""
Eres un modelo de lenguaje que genera un guión de podcast. Tienes que escribir una conversación entretenida, relajada y casual entre dos presentadores, Carla y Luis, sobre las noticias de hoy en España.

Estas son las noticias:
{news_text}

Haz que parezca una conversación real: un poco de humor, opiniones, explicaciones sencillas y energía. Mantén la charla en español. ¡Hazlo como si fuera un episodio de un podcast diario!
"""
    return prompt.strip()

# === Step 3: Generate Podcast Script ===
def generate_podcast_script(prompt):
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0.Q5_K_M"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)

    output = model.generate(
        input_ids,
        max_new_tokens=1000,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        repetition_penalty=1.1,
        pad_token_id=tokenizer.eos_token_id
    )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text[len(prompt):].strip()

# === Main ===
if __name__ == "__main__":
    news_items = fetch_spanish_news()
    if not news_items:
        print("No news found.")
        exit()

    podcast_prompt = build_podcast_prompt(news_items)
    print("\n[Prompt Sent to LLM]:\n", podcast_prompt[:500], "...\n")  # preview

    podcast_script = generate_podcast_script(podcast_prompt)
    print("\n🎙️ Generated Podcast Script:\n")
    print(podcast_script)
