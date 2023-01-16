import datetime, requests, json, os, sys
sys.path.append("../utils")
from utils.utils import printAndLog, printAndLogError


class InstagramAcquisition:

    '''
    InstagramAcquisition init function:
    - print banner
    - set logfile name
    '''
    def __init__(self, logfile_name):
        self.printBanner()
        self.logfile_name = logfile_name


    def printBanner(self):
        print("""
  _____           _                                                          _     _ _   _             
 |_   _|         | |                                                        (_)   (_) | (_)            
   | |  _ __  ___| |_ __ _  __ _ _ __ __ _ _ __ ___     __ _  ___ __ _ _   _ _ ___ _| |_ _  ___  _ __  
   | | | '_ \/ __| __/ _` |/ _` | '__/ _` | '_ ` _ \   / _` |/ __/ _` | | | | / __| | __| |/ _ \| '_ \ 
  _| |_| | | \__ \ || (_| | (_| | | | (_| | | | | | | | (_| | (_| (_| | |_| | \__ \ | |_| | (_) | | | |
 |_____|_| |_|___/\__\__,_|\__, |_|  \__,_|_| |_| |_|  \__,_|\___\__, |\__,_|_|___/_|\__|_|\___/|_| |_|
                            __/ |                                   | |                                
                           |___/                                    |_|                                                        
        """)


    '''
    Given a instagram username: use official instagramma api to return an object that contains:
    - followers
    - following
    - post number
    - post details
    '''
    def getInstagramData(self, args):
        
        insta_data = {}

        try:
            printAndLog(self.logfile_name, "[*] instagramAcquisition.getInstagramData(username)")

            username = args[0]
            acquisition_datetime = args[1]
            cookies = args[2]

            headers = {
                'authority': 'www.instagram.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'no-cache',
                'cookie': cookies,
                'pragma': 'no-cache',
                'sec-ch-prefers-color-scheme': 'light',
                'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
                'viewport-width': '396'
            }

            url = "https://www.instagram.com/"+username+"/?__a=1&__d=dis"
            response = requests.request("GET", url, headers=headers, data={})
            
            g=json.loads(response.text)['graphql']
            user=g["user"]
            id=user["id"]
            post=user["edge_owner_to_timeline_media"]
            posts=post["edges"]
            post_data=[]

            index=0
            for p in posts:
                item = p["node"]
                item_likes=item["edge_liked_by"]
                item_comments=item["edge_media_to_comment"]
                post_data.append({"item":index,"type":item["__typename"],"display_url":item["display_url"],"likes":item_likes["count"],"comments":item_comments["count"],"timestamp":item["taken_at_timestamp"]})
                index=index+1

            # "timestamp":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            insta_data = {
                "acquisition_datetime":acquisition_datetime,
                "username":username,
                "followers":user["edge_followed_by"]["count"],
                "following":user["edge_follow"]["count"],
                "full_name":user["full_name"],
                "is_business":user["is_business_account"],
                "business_category_name":user["business_category_name"],
                "category_name":user["category_name"],
                "is_verified":user["is_verified"],
                "profile_pic_url":user["profile_pic_url"],
                "post_count":post["count"],
                "timestamp":datetime.datetime.now(),
                "post_data":post_data}  

            printAndLog(self.logfile_name, "[+] instagram data for {}".format(username))

            return insta_data
        
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] instagramAcquisition.getInstagramData(username) - error message: {}".format(str(e)))
            return -1


    '''
    Given a instagram username read a json file that contains all storical data to return an array that for each day contains:
    - date
    - followers
    - following
    - post number
    '''
    def getStoricalInstagramData(self, args):
        
        insta_data = []

        try:
            printAndLog(self.logfile_name, "[*] instagramAcquisition.getStoricalInstagramData(username)")

            username = args[0]
            acquisition_datetime = args[1]

            with open(os.path.dirname(os.path.abspath(__file__)) + "/instagram_influencer_history.json", "r") as storical_data:
                storical_data = [data["history"] for data in json.load(storical_data) if data["name"] == username]
                if len(storical_data) != 0:
                    storical_data = storical_data[0]
                    for single_day in storical_data:
                        insta_data.append({
                            "acquisition_datetime":acquisition_datetime,
                            "username":username,
                            "followers": single_day["follower"],
                            "following": single_day["following"],
                            "post_count": single_day["post"],
                            "timestamp": datetime.datetime.strptime(single_day["date"], "%Y-%m-%d")
                        })
            
            printAndLog(self.logfile_name, "[+] {} instagram data for {}".format(len(insta_data), username))
            return insta_data
        
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] instagramAcquisition.getStoricalInstagramData(username) - error message: {}".format(str(e)))
            return -1