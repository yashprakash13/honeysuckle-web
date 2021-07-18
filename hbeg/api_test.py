import ast
import json
import time

import AO3
import requests
from bs4 import BeautifulSoup

# import requests


# def get_story_details(link):
#     story_id = link[link.index("s/") + 2 : link.index("/", link.index("s/") + 4)]

#     response = requests.get(f"http://localhost:8000/hsapi/ffn/{story_id}")
#     data = json.loads(response.text)

#     print(data["title"])


# get_story_details("https://www.fanfiction.net/s/2963991/1/Harry-Potter-and-the-Oroborus-Light")


def get_new_stories():
    url = "https://archiveofourown.org/tags/Hermione%20Granger*s*Harry%20Potter/works?page=1"

    html = requests.get(url).content

    soup = BeautifulSoup(html, "html.parser")

    all_stories_ol = soup.find("ol", {"class": "work index group"}).findAll("li", recursive=False)
    # print(all_stories_ol)
    a = time.time()
    for li in all_stories_ol:
        workid = li.get("id")[5:]
        work = AO3.Work(int(workid))
        print(work.title)
    print("Time taken: ", time.time() - a)


get_new_stories()
