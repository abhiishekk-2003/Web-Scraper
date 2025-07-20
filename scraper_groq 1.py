import asyncio
import json
import random
import time
import requests
from playwright.async_api import async_playwright
from instructor import OpenAISchema, patch
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUMMARY_WORD_LIMIT = 150 

client = Groq(api_key=GROQ_API_KEY)
patch(client) 

class SummarySchema(OpenAISchema):
    """Schema for structured summarization"""
    summary: str

async def get_search_results(query, num_results=5):
    """Fetch search results from SerpAPI."""
    url = f"https://serpapi.com/search.json?q={query}&api_key={SERPAPI_KEY}&num={num_results}"
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        results = response.json()
        return [res["link"] for res in results.get("organic_results", [])]
    except requests.RequestException as e:
        print(f"Error fetching search results: {e}")
        return []

async def scrape_website(playwright, url):
    """Scrape content from a website using Playwright."""
    try:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        page = await context.new_page()

        print(f"Visiting {url} ...")
        await page.goto(url, timeout=60000, wait_until="domcontentloaded")
        title = await page.title()
        text = await page.inner_text("body")

        await browser.close()

        delay = random.uniform(2, 5)
        print(f"Waiting {delay:.2f} seconds before next request...")
        await asyncio.sleep(delay)

        return {"url": url, "title": title, "content": text[:2000]}

    except Exception as e:
        return {"url": url, "error": str(e)}

async def summarize_with_groq(content):
    """Summarize the scraped content using GroqAI LLaMA 3-8B."""
    try:
        response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "You are a helpful AI assistant that summarizes text."},
        {"role": "user", "content": f"Summarize the following content in {SUMMARY_WORD_LIMIT} words:\n\n{content}"}],
        temperature=0.7,
        max_tokens=250,
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"GroqAI summarization failed: {e}")
        return "Summarization error."

async def main(topic):
    """Orchestrates fetching search results, scraping, and summarizing."""
    async with async_playwright() as playwright:
        print(f" Searching Google for: {topic}")
        urls = await get_search_results(topic)
        print(f"Found {len(urls)} websites to scrape.")

        results = []
        for url in urls:
            result = await scrape_website(playwright, url)
            results.append(result)

        all_text = " ".join([r["content"] for r in results if "content" in r])

        summary = await summarize_with_groq(all_text)

        output = {
        "topic": topic,
        "scraped_at": time.strftime("%d-%m-%Y %H:%M:%S"),
        "summary": summary,
        "results": results,
        }

        with open("scraped_data.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

        print("Scraping & summarization complete. Data saved to 'scraped_data.json'")

if __name__ == "__main__":
    topic = "Top cars of India in 2024"
    asyncio.run(main(topic))




    
    