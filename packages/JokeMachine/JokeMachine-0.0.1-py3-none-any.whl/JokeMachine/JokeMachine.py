import requests
import random

def fetch_joke(url):
 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            jokes = response.json()
            setup = jokes.get("hook", "")
            punchline = jokes.get("punchline", "")
            return setup, punchline
        else:
            return None
    except requests.exceptions.RequestException:
        return None
def fetch_full_joke(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            jokes = response.json()
            setup = jokes.get("hook", "")
            punchline = jokes.get("punchline", "")
            joke=setup+"\n"+punchline
            return joke
        else:
            return None
    except requests.exceptions.RequestException:
        return None
def Dad_Joke(full=None):
    """
    Fetches a random dad joke from the API.

    Args:
        full (bool): If True, returns the full joke with a newline between setup and punchline.
                               If False (default), returns a tuple containing the setup (str) and punchline (str).

    Returns:
        Tuple: If full is False, returns a tuple representing the random joke fetched from the API,
                                            containing the setup (str) and punchline (str).
                                            If full is True, returns the full joke as a single string with a newline between setup and punchline.
                                            Returns None if the request fails or no jokes are available.
    """
    url = "https://mistiiqx.pythonanywhere.com/dad"
    if full == True:
         return fetch_full_joke(url)
    if not full:
         return fetch_joke(url)


