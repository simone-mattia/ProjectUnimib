import requests, datetime, time, sys
sys.path.append("../utils")
from bs4 import BeautifulSoup
from utils.utils import printAndLog, printAndLogError


class AnsaAcquisition:

    '''
    AnsaAcquisition init function:
    - print banner
    - set logfile name
    '''
    def __init__(self, logfile_name):
        self.printBanner()
        self.logfile_name = logfile_name


    def printBanner(self):
        print("""
                                                     _     _ _   _             
     /\                         /\                  (_)   (_) | (_)            
    /  \   _ __  ___  __ _     /  \   ___ __ _ _   _ _ ___ _| |_ _  ___  _ __  
   / /\ \ | '_ \/ __|/ _` |   / /\ \ / __/ _` | | | | / __| | __| |/ _ \| '_ \ 
  / ____ \| | | \__ \ (_| |  / ____ \ (_| (_| | |_| | \__ \ | |_| | (_) | | | |
 /_/    \_\_| |_|___/\__,_| /_/    \_\___\__, |\__,_|_|___/_|\__|_|\___/|_| |_|
                                            | |                                
                                            |_|                                                           
        """)


    '''
    Given a list of names and and a x number of days:
    - webscaping of ansa.it
    - search articles for given names in the last x days
    - return list of articles  
    '''
    def getAnsaArticles(self, args):

        URL = "https://www.ansa.it/ricerca/ansait/search.shtml"
        articles = []

        try:
            printAndLog(self.logfile_name, "[*] ansaAcquisition.getArticles(names, days)")

            names = args[0]
            days = args[1]
            acquisition_datetime = args[2]
            
            for name in names:
                article_index = 0
                n_articles = 0
                loop = True

                while loop:

                    search_data = {"any":name, "periodo":days, "rows":50, "sort": "data:desc", "start": article_index}
                    search_response = requests.post(URL, data = search_data)

                    soup = BeautifulSoup(search_response.content, "html.parser")

                    if article_index == 0:
                        n_articles = int(soup.find(class_="search-num-result").text.split(" ")[0])
                    else:
                        time.sleep(1)
                    raw_articles = soup.find_all(class_= "search-content-result")

                    for raw_article in raw_articles:
                        article = {}
                        article["acquisition_datetime"] = acquisition_datetime
                        article["username"] = names[0]
                        article["timestamp"] = datetime.datetime.strptime(raw_article.find("span").text, "%d-%m-%Y %H:%M") - datetime.timedelta(hours=1)
                        article["title"] = raw_article.find("a").text
                        if article not in articles:
                            articles.append(article)
                    
                    article_index += 50
                    if article_index > n_articles:
                        loop = False

            for article in articles:
                if any(name.lower() in article["title"].lower() for name in names):
                    article["inTitle"] = True
                else:
                    article["inTitle"] = False
            
            printAndLog(self.logfile_name, "[+] {} ansa articles for {}".format(len(articles), names[0]))
            return articles
        
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] ansaAcquisition.getArticles(names, days) - error message: {}".format(str(e)))
            return -1