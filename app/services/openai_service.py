from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.schemas.lead import LeadMessage

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_text(text: str) -> str:
    if len(text) > 4000:
        text = text[:4000]  # Prevent token overflow

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert content summarizer. Return a concise, clear summary of the following blog content."},
            {"role": "user", "content": text}
        ],
        temperature=0.6,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()

def analyze_lead_message(lead: LeadMessage) -> dict:
    message_text = lead.message
    prompt = f"""
    You are an AI sales assistant. Analyze the following lead message and return:

    1. A qualification label: Hot Lead, Not Ready, Not Relevant
    2. Confidence score between 0.0 and 1.0
    3. Estimated budget (if mentioned or inferred)
    4. Urgency (1 to 5)
    5. Tags (1-3 keywords)
    6. Product fit (High, Medium, Low)

    Message:
    ---
    {message_text}
    ---

    Respond with a JSON object with keys: qualification, confidence, budget, urgency, tags, product_fit
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that classifies and analyzes lead messages."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500
    )

    raw_content = response.choices[0].message.content.strip()

    try:
        result = eval(raw_content)  # For demo purposes — switch to `json.loads()` in production
        result.update({"name": lead.name, "email": lead.email})
        return result
    except Exception as e:
        return {
            "name": lead.name,
            "email": lead.email,
            "error": f"Failed to parse response: {str(e)}",
            "raw": raw_content
        }
