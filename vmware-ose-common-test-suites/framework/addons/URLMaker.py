# -*- coding:utf-8 -*-

###################################################
#Function: make the API request URL
#Input: protocal, host, interface
#Output: API URL
###################################################


from framework import TestLog

class URLMaker():

    def __init__(self):

        self.name = "URLMaker"

    _default_host = "127.0.0.1"
    _default_interface = "/"

    def make_httpurl(self, host=_default_host, port="", interface=_default_interface):

        self.logger = TestLog().getlog()

        if host == "":

            self.logger.error("Please input your host")

        elif interface == "":

            self.logger.error("Please input your interface")

        elif port == "":

            self.request_interface = "http://" + str(host) + str(interface)
            self.logger.info("The Interface URL is " + self.request_interface)

            return self.request_interface

        elif port == 80:
            self.request_interface = "http://" + str(host) + str(interface)
            self.logger.info("The Interface URL is " + self.request_interface)

        else:

            self.request_interface = "http://" + str(host) + ":" + str(port) + str(interface)
            self.logger.info("The Interface URL is " + self.request_interface)

            return self.request_interface

    def make_httpsurl(self, host=_default_host, port="", interface=_default_interface):

        self.logger = TestLog().getlog()

        if host == "":

            self.logger.error("Please input your host")

        elif interface == "":

            self.logger.error("Please input your interface")

        elif port == "":

            self.request_interface = "https://" + str(host) + str(interface)
            self.logger.info("The Interface URL is " + self.request_interface)

            return self.request_interface

        elif port == 443:
            self.request_interface = "https://" + str(host) + str(interface)
            self.logger.info("The Interface URL is " + self.request_interface)

        else:
            self.request_interface = "https://" + str(host) + ":" + str(port) + str(interface)
            self.logger.info("The Interface URL is " + self.request_interface)

        return self.request_interface
