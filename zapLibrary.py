#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright 2017 Vitor Aires Pereira <vapereira@criticalsoftware.com>


"""
ZAP Library - Robot keywords to access OWASP ZAP testing library.
"""

import os
import time
from logging import info, warn
from selenium import webdriver
from zapv2 import ZAPv2


class zapLibrary(object):
    """
        Library for running ZAP  messages.

        = Table of contents =

        - `Usage`
        - `Examples`
        - `Importing`
        - `Shortcuts`
        - `Keywords`

        = Usage =

        This library has several keyword, for running OWASP ZAP in Robot Framework.
        OWASP ZAP (Zed Attack Proxy) is an open-source web application security scanner.
        Can be used as a proxy server it allows the user to manipulate all of the traffic that passes through it, including traffic using https.

         To perform security usually is needed follow these steps:
            - Start Headless ZAP.
            - Open a Browser that redirect all request to the ZAP proxy.
            - Navigate the web application until reach the step that want to test.
            - Create a ZAP new session.
            - Perform a successful test.
            - Retrieve all Alerts.
            - Run the ZAP alert.

        = Examples =
        Notice how keywords are linked from examples:

        | `Start Headless Zap`                  |  ${ZAP_PATH}      |       |
        | `Open URL in Firefox with ZAP proxy`  | ${URL}            |       |
        | Wait Until Element Is Visible         | ${urlLogo}        |       |
        | Login in Page                         |                   |       |
        | Go to form                            |                   |       |
        | `Create New Session`                  |                   |       |
        | Input text                            | ${form}           | admin |
        | `Perform in  URL Active scan`         | ${URL}            |       |
        | @{ALERTS}=                            | `Get ZAP Alerts`  | ${URL} |
        | `Create Html Report`                  | @{ALERTS}         |       |
        | `Shutdown ZAP`                        |                   |       |

        = Importing =

            ZAP Library can be imported with 2 argument.

            Arguments:

            - ``apikey ``: API key is required by default in order to invoke any of the API operations.
            This is a security feature to prevent malicious sites from invoking the ZAP API. Can be retrieved/removed
            in OWASP ZAP by accessing *Tools> API*.
            - ``proxy ``: URL where ZAP is listening, in this format http://<host>:<port>


            *Example:*


            | =Setting= |  =Value=   | =Argument= | =Argument= |
            | Library   | ZapLibrary |   apikey   |    proxy   |

        """
    ROBOT_LIBRARY_VERSION = '0.1'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

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

            *Example:*

            | Create New Session |
        """
        print('Create a new Session')
        self.zap.core.new_session()

    def vitor(self):
        print('Create a new Session')

    def perform_url_active_scan(self, url):
        """Runs the active scanner against the given URL and/or Context.
        The scans ends when their status reach 100%

        *Example:*

        | Perform URL active scan | http://<address> |
        """
        info('Begin Active scan {}'.format(url))
        scanid = self.zap.ascan.scan(url)
        info('Scan id: {}'.format(self.zap.ascan.scan(url)))
        while int(self.zap.ascan.status(scanid)) < 100:
            info('Scan progress %: {}'.format(self.zap.ascan.status(scanid)))
            time.sleep(5)
        info("Active scan is complete")

    def get_zap_alerts(self, url):
        """Returns, in JSON format all alerts raised by ZAP, filtering by URL.

         Arguments:

         - ``url``: Url to be scanned, should be in ths format: http(s)://address

         *Example 1:*

         | ${alerts}= | Get Zap Alerts | http://<address> |

         *Example 2:*
         Get all risk types found in Attack scan

         | @{ALERTS}= | Get zap alerts   | ${URL}              |             |      |
         | : FOR      | ${ALERT}         | IN                  | @{ALERTS}   |      |
         |    \\      | ${risk}=         | Get From Dictionary | ${ALERT}    | risk |

         """
        info('Retrieve all alerts')
        return self.zap.core.alerts(url)

    def get_zap_alert_total(self, url):
        """Returns quantity of alerts raised by ZAP, filtering by URL.

        Arguments:

        - ``url``: Url to be scanned, should be in ths format: http(s)://<address>

        *Example:*

        | ${number_of_alerts} = | Get Zap Alert Quantity | ${URL} |
        """
        qtyOfAlerts = int(self.zap.core.number_of_alerts(url))
        info('Retrieve alerts {}'.format(qtyOfAlerts))
        return qtyOfAlerts

    def shutdown_zap(self):
        """Shutdown Zap application
        Examples:
        | Shutdown Zap |
        """
        info("Shutting Down ZAP")
        return self.zap.core.shutdown()

    def get_zap_sites(self):
        """Returns,in JSON format, a list of sites accessed by ZAP during the test.

        *Example:*

        | @{SITES}= | Get zap sites |
        """
        info('Retrieved sites')
        return self.zap.core.sites()

    def get_zap_html_report(self):
        """Returns,in HTML format, the Report of the ZAP scan.

        *Example:*
        Create Html Report
        | [Arguments]       | @{ALERTS}                             |                                   |                   |                   |                                                                               |
        | ${print_html} =   | Set Variable                          | False                             |                   |                   |                                                                               |
        | : for             | ${ALERT}                              | IN                                | @{ALERTS}         |                   |                                                                               |
        | \\                | ${risk}=                              | Get From Dictionary               | ${ALERT}          |   risk            |                                                                               |
        | \\                | Run Keyword If                        | '${risk}' in ['Medium' , 'High']  | Set Test Variable | ${print_html}     |   True                                                                        |
        | ${resp}=          | Get ZAP html Report                   |                                   |                   |                   |                                                                               |
        | Create File       | ${ZAP_REPORT_PATH}/${TEST NAME}.html  |  ${resp}                          |                   |                   |                                                                               |
        | Run Keyword If    | ${print_html}                         |  Fail                             | *HTML*<b>Found Security issues, please see: <a href= "${ZAP_REPORT_PATH}${/}${TEST NAME}.html">See Report</a></b>     |
        | Run Keyword Unless| ${print_html}                         |  Pass Execution                   |  *HTML*<b>Found Security issues, please see: <a href= "${ZAP_REPORT_PATH}${/}${TEST NAME}.html">See Report</a></b>    |

        """
        info('Generated html report')
        return self.zap.core.htmlreport()

    @staticmethod
    def start_headless_zap(path):
        """Start OWASP Zap without gui. Run OWASP ZAP in a daemon mode which is then controlled via a REST Application programming interface.

        Arguments:

        - ``path``: OWASP ZAP path

        *Example:*

        | Start Headless Zap | C:\\OWASP\\ZedAttackProxy |

        | Start Headless Zap | ${ZAP_PATH} |
        """
        try:
            os.chdir(path)
            os.popen('zap -daemon')
            info('ZAP RUNNING')
        except IOError as e:
            warn("The OWASP ZAP path is not correctly configured!")

    @staticmethod
    def set_firefox_proxy(host, port):
        """
        Configure a Firefox profile to be able to run a Firefox Browser instance that allows run redirect all Request and Reponses to ZAP application

        Arguments:

        - ``host``: ZAP Local proxy address
        - ``port``: ZAP Local proxy Port

        *Example:*

        Open Firefox using Zap Proxy
        | [Arguments]       | ${url}            |
        | ${profile}=       | set firefox proxy | ${ZAP_HOST}                |${ZAP_PORT} |
        | Create webdriver  | Firefox           | firefox_profile=${profile} |            |
        | Go to             | ${url}            |                            |            |

        """
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.http', host)
        profile.set_preference('network.proxy.http_port', int(port))
        profile.set_preference('network.proxy.ssl', host)
        profile.set_preference('network.proxy.ssl_port', int(port))
        profile.set_preference('network.proxy.type', 1)
        profile.update_preferences()
        return profile

    @staticmethod
    def set_chrome_proxy(host, port):
        """
        Configure a Chrome options to be able to run a Chrome Browser instance that allows run redirect all Request and Reponses to ZAP application

        Arguments:

        - ``host``: ZAP Local proxy address
        - ``port``: ZAP Local proxy Port

        *Example:*

        Open Chrome Using ZAP proxy
        | [Arguments]       | ${url}            |                           |               |
        | ${options}=       | set chrome proxy  | ${ZAP_HOST}               | ${ZAP_PORT}   |
        | Create WebDriver  | Chrome            | chrome_options=${options} |               |
        | Go To             | ${url}            |                           |               |

        """
        PROXY = host + ":" + port
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        return chrome_options

