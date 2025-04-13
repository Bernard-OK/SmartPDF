import requests
from newspaper import Article
from readability import Document
from bs4 import BeautifulSoup
from app.utils.cleaner import clean_text
from playwright.async_api import async_playwright

async def scrape_url_content(url: str) -> str:
    # Try newspaper3k
    try:
        article = Article(url)
        article.download()
        article.parse()
        raw_text = article.text
        cleaned_text = clean_text(raw_text)

        if cleaned_text and len(cleaned_text) >= 50:
            return cleaned_text
    except:
        pass

    # Try readability-lxml
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        doc = Document(response.text)
        soup = BeautifulSoup(doc.summary(), "html.parser")
        paragraphs = soup.find_all("p")
        raw_text = " ".join([p.get_text() for p in paragraphs])
        cleaned_text = clean_text(raw_text)

        if cleaned_text and len(cleaned_text) >= 50:
            return cleaned_text
    except:
        pass

    # Final fallback: Headless browser with async Playwright
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=15000)
            await page.wait_for_timeout(3000)  # Wait for JS-rendered content
            content = await page.content()
            await browser.close()

            soup = BeautifulSoup(content, "html.parser")

            # Try to extract from article tag
            article = soup.find("article")
            if article:
                raw_text = article.get_text()
            else:
                paragraphs = soup.find_all("p")
                raw_text = " ".join([p.get_text() for p in paragraphs])

            cleaned_text = clean_text(raw_text)

            if not cleaned_text or len(cleaned_text) < 50:
                raise Exception("The blog content is missing or too short.")

            return cleaned_text

    except Exception as e:
        raise Exception(f"Failed to scrape URL with all methods: {str(e)}")