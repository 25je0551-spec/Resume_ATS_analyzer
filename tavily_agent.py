from tavily import TavilyClient
import os

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def search_internships(query):

    response = client.search(
        query=query,
        max_results=6,
        search_depth="advanced"
    )

    return response["results"]