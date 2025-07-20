# 🔎 Web Scraper and Summarizer using Groq, SerpAPI, and Playwright

This project is a Python-based web scraper that:
- Searches Google using SerpAPI
- Scrapes the content of the top N websites using Playwright
- Summarizes the content using Groq's LLaMA 3-8B model

---

## 📌 Features

- 🌐 Automated search with [SerpAPI](https://serpapi.com/)
- 🤖 Smart content scraping via [Playwright](https://playwright.dev/python/)
- 🧠 Summarization powered by Groq’s LLaMA 3-8B (using `instructor` for schema-based output)
- ⏱️ Built-in delays and error handling for stability
- 📄 Outputs results in a structured JSON file

---

## 🛠️ Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/web-scraper-groq.git
cd web-scraper-groq
```
### 2. Create a .env file
```
SERPAPI_KEY=your_serpapi_key_here
GROQ_API_KEY=your_groq_api_key_here
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
Dependencies include:

	-	playwright
	-	requests
	-	instructor
	-	groq
	-	python-dotenv
Also install, playwright browsers:
```
playwright install
```
##▶️ How to Run
Update the topic at the bottom of the script:
```
topic = "Top cars of India in 2024"
```
Then run:
```
python scraper_groq.py
```
## 📁 Output
The script creates a file named scraped_data.json with:
Example structure:
```
{
  "topic": "Top cars of India in 2024",
  "scraped_at": "20-07-2025 18:42:01",
  "summary": "...",
  "results": [
    {
      "url": "https://example.com",
      "title": "Example Title",
      "content": "Top cars include..."
    },
    ...
  ]
}
```
## 🧠 Notes
	•	You can control the number of search results by changing num_results in get_search_results().
	•	Summary length is controlled by SUMMARY_WORD_LIMIT.
	•	The summarizer uses a Groq-hosted LLaMA model with chat-completion format.

## 🛡️ Disclaimer
This tool is for research and personal use only. Always comply with the terms of service of the sites you scrape.
