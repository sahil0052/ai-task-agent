# AI Task Execution Agent

This project is an autonomous AI agent that can:
- Search for jobs using Google (SerpAPI)
- Scrape websites
- Extract structured data
- Save results into JSON files

## Example Task
"Find 5 AI agent jobs and save them to a file"

## Tools Used
- LangChain
- OpenAI
- SerpAPI
- BeautifulSoup

## Setup

bash
pip install -r requirements.txt

Create .env:

OPENAI_API_KEY=your_key
SERPAPI_API_KEY=your_key

Run: python main.py
