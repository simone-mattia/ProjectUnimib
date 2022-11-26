'''
Simple tool for RDP Brutefoce based on rdesktop-vrdp tool
'''

import sys
import argparse
import random
import time 


class RDPBruteforce():
    def __init__(self):
        self.info = "RDP Brutefoce"
        self.targetIp = ""
        self.domain = ""
        self.targets = []
        self.usernames = []
        self.passwords = []
        self.random = 0
        self.stealth = ""
        self.timeoutTime = 0 


    def brute(self):
        parser = argparse.ArgumentParser(add_help = True, description = "RDP Brutefoce")
        requiredArgs = parser.add_argument_group('Required Arguments')
        requiredArgs.add_argument('-I', dest = 'targetIP', action = "store",required=True,  help= "Target IP Address")
        requiredArgs.add_argument('-U', dest = 'UsernamesFile', action ="store",required=True,   help='Usernames file')
        requiredArgs.add_argument('-P', dest = 'PasswordsFile', action ="store", help="Passwords file")
        requiredArgs.add_argument('-d', dest = 'Domain', action = "store",type=str, default="", help='Domain (Default:"")')
        requiredArgs.add_argument('-p', dest = 'targetPort', action = "store",type=int, default=3389, help='Target Port (Default:3389)')
        requiredArgs.add_argument('-Timeout', dest = 'timeout', action = "store", type=int, default=15, help='Timeout Time')
        requiredArgs.add_argument('-r', dest = 'random', action = "store", type=int, default=0, help='set max random time between 1 and RANDOM for each attemps in ms (Default: 0)')
        requiredArgs.add_argument('-s', dest = 'stealth', action = "store", type=str, default="False", help='If true rotate username-password combinations (Default:False)')

        if len(sys.argv)==1:
           parser.print_help()
           sys.exit(1)
        options = parser.parse_args()

        self.targetIP = options.targetIP
        self.targetPort = options.targetPort
        self.timeoutTime = options.timeout
        self.domain = options.Domain
        self.usernames = self.fileToList(options.UsernamesFile)
        self.passwords = self.fileToList(options.PasswordsFile)
        self.random = options.random/1000
        self.stealth = options.stealth
        self.brute()


    def brute(self):
        print("[*] {}".format(self.info))
        print("Target is : " + self.targetIP + ":" + str(self.targetPort))

        if self.stealth == "True":
            for password in self.passwords:
                for username in self.usernames:
                    self.connectRDP(username, password, self.targetIP, self.targetPort, self.domain)
        else:
            for username in self.usernames:
                for password in self.passwords:
                    self.connectRDP(username, password, self.targetIP, self.targetPort, self.domain)


    def connectRDP(self, username, password, targetIP, targetPort, domain):
        print("TODO")
        # rdesktop -u simon -p myPass123 192.168.1.10


    def fileToList(self, fileName):
            lineList = []

            try:
                fileParser = open(fileName, 'r')
            except IOError:
                print(" Error opening file : " + fileName)
            except:
                print(" Error accessing file : " + fileName)

            for line in fileParser.readlines():
                newLine = line.replace('\n', '')
                lineList.append(newLine)

            return lineList


    def randomTimeOut(max):
        if max != 0:
            time.sleep(random.randint(1,max))


if __name__ == '__main__':
    brute= RDPBruteforce()
    brute.brute()
