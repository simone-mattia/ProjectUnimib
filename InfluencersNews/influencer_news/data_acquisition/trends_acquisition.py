import itertools, datetime, sys
sys.path.append("../utils")
from utils.utils import printAndLog, printAndLogError
import pandas as pd
from pytrends.request import TrendReq


class TrendsAcquisition:

    '''
    TrendsAcquisition init function:
    - print banner
    - set logfile name
    '''
    def __init__(self, logfile_name):
        self.printBanner()
        self.logfile_name = logfile_name


    def printBanner(self):
        print("""
  _______                 _                               _     _ _   _             
 |__   __|               | |         /\                  (_)   (_) | (_)            
    | |_ __ ___ _ __   __| |___     /  \   ___ __ _ _   _ _ ___ _| |_ _  ___  _ __  
    | | '__/ _ \ '_ \ / _` / __|   / /\ \ / __/ _` | | | | / __| | __| |/ _ \| '_ \ 
    | | | |  __/ | | | (_| \__ \  / ____ \ (_| (_| | |_| | \__ \ | |_| | (_) | | | |
    |_|_|  \___|_| |_|\__,_|___/ /_/    \_\___\__, |\__,_|_|___/_|\__|_|\___/|_| |_|
                                                 | |                                
                                                 |_|                                                        
        """)


    '''
    Given a list of names return the list of max google trend index for each week since 2022-01-01
    '''
    def getStoricalTrendData(self, args):

        URL = "https://www.ansa.it/ricerca/ansait/search.shtml"
        trends_data = []

        try:
            printAndLog(self.logfile_name, "[*] trendsAcquisition.getStoricalTrendData(names)")

            names = args[0]
            acquisition_datetime = args[1]

            pytrend = TrendReq(hl='it-IT',geo = 'IT', timeout=(3.05,27), retries = 2, backoff_factor = 0.2)
            pytrend.build_payload(kw_list = names, timeframe='2022-01-01 {}'.format(str(datetime.datetime.now().date())))
            df = pytrend.interest_over_time()

            if df.shape[0] != 0:

                df['week'] = df.index#strftime("%Y-%m-%d")
                df['username'] = names[0]
                df['max_trend'] = df[names].apply(max, axis=1)
                df['acquisition_datetime'] = acquisition_datetime
                df = df[['week', 'username','max_trend', 'acquisition_datetime']]

            else: # if no data available -> "fake" dataframe

                weeks = pd.date_range(start='2022-01-02', end =str(datetime.datetime.now().date()), freq='W')
                #creating pandas Series with date index
                s = pd.Series(weeks)
                data = {
                    'week':s,
                    'username':list(itertools.repeat(names[0], len(s))),
                    'max_trend':list(itertools.repeat(0, len(s))),
                    'acquisition_datetime':list(itertools.repeat(acquisition_datetime, len(s)))
                }
                #datetime.datetime.strptime(s, "%Y-%m-%d")
                df = pd.DataFrame(data)

            printAndLog(self.logfile_name, "[+] trends data for {}".format(names[0]))
            return df.to_dict('records')
        
        except Exception as e:
            printAndLogError(self.logfile_name, "[-] trendsAcquisition.getStoricalTrendData(names, acquisition_datetime) - error message: {}".format(str(e)))
            return -1

    '''
    Given a list of names return the list of max google trend index for the last X week, passed as parameter 
    '''
    def getTrendData(self, args):

            try:
                printAndLog(self.logfile_name, "[*] trendsAcquisition.getTrendData(names, days)")

                names = args[0]
                weeks = args[1]
                acquisition_datetime = args[2]

                all_data = self.getStoricalTrendData([names, acquisition_datetime])
                if all_data == -1:
                    return -1
                else:
                    return all_data[len(all_data) - weeks:]

            
            except Exception as e:
                printAndLogError(self.logfile_name, "[-] trendsAcquisition.getTrendData(names, days) - error message: {}".format(str(e)))
                return -1