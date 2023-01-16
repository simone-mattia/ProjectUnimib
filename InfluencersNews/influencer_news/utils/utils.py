import datetime, sys, time

'''
Given a message and a logfile name:
- print it on the screen
- log into the indicated file (.log)
'''
def printAndLog(logfile_name, message):

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print("{} - {}".format(date, message))

    with open(sys.path[0] + "/logs/{}.log".format(logfile_name),"a") as logfile:
        logfile.write("{} - {}\n".format(date, message))


'''
Given a message and a logfile name:
- print it on the screen
- log into the indicated file (both in .log and .error)
'''
def printAndLogError(logfile_name, message):

    printAndLog(logfile_name, message)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(sys.path[0] + "/logs/{}.error".format(logfile_name),"a") as logfile:
        logfile.write("{} - {}\n".format(date, message))


'''
Given a number n, a function and the argument of the funcion
Try executing a function, with its args, until it succeeds:
- if it successful return the function ouput
- if it fails doubles sleep times
- after n attempts terminate execution with -1
'''
def tryFunctionNTimes(logfile_name, n, function, args):

    function_result = -1
    sleep_time = 1 
    count = 1

    if args == []:
        function_result = function()
    else:
        function_result = function(args)
    
    while function_result == -1:

        time.sleep(sleep_time)
        
        if args == []:
            function_result = function()
        else:
            function_result = function(args)

        sleep_time *= 2
        count += 1

        if count == n:
            printAndLog(logfile_name, "[!] error in {}".format(str(function)))
            sys.exit(-1)
    
    return function_result

'''
Print banner
'''
def printBanner():
    print(
'''
 /$$$$$$            /$$$$$$  /$$                                                                             /$$   /$$                                  
|_  $$_/           /$$__  $$| $$                                                                            | $$$ | $$                                  
  | $$   /$$$$$$$ | $$  \__/| $$ /$$   /$$  /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$$      | $$$$| $$  /$$$$$$  /$$  /$$  /$$  /$$$$$$$
  | $$  | $$__  $$| $$$$    | $$| $$  | $$ /$$__  $$| $$__  $$ /$$_____/ /$$__  $$ /$$__  $$ /$$_____/      | $$ $$ $$ /$$__  $$| $$ | $$ | $$ /$$_____/
  | $$  | $$  \ $$| $$_/    | $$| $$  | $$| $$$$$$$$| $$  \ $$| $$      | $$$$$$$$| $$  \__/|  $$$$$$       | $$  $$$$| $$$$$$$$| $$ | $$ | $$|  $$$$$$ 
  | $$  | $$  | $$| $$      | $$| $$  | $$| $$_____/| $$  | $$| $$      | $$_____/| $$       \____  $$      | $$\  $$$| $$_____/| $$ | $$ | $$ \____  $$
 /$$$$$$| $$  | $$| $$      | $$|  $$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$| $$       /$$$$$$$/      | $$ \  $$|  $$$$$$$|  $$$$$/$$$$/ /$$$$$$$/
|______/|__/  |__/|__/      |__/ \______/  \_______/|__/  |__/ \_______/ \_______/|__/      |_______/       |__/  \__/ \_______/ \_____/\___/ |_______/                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
''')