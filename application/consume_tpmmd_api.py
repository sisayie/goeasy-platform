#################################################################################
#1. Get a journey from public db
#2. post a journey to TPMM
#3. Get a MM from TPMM using the mapped(journeyId) #use the id of a journey record

#Algorithm:
#if mm staus == not sent:
#    post journey to TPMM(journey)
#     if sent is ok:
#       mm status = sent
#    update mm-sent-statu in db
#    #getTPmm(journeyId)
#else if mm status is sent:
#    getTPMM(mapped(journeyId))

# inlcude sensor data needs to be sent to TPMM. 
# TODO: How can it affect privacy and security of the data subject?

#Db(journey) --> [get(journey)] --> post(journey to tpmmd) --> get (tpmm from TPMMD) --> update db

############  1 #########################33
import requests
from config import *


logger = logging.getLogger(__file__)

def getJourney(journeyId):
    url = 'https://galileocloud.goeasyproject.eu/GEP/paib/publicstorage/'+journeyId
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    return data
    
'''def sendBatchTPMMD():
    get all journeys with tpmmd ==1 (journeys that are not sent)
    iterate to post the journeys to tpmmd
    postJourneyTP(journey)
    '''

############  2  ################################################################


def postJourneyTP(journey):
    from database import update_tpmmd
    #url = 'http://172.19.0.6/route'
    url = 'https://galileocloud.goeasyproject.eu/LBS/route'
    # url = 'http://galileocloud.goeasyproject.eu:8222/route'
    headers = {"Accept": "application/json"}
    # call get service with headers and params
    logger.debug("This is the data posted:\n" + json.dumps( journey, sort_keys=True, indent=4) )
    response = requests.post(url,json= journey, headers=headers)
    logger.debug(f'POST request to TP, response.status_code: {response.status_code}')
    logger.debug(f'POST request to TP, response.text: {response.text}')
    update_tpmmd(journey['journey_id'], 2)  # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 100 < error_code)
    #logger.debug(f'POST request to TP, response.content: {response.content}')
    # respons OK, update tpmmd in db
	
############### 3 ################3


def getTPMM(journeyId):
    from database import update_tpv_behaviour
    url = 'https://galileocloud.goeasyproject.eu/LBS/route/'+journeyId
    headers = {"Accept": "application/json"}
    # call get service with headers and params
    response = requests.get(url, headers=headers)
    logger.debug(f'GET request to TP, response.status_code: {response.status_code}')
    logger.debug(f'GET request to TP, response.text: {response.text}')
    if (response.status_code == requests.codes.ok):
        data = json.loads(response.content)
        update_tpv_behaviour(journeyId, data['tpv_defined'])
        logger.debug("GET request to TP, json.loads(response.content):" + str(data['tpv_defined']))
        logger.debug("GET request to TP, response.content:" + str(response.content))


'''def getBatchTPMMD():
    get all journeys with tpmmd ==2 (journeys that are sent but do not have tpmm)
    iterate to get the journeys from tpmmd
    tpmm = getTPMM()
    '''