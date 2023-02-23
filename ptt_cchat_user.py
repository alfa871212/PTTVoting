import requests
from bs4 import BeautifulSoup



class Users:
    def __init__(self, id, rawcontent):
        self.id = id 
        # raw content is a lis(maybe with more than two comments)
        self.rawcontent = rawcontent
        self.voted_num_lis =[]
        self.num_voted = 0
        self.counts = 1
    def push_counts(self):
        return self.counts
    def add_counts(self):
        self.counts = self.counts+1
    def create_voted_num(self):
        temp=[]
        for i in range(self.counts):
            ind = self.counts - i - 1
            temp = self.rawcontent[ind].split()
            for j in range(len(temp)):
      
                if (temp[j].isdigit()):
                    if(int(temp[j]) not in self.voted_num_lis):
                        if (int(temp[j])<=120):
                            if (len(self.voted_num_lis)<4):
                                self.voted_num_lis.append(int(temp[j]))
        list(set(self.voted_num_lis))

    def check_valid_vote(self):
        if (len(self.voted_num_lis)>=5):
            print(self.id+" has voted for more than 4 comics.")
            
class StatSys:
    def __init__(self, urlLis):
        #self.num_voter = len(userLis)
        self.num_voter = 0
        self.repeated_voter=[]
        self.urlLis = urlLis
        self.result = [0]*120
        self.vote_times = [0]*4 # vote_times[] saves the number of voters who vote once, twice ...
        #self.comicLis = comicLis # comicLis saves the comic list with sequences(original)
        #self.userLis = userLis # userList saves the user list with pushing sequence(if repeated, save once)
        self.comicLis = []
        self.userLis = []
        self.sortedresList = []
        #self.resDict = dict.fromkeys(comicLis, 0)
        self.resDict = dict()
        #self.rankDict = dict.fromkeys(comicLis, 0)
        self.rankDict = dict()
    def index_in_id_lis(self,lis,id):
        temp=[]
        for i in range(len(lis)):
            temp.append(lis[i].id)
        if id in temp:
            return temp.index(id)
        else:
            return
    def check_in_id_lis(self,lis,id):
        temp=[]
        for i in range(len(lis)):
            temp.append(lis[i].id)
        return id in temp
    def find_user(self,lis,id):
        for i in range(len(lis)):
            if lis[i].id == id:
                return lis[i]
    def grabUrl(self):
        for i in range(len(urlLis)):
            print("Requesting reponse from URL...")
            html = requests.get(urlLis[i])
            print("URL html get!")
            html_str = html.text
            soup = BeautifulSoup(html_str, 'lxml')
            user_id_from_url=soup.find_all(class_="f3 hl push-userid")
            user_id_lis=[]
            content_from_url=soup.find_all(class_="f3 push-content")
            content_lis=[]
            main_content=soup.find(id='main-content')

            ind = 1
            for tag in main_content:
                tmp = str(tag.string)
                if(tmp[0]=='='):
                    last_word_index = tmp.find("\n")
                    self.comicLis.append(tmp[1:last_word_index]+"("+str(ind)+")")
                    ind = ind+1

            for tag in user_id_from_url:
                user_id_lis.append(tag.string)
            for tag in content_from_url:
                tmp = str(tag.string)
                tmp = tmp[2:]
                content_lis.append(tmp)

            for i in range(len(user_id_lis)):
                push_id = user_id_lis[i]
                content = content_lis[i]
                if (self.check_in_id_lis(self.userLis,push_id)):
                    #print(push_id)
                    self.repeated_voter.append(push_id)
                    ind = self.index_in_id_lis(self.userLis,push_id)
                    self.userLis[ind].rawcontent.append(content)
                    self.userLis[ind].add_counts()
                else:    
                    tmp = []
                    tmp.append(content)
                    user = Users(push_id,tmp)
                    self.userLis.append(user)
            for i in range(len(self.userLis)):
                self.userLis[i].create_voted_num()
                self.userLis[i].check_valid_vote()
        self.resDict = dict.fromkeys(self.comicLis, 0)
        self.rankDict = dict.fromkeys(self.comicLis, 0)
        self.num_voter = len(self.userLis)
    def startVote(self):
        self.grabUrl()
        for i in range(self.num_voter):
            vote = []
            vote = self.userLis[i].voted_num_lis
            self.vote_times[len(vote)-1] = self.vote_times[len(vote)-1]+1
            for j in range(len(vote)):
                vote_ind = vote[j]
                #print(vote_ind)
                self.resDict[self.comicLis[vote_ind-1]]=self.resDict[self.comicLis[vote_ind-1]]+1
                #self.result[vote_ind-1] = self.result[vote_ind-1]+1
        
        sorted_all_results = sorted(self.resDict.items(), key=lambda x:x[1],reverse=True)
        #print(sorted_all_results)
        rank = 1
        repeated_times = 1
        buffer = -1
        for i in range(len(sorted_all_results)):
            rank = i+1
            if (sorted_all_results[i][1] != buffer):
                comic_name = sorted_all_results[i][0]
                self.rankDict[comic_name] = rank
                repeated_times = 1 
            else:
                comic_name = sorted_all_results[i][0]
                self.rankDict[comic_name] = rank - repeated_times
                repeated_times = repeated_times+1
            buffer = sorted_all_results[i][1]
        self.sortedresList = sorted_all_results
    def checkRelation(self, num1,num2): # return P(vote num1 and num2| vote num1)
        vote_for_num1 = 0
        num1_comic_name = self.comicLis[num1-1]
        vote_for_num1_num2 = 0
        num2_comic_name = self.comicLis[num2-1]

        for i in range(self.num_voter):
            if (num1 in self.userLis[i].voted_num_lis):
                vote_for_num1 = vote_for_num1 + 1
                if (num2 in self.userLis[i].voted_num_lis):
                    vote_for_num1_num2 = vote_for_num1_num2 + 1

        out = "Percentage of voting for "+num1_comic_name +" who also vote for "+num2_comic_name +" is "+ str(vote_for_num1_num2/vote_for_num1)
        print(out)
    
    def isValidSearchNum(self,num):
        return num > 0 and num <=120
    def checkRank(self,search):
        if (isinstance(search, int)):
            if(self.isValidSearchNum(search)):
                comic = self.comicLis[search-1]
                print(self.rankDict[comic])
            else:
                print("Invalid search num!!")
        else:
            print(self.rankDict[search])
    def isValidSearchNum(self,num):
        return num > 0 and num <=120
    def showResult(self):
        #print(self.resDict)

        sorted_all_results = sorted(self.resDict.items(), key=lambda x:x[1],reverse=True)
        #print(sorted_all_results)
        rank = 1
        repeated_times = 1
        buffer = -1
        for i in range(len(self.sortedresList)):
            rank = i+1
            if (self.sortedresList[i][1] != buffer):
                output=str(rank)+". "+self.sortedresList[i][0]+" "+str(self.sortedresList[i][1])
                print(output)
                repeated_times = 1 
            else:
                output=str(rank-repeated_times)+". "+self.sortedresList[i][0]+" "+str(self.sortedresList[i][1])
                repeated_times = repeated_times+1

                print(output)
            buffer = self.sortedresList[i][1]




# Useful function --> should implement in statSys


url = 'https://www.ptt.cc/bbs/C_Chat/M.1676194202.A.7DD.html'
url2 = 'https://www.ptt.cc/bbs/C_Chat/M.1676455607.A.9CA.html'
urlLis = []
urlLis.append(url)
urlLis.append(url2)

#statsys = StatSys(user_class_lis,comic_name,urlLis)
statsys = StatSys(urlLis)
statsys.startVote()
statsys.showResult()