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


# def get_story_details_ao3(story_id):
#     response = requests.get(f"https://hisbrowneyedgirl.com/hsapi/ao3/{story_id}")
#     data = json.loads(response.text)
#     print(data)


# get_story_details_ao3("29403498")


# def get_new_stories():
#     url = "https://archiveofourown.org/tags/Hermione%20Granger*s*Harry%20Potter/works?page=1"

#     html = requests.get(url).content

#     soup = BeautifulSoup(html, "html.parser")

#     all_stories_ol = soup.find("ol", {"class": "work index group"}).findAll("li", recursive=False)
#     # print(all_stories_ol)
#     a = time.time()
#     for li in all_stories_ol:
#         workid = li.get("id")[5:]
#         work = AO3.Work(int(workid))
#         print(work.title)
#     print("Time taken: ", time.time() - a)


# get_new_stories()


def search_ao3(query):
    search = AO3.Search(title=query, fandoms="Harry Potter", rating=13)
    search.update()
    print(search.total_results)
    for result in search.results:
        print(result)


search_ao3("bonds of time")


# import requests as r

# # add review
# review = "This movie was exactly what I wanted in a Godzilla vs Kong movie. It's big loud, brash and dumb, in the best ways possible. It also has a heart in a the form of Jia (Kaylee Hottle) and a superbly expressionful Kong. The scenes of him in the hollow world are especially impactful and beautifully shot/animated. Kong really is the emotional core of the film (with Godzilla more of an indifferent force of nature), and is done so well he may even convert a few members of Team Godzilla."


# keys = {"review": review}

# prediction = r.get("http://127.0.0.1:8000/predict-review/", params=keys)

# results = prediction.json()
# print(results["prediction"])
# print(results["Probability"])
