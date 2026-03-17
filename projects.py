from dotenv import load_dotenv
import os
import json
import requests
from bs4 import BeautifulSoup

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

from langchain.utilities import SerpAPIWrapper

load_dotenv()

search = SerpAPIWrapper()

def search_jobs(query: str):
    return search.run(query)

search_tool = Tool(
    name="Job Search",
    func=search_jobs,
    description="Search for AI agent or AI jobs from Google"
)

def scrape_website(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator=" ", strip=True)

        return text[:3000] 
    except Exception as e:
        return f"Error scraping: {str(e)}"

scrape_tool = Tool(
    name="Web Scraper",
    func=scrape_website,
    description="Scrape content from a given URL"
)

def save_to_file(data: str):
    try:
        parsed = json.loads(data)

        with open("job_list.json", "w") as f:
            json.dump(parsed, f, indent=4)

        return "Saved to job_list.json successfully"
    except Exception as e:
        return f"Error saving file: {str(e)}"

file_tool = Tool(
    name="File Writer",
    func=save_to_file,
    description="Save structured JSON data into a file"
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

tools = [search_tool, scrape_tool, file_tool]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

query = """
Find 5 AI agent developer jobs.
For each job extract:
- title
- company
- location
- link

Return ONLY JSON format like:
[
  {
    "title": "...",
    "company": "...",
    "location": "...",
    "link": "..."
  }
]

Then save it using File Writer tool.
"""

agent.run(query)