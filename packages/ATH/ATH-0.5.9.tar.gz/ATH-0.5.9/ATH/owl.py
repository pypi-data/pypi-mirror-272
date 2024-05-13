import webbrowser
from requests import get
from bs4 import BeautifulSoup

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

dict_cokies = {
    "SOCS": "CAISHAgBEhJnd3NfMjAyNDA1MDItMF9SQzIaAnJvIAEaBgiA3uWxBg",
    "NID": "514=qjaciV8V1GpYd_-W5S4XFREADeKWknqjET8PHP-9V3p2_BonBYe0HWPKFLYghc6KW5dAzGuyu00OKXFlfL2c2eIYN8k4v7tMWbMVbBD2PDSEy-ILnU5GDEMrYh9Aj3jESYlBrwbr0rjmHxOjb3Q_0mVE5Fo_uimvjAV4bDJjrxQnk9SIZqXx8F3PBsrQElmLhIh4suwnCWdB3OY",
    "AEC": "AQTF6HxFC7aiGu7YFc-HRw-OKZrIAgyMBLB2DqhQF1lXxd6DIsJ_8I-l9vw",
}


def scrap_google(prompt):
    lk = []
    url = "https://www.google.com/search?q=" + prompt
    response = get(url, cookies=dict_cokies)
    content = response.text
    bs = BeautifulSoup(content, "html.parser")
    links = bs.find_all("a")
    links = filter(lambda link: "/url?" in link.get("href") and "google" not in link.get("href") and "/search" not in link.get("href"), links)
    for i, link in enumerate(links):
        link = link.get("href").replace("/url?q=", "")
        print(i + 1, link)
        lk.append(link)
    choice = int(input("Enter choice: "))
    lk = list(lk)
    webbrowser.open(lk[int(choice)-1])