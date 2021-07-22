# -*- coding:utf-8 -*-

###########################################
#Function: Logging for testing
#Input: None
#Output: Logging to stdout and log file,
#        log file will be named by execute time, log path will be execute current path
###########################################


import logging
import os
import time
import threading


class TestLog():
    lock = threading.Lock()

    def __init__(self):

        self.name = "Testlog"

    _default_logname = "API_Test"

    def getlog(self, log_name=_default_logname):

        #set log level. log path and save the log to file

        # create logger
        TestLog.lock.acquire()
        self.logger = logging.getLogger()

        self.log_time = time.strftime("%Y-%m-%d-%H-%M-%S")

        if not len(self.logger.handlers):
            self.logger.setLevel(logging.DEBUG)
            # create file log handler
            self.log_path = os.getcwd()

            if os.path.exists(self.log_path + "/logs") == False:
                os.system("mkdir logs")

            self.log_name = self.log_path + "/logs/" + log_name + '@' + self.log_time + '.log'

            #fh = logging.FileHandler(self.log_name, 'a')  # append python2
            fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # append python3
            fh.setLevel(logging.DEBUG)

            # create handler，to output to console
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            # define handler output formart
            formatter = logging.Formatter(
                '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # add the handler to logger
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

            # remover the handler after record the log
            #self.logger.removeHandler(ch)
            #self.logger.removeHandler(fh)
            # close the log file
            fh.close()
            ch.close()

        TestLog.lock.release()
        return self.logger