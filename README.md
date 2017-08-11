# **Running ZAP in a Robot Framework**

-----------------------

## What is this repository for ?

* Resources files that allows run Security tests using OWASP ZAP (https://www.owasp.org/) in Robot Framework Automation test

-----------------------

## How do I get set up?
### Is needed some depending libraries, that can be installed, through pip:

    The ZAP api can be downloaded from PyPI (download link in The ZAP API page) or it can be installed using:

    pip install python-owasp-zap-v2.4


### Download these files and run this command:

    python setup.py install

-----------------------
### Robot variables that should be adjusted for test

* These variables should be used to the project context.

| Variables  |Example |Information   |
|---|---|---|
| @{risk_alerts}  | ``` Medium     High ```| Risk list alert, can be configured by adding or remove alerts from this set _[Low,Medium,High]_, don´t forget the python tabulation between each risk alert  |
| ${ZAP_HOST}  |  localhost | Host where the ZAP will retrive all Request and Responses|
| ${ZAP_PORT}  |  9090 |Host PORT for ZAP|
| ${ZAP_PATH}  | (WIN) C:\\OWASP\\ZedAttackProxy   | Directory where the zap executable is placed.|
| ${ZAP_REPORT_PATH}|    C:\\testing\\RF_ZAP\\rf\\ZAPlogs |Directory where the zap logs are placed.
| ${API_KEY}    |  ${EMPTY} | API key is required by default in order to invoke any of the API operations. This is a security feature to prevent malicious sites from invoking the ZAP API. Can be retrieved/removed in OWASP ZAP bym accessing *Tools> API*.


### Robot Keywords that can be used:
| Keyword  |Argument/Return |    |
|---|---|---|
|Start Headless ZAP||Start OWASP ZAP without GUI|
|Create New Session ZAP||Creates a new session|
|Perform URL Active Scan| *[Arguments]*: URL|Runs the active scanner against the given URL|
|Get Zap Alerts| *[Arguments]*: URL *[Return]*:Alert list|Returns in JSON format, all alerts raised by ZAP, filtered by URL|
|Get Zap Alert Total| *[Arguments]*: URL *[Return]*:Alert quantity |Returns as integer quantity of alerts raised by ZAP|
|Get Zap Sites| *[Return]*:Sites | Returns in JSON format, a list of sites accessed by ZAP during the scan.
|Get Zap Html Report| *[Return]*:Html Format | Returns in Html format, the Report of the ZAP scan
|Shutdown ZAP|    |  Use to Shutdown Zap application|
|Set Firefox proxy|*[Arguments]*:Host , Port| Configure a Firefox profile to be able to run a Firefox Browser instance that allows  redirect all Request and Reponses to ZAP application to the Host:Port
|Set Chorme proxy|*[Arguments]*:Host , Port| Configure a Chrome browser to be able to run a Browser instance that allows  redirect all Request and Reponses to ZAP application to the Host:Port


### Usage

#### To perform security usually is needed follow these step:
* Start Headless ZAP
* Open a Browser that redirect all request to the ZAP proxy to the site to be run ZAP security test;
* Navigate the web application until reach the step that want to test: Page, Field, Form...
* Create a ZAP new session
* Perform a successful test
* Perform URL Active Scan
* Get Zap Alerts
* Run the ZAP alert

#### Here is an example in Robot Framework of how to use this Resource, to test security issue in a Form:
```python
Start Headless      ZAP
Open URL in Firefox with ZAP proxy    ${URL}
Wait Until Element Is Visible    ${urlLogo}
Login in Page
Go to Form
Create New Session ZAP
Input text      ${form}     admin
Perform URL Active Scan 		${URL}
@{ALERTS}=    	Get Zap Alerts   ${URL}
Shutdown ZAP
```

-----------------------

### Who do I talk to?

* Vitor Aires // vapereira@criticalsoftware.com

### Todo
* Beta testing;