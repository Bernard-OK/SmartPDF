# 🧠 AI Blog Summarizer API

A FastAPI-powered microservice that summarizes raw blog text or online articles using OpenAI's GPT-4.

---

## 🚀 Features

- Summarize **any blog or article** by URL
- Summarize **raw text content**
- Uses **GPT-4** via OpenAI API
- Built with **FastAPI** and **BeautifulSoup**
- Clean and extendable architecture
- Automatically documented with Swagger UI

---

## 📌 Endpoints

### `POST /api/summarize-text`

**Request Body:**
```json
{
  "text": "Paste your blog content here..."
}

Response:

{
  "summary": "This blog discusses..."
}

POST /api/summarize-url

Request Body:

{
  "summary": "This article explains..."
}

🧰 Tech Stack
	•	🐍 Python 3.10+
	•	⚡ FastAPI
	•	🌐 OpenAI GPT-4 API
	•	🧽 BeautifulSoup (HTML scraping)
	•	🔐 Dotenv for secret management

⚙️ Installation & Setup
	1.	Clone the repo:
git clone https://github.com/yourusername/ai-blog-summarizer.git
cd ai-blog-summarizer

	2.	Create virtual environment:
python3 -m venv venv
source venv/bin/activate

    3.	Install dependencies
pip install -r requirements.txt

    4.	Add your OpenAI key in .env:
OPENAI_API_KEY=your_key_here
    5.	Run the server:
uvicorn app.main:app --reload
    6.	Visit the API docs:
http://localhost:8000/docs


🧪 Example Use Case
	•	Summarize long blog articles for newsletters
	•	Generate SEO-friendly summaries for marketing
	•	Quickly digest content from competitor sites
	•	Build summarizer integrations into content platforms



📸 Screenshots

Add screenshots of:
	•	Swagger UI
	•	Example response
	•	Postman demo (if available)


🤝 Contributing

Open to contributions, improvements, and feedback.
Feel free to fork and enhance the logic or connect your own frontend.

📄 License

MIT License

✨ Author

Bernard Okwampah
LinkedIn →
CTO | Full Stack AI Developer