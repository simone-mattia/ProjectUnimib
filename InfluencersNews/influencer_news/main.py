import os, dotenv, datetime, time, csv
from utils.utils import tryFunctionNTimes, printAndLog, printBanner
from utils.mongo import Mongo
from data_acquisition.influencers_acquisition import InfluencersAcquisition
from data_acquisition.ansa_acquisition import AnsaAcquisition
from data_acquisition.instagram_acquisition import InstagramAcquisition
from data_acquisition.trends_acquisition import TrendsAcquisition

# ENVIROMENT VARIABLES
dotenv.load_dotenv() # DEV ONLY
DB_NAME = os.environ["DB_NAME"]
INFLUENCERS_COLLECTION = os.environ["INFLUENCERS_COLLECTION"]
LOG_COLLETION = os.environ["LOG_COLLETION"]
NEWS_COLLECTION = os.environ["NEWS_COLLECTION"]
INSTAGRAM_COLLECTION = os.environ["INSTAGRAM_COLLECTION"]
TREND_COLLECTION = os.environ["TREND_COLLECTION"]
MONGO_CONNECT_STRING = os.environ["MONGO_CONNECT_STRING"]
INSTAGRAM_COOKIES = os.environ["INSTAGRAM_COOKIES"]
TYPE = os.environ["TYPE"]


'''
Based on the enviroment variable "TYPE" launch
- data acquisition storical
- data acquisition service
- debug mode
'''
def main():

    printBanner()

    # Log info
    LOGFILE_NAME = "data_acquisition_{}".format(TYPE)
    acquisition_datetime = datetime.datetime.now()
    printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - {} - start at {}".format(TYPE, acquisition_datetime))

    # Connect to MongoDB
    mongo = Mongo(LOGFILE_NAME, LOG_COLLETION) 
    tryFunctionNTimes(LOGFILE_NAME, 5, mongo.connect, [MONGO_CONNECT_STRING])
    tryFunctionNTimes(LOGFILE_NAME, 5, mongo.setDB, [DB_NAME])

    # Check if the influencers acquisition has already been done
    influencers_list = []
    lastLog = tryFunctionNTimes(LOGFILE_NAME, 5, mongo.findLastLog, [{"action":"influencers-acquisition"}])
    if lastLog is not None:
        printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - influencers data already acquisited at {}".format(lastLog["datetime"]))
        influencers_list = tryFunctionNTimes(LOGFILE_NAME, 5, mongo.find, [INFLUENCERS_COLLECTION])
    else:
        printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - first influencers acquisition or last failed")
        influencers = InfluencersAcquisition(LOGFILE_NAME) 
        influencers_list = tryFunctionNTimes(LOGFILE_NAME, 10, influencers.getInfluencers, [acquisition_datetime])
        tryFunctionNTimes(LOGFILE_NAME, 5, mongo.writeMany, [INFLUENCERS_COLLECTION, influencers_list])
        tryFunctionNTimes(LOGFILE_NAME, 5, mongo.writeLog, [TYPE, "influencers-acquisition", acquisition_datetime])

    if TYPE == "STORICAL":

        # Check if the ansa articles acquisition has already been done
        lastLog = tryFunctionNTimes(LOGFILE_NAME, 5, mongo.findLastLog, [{"mode":TYPE, "action":"ansa-acquisition"}])
        if lastLog is not None:
            printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - ansa articles already acquisited at {}".format(lastLog["datetime"]))
        else:
            printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - first ansa acquisition or last failed")
            # TODO single storical start datatime 
            days = (datetime.datetime.now() - datetime.datetime(2022,1,1)).days
            ansaAcquisition(LOGFILE_NAME, influencers_list, mongo, days, acquisition_datetime)
            tryFunctionNTimes(LOGFILE_NAME, 5, mongo.writeLog, [TYPE, "ansa-acquisition", acquisition_datetime])
        
        # Check if the instagram data acquisition has already been done
        lastLog = tryFunctionNTimes(LOGFILE_NAME, 5, mongo.findLastLog, [{"mode":TYPE, "action":"instagram-acquisition"}])
        if lastLog is not None:
            printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - instagram data already acquisited at {}".format(lastLog["datetime"]))
        else:
            printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - first instagram data acquisition or last failed")
            storicalInstagramAcquisition(LOGFILE_NAME, influencers_list, mongo, acquisition_datetime)
            tryFunctionNTimes(LOGFILE_NAME, 5, mongo.writeLog, [TYPE, "instagram-acquisition", acquisition_datetime])

        # Check if the trends data acquisition has already been done
        lastLog = tryFunctionNTimes(LOGFILE_NAME, 5, mongo.findLastLog, [{"mode":TYPE, "action":"trends-acquisition"}])
        if lastLog is not None:
            printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - trends data already acquisited at {}".format(lastLog["datetime"]))
        else:
            printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - first trends data acquisition or last failed")
            storicalTrendsAcquisition(LOGFILE_NAME, influencers_list, mongo, acquisition_datetime)
            tryFunctionNTimes(LOGFILE_NAME, 5, mongo.writeLog, [TYPE, "trends-acquisition", acquisition_datetime])


    elif TYPE == "SERVICE":

        # Check if the ansa articles acquisition has already been done in the last 24h
        lastLog = tryFunctionNTimes(LOGFILE_NAME, 5, mongo.findLastLog, [{"action":"ansa-acquisition"}])
        if lastLog is None:
            printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - waiting for storical data acquisition")
        else:
            missing_days = (datetime.datetime.now() - lastLog["datetime"]).days
            if missing_days < 1:
                printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - ansa articles already acquisited at {}".format(lastLog["datetime"]))
            else:
                ansaAcquisition(LOGFILE_NAME, influencers_list, mongo, missing_days, acquisition_datetime)
                tryFunctionNTimes(LOGFILE_NAME, 5, mongo.writeLog, [TYPE, "ansa-acquisition", acquisition_datetime])

        printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - end at {}".format(datetime.datetime.now()))

        # Check if the instagram data acquisition has already been done
        lastLog = tryFunctionNTimes(LOGFILE_NAME, 5, mongo.findLastLog, [{"action":"instagram-acquisition"}])
        if lastLog is None:
            printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - waiting for storical data acquisition")
        else:
            missing_days = (datetime.datetime.now() - lastLog["datetime"]).days
            if missing_days < 1:
                printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - instagram data already acquisited at {}".format(lastLog["datetime"]))
            else:
                instagramAcquisition(LOGFILE_NAME, influencers_list, mongo, acquisition_datetime)
                tryFunctionNTimes(LOGFILE_NAME, 5, mongo.writeLog, [TYPE, "instagram-acquisition", acquisition_datetime])
        
        # Check if the trends data acquisition has already been done
        lastLog = tryFunctionNTimes(LOGFILE_NAME, 5, mongo.findLastLog, [{"action":"trends-acquisition"}])
        if lastLog is None:
            printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - waiting for storical data acquisition")
        else:
            missing_weeks = (datetime.datetime.now() - lastLog["datetime"]).days // 7
            if missing_weeks < 1:
                printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - trends data already acquisited at {}".format(lastLog["datetime"]))
            else:
                trendsAcquisition(LOGFILE_NAME, influencers_list, mongo, missing_weeks, acquisition_datetime)
                tryFunctionNTimes(LOGFILE_NAME, 5, mongo.writeLog, [TYPE, "trends-acquisition", acquisition_datetime])
        
        time.sleep(3660)
    
    else:
        # DEBUG
        pass

    printAndLog(LOGFILE_NAME, "[*] DATA ACQUISITION - {} - end at {}".format(TYPE, datetime.datetime.now()))
             

def ansaAcquisition(logfile_name, influencers_list, mongo, days, acquisition_datetime):
    ansa = AnsaAcquisition(logfile_name)
    for influencer in influencers_list:
        influencers_articles = tryFunctionNTimes(logfile_name, 10, ansa.getAnsaArticles, [influencer["names"], days, acquisition_datetime])
        if len(influencers_articles) != 0:
            #TODO aggiungere controllo last time 
            tryFunctionNTimes(logfile_name, 5, mongo.writeMany, [NEWS_COLLECTION, influencers_articles])


def instagramAcquisition(logfile_name, influencers_list, mongo, acquisition_datetime):
    instagram = InstagramAcquisition(logfile_name)
    for influencer in influencers_list:
        instagram_data = tryFunctionNTimes(logfile_name, 10, instagram.getInstagramData, [influencer["username"], acquisition_datetime, INSTAGRAM_COOKIES])
        if instagram_data != {}:
            tryFunctionNTimes(logfile_name, 5, mongo.writeOnce, [INSTAGRAM_COLLECTION, instagram_data])

def storicalInstagramAcquisition(logfile_name, influencers_list, mongo, acquisition_datetime):
    instagram = InstagramAcquisition(logfile_name)
    for influencer in influencers_list:
        instagram_data = tryFunctionNTimes(logfile_name, 10, instagram.getStoricalInstagramData, [influencer["username"], acquisition_datetime])
        if len(instagram_data) != 0:
            tryFunctionNTimes(logfile_name, 5, mongo.writeMany, [INSTAGRAM_COLLECTION, instagram_data])


def trendsAcquisition(logfile_name, influencers_list, mongo, weeks, acquisition_datetime):
    trends = TrendsAcquisition(logfile_name)
    for influencer in influencers_list:
        trends_data = tryFunctionNTimes(logfile_name, 20, trends.getTrendData, [influencer["names"], weeks, acquisition_datetime])
        time.sleep(1)
        if len(trends_data) != 0:
            tryFunctionNTimes(logfile_name, 5, mongo.writeMany, [TREND_COLLECTION, trends_data])

def storicalTrendsAcquisition(logfile_name, influencers_list, mongo, acquisition_datetime):
    trends = TrendsAcquisition(logfile_name)
    for influencer in influencers_list:
        trends_data = tryFunctionNTimes(logfile_name, 20, trends.getStoricalTrendData, [influencer["names"], acquisition_datetime])
        time.sleep(1)
        if len(trends_data) != 0:
            tryFunctionNTimes(logfile_name, 5, mongo.writeMany, [TREND_COLLECTION, trends_data])



if __name__ == "__main__":
    main()