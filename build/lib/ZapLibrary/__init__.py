#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright 2017 Vitor Aires <airesv@gmail.com>


"""
ZAP Library - Robot keywords to access OWASP ZAP testing library. 
"""

import os
import time
import json
from logging import debug, error, info, warn
from selenium import webdriver
from zapv2 import ZAPv2


class ZapLibrary(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.0.1'

    def __init__(self, apikey, proxy):
        """ZAP Library can be imported with 2 argument.
        Arguments:
        - ``apikey ``: API key is required by default in order to invoke any of the API operations. 
        This is a security feature to prevent malicious sites from invoking the ZAP API. Can be retrieved/removed
        in OWASP ZAP bym accessing *Tools> API*.
        - ``proxy ``: URL where ZAP is listening, in this format http://<host>:<port>
        Examples:
        | = Keyword Definition =  | = Description =       |
        | Library `|` ZapLibrary | apikey | proxy|
        """
        self.zap = ZAPv2(apikey=apikey, proxies={'http': proxy, 'https': proxy})

    # Create a new Session
    def create_new_session(self):
        """Creates a new session in ZAP, optionally overwriting existing files.
            Examples:
            | Create New Session |
        """
        print('Create a new Session')
        self.zap.core.new_session()

    def perform_URL_active_scan(self, url):
        """Runs the active scanner against the given URL and/or Context. 
        The scans ends when their status reach 100%
        Examples:
        | Perform URL active scan | <URL> |
        """
        print('Begin Active scan {}'.format(url))
        scanid = self.zap.ascan.scan(url)
        print (scanid)
        print(self.zap.ascan.status(scanid))
        while (int(self.zap.ascan.status(scanid)) < 100):
            info('Scan progress %: {}'.format(self.zap.ascan.status(scanid)))
            time.sleep(5)
        info ("Active scan is complete")

    def get_zap_alerts(self, url):
        """Returns, in JSON format all alerts raised by ZAP, filtering by URL. 
        Arguments:
        - ``url``: Url to be scanned, should be in ths format: http(s)://address
        Examples:
        | Get Zap Alerts | url |
        """
        print('Retrieve all alerts')
        #alertsJson =json.dumps(self.zap.core.alerts(url))
        return self.zap.core.alerts(url)

    def get_zap_alert_total(self, url):
        """Returns quantity of alerts raised by ZAP, filtering by URL. 
        Arguments:
        - ``url``: Url to be scanned, should be in ths format: http(s)://address
        Examples:
        | Get Zap Alert Quantity | url |
        """
        qtyOfAlerts = int(self.zap.core.number_of_alerts(url))
        print('Retrieve alerts {}'.format(qtyOfAlerts))
        return qtyOfAlerts

    def shutdown_zap(self):
        """Shutdown Zap application 
        Examples:
        | Shutdown Zap |
        """
        print("Shutdown ZAP")
        return self.zap.core.shutdown()

    def get_zap_sites(self):
        """Returns,in JSON format, a list of sites accessed by ZAP
        Examples:
        | Shutdown Zap |
        """
        print('Retrieved sites')
        return self.zap.core.sites()

    def get_zap_html_report(self):
        """Returns,in JSON format, a list of sites accessed by ZAP
        Examples:
        | Shutdown Zap |
        """
        print('Generated html report')
        return self.zap.core.htmlreport()

    def start_headless_zap(self, path):
        """Start OWASP Zap without gui.
        Examples:
        | Shutdown Zap |
        """

        try:
            os.chdir(path)
            os.popen('zap -daemon')
        except IOError as e:
            print "The OWASP ZAP path is not correctly configured!"

    def set_firefox_proxy(host, port):
        """
        Configure a Firefox profile to be able to run a Firefox Browser instance that allows run redirect all Request and Reponses to ZAP application 
        Arguments:
        - ``host``: ZAP Local proxy address
        - ``port``: ZAP Local proxy Port
        """
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.http', host)
        profile.set_preference('network.proxy.http_port', int(port))
        profile.set_preference('network.proxy.ssl', host)
        profile.set_preference('network.proxy.ssl_port', int(port))
        profile.set_preference('network.proxy.type', 1)
        profile.update_preferences()
        return profile

    def set_chrome_proxy(host, port):
        """
        Configure a Chrome options to be able to run a Chrome Browser instance that allows run redirect all Request and Reponses to ZAP application 
        Arguments:
        - ``host``: ZAP Local proxy address
        - ``port``: ZAP Local proxy Port
        """
        PROXY = host + ":" + port
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        return chrome_options

