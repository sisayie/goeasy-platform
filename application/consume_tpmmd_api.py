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


def postJourneyTP(journey, journeyId): # Original journeyId provided, as the journeyId in the journey is replaces with a new one
    from database import update_tpmmd
    #url = 'http://172.19.0.6/route'
    url = 'https://galileocloud.goeasyproject.eu/LBS/route'
    # url = 'http://galileocloud.goeasyproject.eu:8222/route'
    headers = {"Accept": "application/json"}
    # call get service with headers and params
    #logger.debug("This is the data posted:\n" + json.dumps( journey, sort_keys=True, indent=4) )
    response_status = 1 # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 10XXX-send_error_code, 20XXX-retrive_error_code)
    try: 
        response = requests.post(url,json= journey, headers=headers)
        logger.debug(f'POST request to TP, response.status_code: {response.status_code}')
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        logger.debug(f'POST request to TP, Timeout exception: {response.status_code}')
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        logger.debug(f'POST request to TP, TooManyRedirects exception: {response.status_code}')
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        logger.debug(f'POST request to TP, RequestException exception: {response.status_code}')
    
    if (response.status_code == requests.codes.ok):
        response_status = 2 # detection status: 2-sent,
    else:
        response_status = 10000 + response.status_code  # (10XXX-send_error_code, 20XXX-retrive_error_code)
        logger.debug(f'POST request to TP, response.text: {response.text}')
        #logger.debug(f'POST request to TP, response.content: {response.content}')
        
    update_tpmmd(journeyId, response_status) # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 10XXX-send_error_code, 20XXX-retrive_error_code)
    return response_status
	
############### 3 ################3


def getTPMM(newID, journeyId):
    from database import update_tpv_behaviour
    url = 'https://galileocloud.goeasyproject.eu/LBS/route/'+newID
    headers = {"Accept": "application/json"}
    # call get service with headers and params
    response = requests.get(url, headers=headers)
    logger.debug(f'GET request to TP, response.status_code: {response.status_code}')
    #logger.info(f'GET request to TP, response.text: {response.text}')
    if (response.status_code == requests.codes.ok):
        data = json.loads(response.content)
        update_tpv_behaviour(journeyId, data['tpv_defined'])
        logger.debug("This is the data returned bay the TPMMD:\n" + json.dumps( data, indent=4) )
        #logger.debug("GET request to TP, json.loads(response.content):" + str(data['tpv_defined']))
        #logger.debug("GET request to TP, response.content:" + str(response.content))
    
    return response.status_code

'''def getBatchTPMMD():
    get all journeys with tpmmd ==2 (journeys that are sent but do not have tpmm)
    iterate to get the journeys from tpmmd
    tpmm = getTPMM()
    '''
