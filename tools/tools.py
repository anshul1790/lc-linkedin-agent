from langchain_tavily import TavilySearch

def get_profile_url_tavily(name: str):
    """
    Uses Tavily Search to find the LinkedIn profile URL of a person by their name.
    Args:
        name (str): The full name of the person to look up.
    Returns:
        str: The LinkedIn profile URL or "Profile not found" if no profile is found.
    """
    search = TavilySearch()
    response = search.run(f"{name}")
    return response
