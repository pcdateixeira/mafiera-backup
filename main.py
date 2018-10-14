# Put avatars in another json document
# Add titles

import urllib.request
import re
import json
import utils
from bs4 import BeautifulSoup

threadUrl = "https://www.resetera.com/threads/conspiracy-mafia-ot-where-paranoia-is-part-of-the-flavour.73689/page-2"

req = urllib.request.Request(
    threadUrl,
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
)

html = urllib.request.urlopen(req).read()
threadPage = BeautifulSoup(html, 'lxml').findAll(class_=["messageText", "messageUserInfo"])

texts = []
usernames = []
avatars = []

for element in threadPage:
    if str(element).find("blockquote class=\"messageText") > 0:
        texts.append(utils.validateText(str(element)))
        continue

    matchUsername = re.search(r'itemprop="name">(.+?)<\/a>', str(element)) # finds usernames
    if matchUsername:
        usernames.append(matchUsername.group(1))

    matchAvatar = re.search(r'a class="avatar(.*) src="(.+?)" width=', str(element)) # finds avatars
    if matchAvatar:
        avatars.append("https://www.resetera.com/" + matchAvatar.group(2))

jsonData = dict()

for i in range(len(usernames)):
    dictPost = dict()
    dictPost['Name'] = usernames[i]
    dictPost['Avatar'] = avatars[i]
    dictPost['Text'] = texts[i]
    if i < 9:
        jsonData['Post #0' + str(i+1)] = dictPost
    else:
        jsonData['Post #' + str(i+1)] = dictPost

with open('output.json', 'w', encoding="utf-8") as outfile:
    json.dump(jsonData, outfile, sort_keys=True, indent=4, ensure_ascii=False)
