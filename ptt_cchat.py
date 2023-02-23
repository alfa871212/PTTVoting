import requests
from bs4 import BeautifulSoup



class Users:
    def __init__(self, id, rawcontent, push_counts):
        self.id = id 
        # raw content is a lis(maybe with more than two comments)
        self.rawcontent = rawcontent
    
    def user_counts(self):
        return len(self.rawcontent)






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

unique_user_id_lis=[]
unique_content_lis=[]
#following has some bug --> id--content mismatch
for i in user_id_lis:
    if i not in unique_user_id_lis:
        unique_user_id_lis.append(i)
        unique_content_lis.append(content_lis[unique_user_id_lis.index(i)])

test_dict = dict(zip(user_id_lis,content_lis))
#print(unique_user_id_lis)
#print(unique_content_lis)
user_voted=dict()
comic_counts=[0]*120
#print(comic_counts)
#for i in unique_content_lis:
for i in content_lis:

    push_content_split = i.split()
    push_content_split = list(set(push_content_split))
    voted_num_for_one_user=[]
    for j in push_content_split:
        if j.isdigit():
            voted_num = int(j)
            if voted_num < 120 and voted_num > 0:
                voted_num_for_one_user.append(voted_num)
                comic_counts[voted_num-1]=comic_counts[voted_num-1]+1
    #user_voted[unique_user_id_lis[unique_content_lis.index(i)]]=voted_num_for_one_user
    user_voted[user_id_lis[content_lis.index(i)]]=voted_num_for_one_user

all_results=dict()
for i in range(len(comic_counts)):
    all_results[comic_name[i]]=comic_counts[i]
#print(all_result)

sorted_all_results = sorted(all_results.items(), key=lambda x:x[1],reverse=True)
#print(sorted_all_results)
for i in range(len(sorted_all_results)):
    output=str(i+1)+". "+sorted_all_results[i][0]+" "+str(sorted_all_results[i][1])
    print(output)