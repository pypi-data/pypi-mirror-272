import webbrowser

def owl(url):
    if url.startswith("https://"):
        webbrowser.open(url)
    else:
        webbrowser.open(f"https://{url}")

def web_search_with_google(prompt):
    webbrowser.open(f"https://www.google.com/search?q={prompt}")

def web_search_with_wikipedia(prompt):
    webbrowser.open(f"https://en.wikipedia.org/wiki/{prompt}")

def web_search_with_youtube(prompt):
    if prompt.startswith("@"):
        webbrowser.open(f"https://www.youtube.com/{prompt}")
    else:
        webbrowser.open(f"https://www.youtube.com/results?search_query={prompt}")

def web_search_with_bing(prompt):
    webbrowser.open(f"https://www.bing.com/search?q={prompt}")