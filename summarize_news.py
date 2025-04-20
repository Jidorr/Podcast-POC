from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Read the contents of the top_headlines.txt file
file_path = "top_headlines.txt"

def load_news():
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")

# Build the summarization prompt
def build_summary_prompt(text):
    prompt = f"""
You are a helpful assistant that summarizes daily news for a podcast. Summarize the following news articles in clear, concise, and engaging English:

{text}
"""
    return prompt.strip()

# Generate summary using TinyLlama
def summarize(prompt):
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0.Q5_K_M"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )

    inputs = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
    outputs = model.generate(
        inputs,
        max_new_tokens=500,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result[len(prompt):].strip()

# Run the script
if __name__ == "__main__":
    raw_text = load_news()
    prompt = build_summary_prompt(raw_text)
    summary = summarize(prompt)

    print("\n🧠 Summarized News:\n")
    print(summary)
