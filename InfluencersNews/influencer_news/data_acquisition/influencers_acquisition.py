import requests, sys, os, json, datetime
sys.path.append("../utils")
from bs4 import BeautifulSoup
from utils.utils import printAndLog, printAndLogError

class InfluencersAcquisition:

    '''
    InfluencersAcquisition init function:
    - set logfile name
    - print banner
    '''
    def __init__(self, args):
        self.logfile_name = args[0]
        self.printBanner()


    def printBanner(self):
        print("""
  _____        __ _                                                              _     _ _   _             
 |_   _|      / _| |                                        /\                  (_)   (_) | (_)            
   | |  _ __ | |_| |_   _  ___ _ __   ___ ___ _ __ ___     /  \   ___ __ _ _   _ _ ___ _| |_ _  ___  _ __  
   | | | '_ \|  _| | | | |/ _ \ '_ \ / __/ _ \ '__/ __|   / /\ \ / __/ _` | | | | / __| | __| |/ _ \| '_ \ 
  _| |_| | | | | | | |_| |  __/ | | | (_|  __/ |  \__ \  / ____ \ (_| (_| | |_| | \__ \ | |_| | (_) | | | |
 |_____|_| |_|_| |_|\__,_|\___|_| |_|\___\___|_|  |___/ /_/    \_\___\__, |\__,_|_|___/_|\__|_|\___/|_| |_|
                                                                        | |                                
                                                                        |_|                                
        """)

        
    '''
    Influencers acquisition function:
    - get top 100 influencers
    - set influencers names alias
    - return influencers list
    '''
    def getInfluencers(self, args):
        acquisition_datetime = args[0]
        self.getTop100InfluencersLocal()
        print(self.influencers)
        #self.influencerAlias()
        for influencer in self.influencers:
            influencer["acquisition_datetime"] =  acquisition_datetime
        return self.influencers


    '''
    Get Top100 influencers:
    - webscraping of influenceritalia.it
    - exception for "Ultimo" to avoid false articles
    - return influencers list with instagram username and real name 
    '''
    def getTop100Influencer(self):

        URL = "https://www.influenceritalia.it/?p=instagram"
        URL_NAME = "https://www.influenceritalia.it/u/"
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3835.0 Safari/537.36', 'Accept': '*/*'}
        self.influencers = {}

        try: 
            printAndLog(self.logfile_name, "[*] influencersAcquisition.getTop100Influencer()")
            response = requests.get(URL,headers= headers)
            html_tree = BeautifulSoup(response.text, "html.parser")
            elements=html_tree.find_all("a", class_="claNome")

            for i in elements:

                name = i['name']
                url_name = URL_NAME + name

                response_name = requests.get(url_name,headers= headers)
                html_tree_name = BeautifulSoup(response_name.text, "html.parser")

                name_surname=html_tree_name.find_all("strong")[0].text
                
                if name_surname == "Ultimo":
                    name_surname = "Ultimo Peterpan"
                if name_surname == "ipantellas":
                    name_surname = "i-pantellas"
                
                self.influencers[name]={"names": [name, name_surname],"position":elements.index(i)+1}
        
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] influencersAcquisition.getTop100Influencer() - error message: {}".format(str(e)))
            self.influencers = -1

    '''
    Get Top100 influencers from local json
    '''
    def getTop100InfluencersLocal(self):
        
        self.influencers = []

        try:
            printAndLog(self.logfile_name, "[*] influencersAcquisition.getTop100InfluencersLocal()")

            with open(os.path.dirname(os.path.abspath(__file__)) + "/influencers_history.json", "r") as storical_data:
                storical_data = json.load(storical_data)
                if len(storical_data) != 0:
                    for element in storical_data:
                        self.influencers.append({ 
                            "username": element["username"],
                            "names":element["names"],
                            "position":element["position"],
                        })
            
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] influencersAcquisition.getTop100InfluencersLocal() - error message: {}".format(str(e)))
            self.influencers = -1
    

    '''
    Given an influencers list add influencers alias at name list:
    - use a pre-defined INFLUENCERS_ALIAS dictionary 
    - return the updated list 
    '''
    def influencerAlias(self):

        INFLUENCERS_ALIAS = {
            "chiaraferragni":["ferragnez"],
            "fedez": ["ferragnez"],
            "andreapirlo21": ["andrea pirlo"],
            "ykaaar": ["maneskin"],
            "urban_streetart":["urban streetart"],
            "sferaebbasta": ["sfera ebbasta", "gionata boschetti"],
            "ultimopeterpan": ["ultimo peter pan", "niccolò moriconi", "niccolo moriconi"],
            "alicecampello": ["alice campello"],
            "pioeamedeo83": ["pio d'Antini", "amedeo grieco"],
            "elodie": ["elodie di patrizi"],
            "j.axofficial": ["alessandro aleotti"],
            "ghali":["ghali amdouni"],
            "lebonwski":["salmo", "maurizio pisciottu"],
            "stefanolepri": ["stefano lepri", "st3pny"],
            "valebise": ["Valentino Bisegna"],
            "ipantellas": ["jacopo malnati", "daniel marangiolo"]
        }

        influencers_list = []

        try: 
            printAndLog(self.logfile_name, "[*] influencersAcquisition.influencerAlias()")
            for alias in INFLUENCERS_ALIAS:
                if alias in self.influencers.keys():
                    for new_alias in INFLUENCERS_ALIAS[alias]:
                        self.influencers[alias]["names"].append(new_alias)

            for username in self.influencers.keys():
                influencer = self.influencers[username]
                influencer["username"] = username
                influencers_list.append(influencer)

            self.influencers = influencers_list

        except Exception as e:
            printAndLogError(self.logfile_name, "[-] influencersAcquisition.influencerAlias(influencers) - error message: {}".format(str(e)))
            self.influencers = -1