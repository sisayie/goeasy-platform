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
import requests

def postJourneyTP(journey):
    url = 'http://172.19.0.6/route'
    headers = {"Accept": "application/json"}
    # call get service with headers and params
    response = requests.post(url,data = journey, headers=headers)
    # respons OK, update tpmmd in db
	
############### 3 ################3
import requests
def getTPMM(journeyId):
    url = 'https://galileocloud.goeasyproject.eu/LBS/route/'+journeyId
    headers = {"Accept": "application/json"}
    # call get service with headers and params
    response = requests.get(url, headers=headers)

'''def getBatchTPMMD():
    get all journeys with tpmmd ==2 (journeys that are sent but do not have tpmm)
    iterate to get the journeys from tpmmd
    tpmm = getTPMM()
    '''