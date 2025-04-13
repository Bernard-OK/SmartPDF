from openai import OpenAI
from app.config import OPENAI_API_KEY

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_text(text: str) -> str:
    if len(text) > 4000:
        text = text[:4000]  # Prevent token overflow

    response = client.chat.completions.create(
        model="gpt-4",  # You can switch to "gpt-3.5-turbo" for faster/cheaper use
        messages=[
            {"role": "system", "content": "You are an expert content summarizer. Return a concise, clear summary of the following blog content."},
            {"role": "user", "content": text}
        ],
        temperature=0.6,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()