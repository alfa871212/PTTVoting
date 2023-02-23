import requests
from bs4 import BeautifulSoup


def add_vote(index):
    comic_counts[index-1]=comic_counts[index-1]+1

url = 'https://www.ptt.cc/bbs/C_Chat/M.1676194202.A.7DD.html'
print("Requesting reponse from URL...")
html = requests.get(url)
print("URL html get!")
html_str = html.text
soup = BeautifulSoup(html_str, 'lxml')
user_id_from_url=soup.find_all(class_="f3 hl push-userid")
user_id_lis=[]
content_from_url=soup.find_all(class_="f3 push-content")
content_lis=[]
main_content=soup.find(id='main-content')
comic_name=[]
for tag in main_content:
    tmp = str(tag.string)
    if(tmp[0]=='='):
        last_word_index = tmp.find("\n")
        comic_name.append(tmp[1:last_word_index])

for tag in user_id_from_url:
    user_id_lis.append(tag.string)
for tag in content_from_url:
    tmp = str(tag.string)
    tmp = tmp[2:]
    content_lis.append(tmp)
comic_counts=[0]*120

for i in range(len(user_id_lis)):
    print(user_id_lis[i])
    print(content_lis[i])
    tmp = content_lis[i].split()
    print("splitting voted seq: " , tmp)
    ind = -1
    while (ind!="0"):
        ind = input("vote num:")
        add_vote(int(ind))
    print("--------------")

print(comic_counts)
