# -*- coding: utf-8 -*-
"""
Created on Tue Jul 1 10:20:10 2020

@author: rachev
"""

import threading
import queue
import time
import logging
import asyncio
import uuid

#from database import *
from config import *
from consume_tpmmd_api import *

logger = logging.getLogger(__file__)

sendThread = threading.Thread()
requestThread = threading.Thread()
# delayTread = threading.Thread()
sendQueue = queue.Queue()
requestQueue = queue.Queue()
rescheduledSet = set()
newIDs={}

async def delayedPut(journey, delay=5):
    logger.debug('delayedPut startet, journeyId: ' + journey + " delay: " + delay)
    await asyncio.sleep(delay)
    requestQueue.put(journey)
    logger.debug('journeyId: ' + journey + " has been put in requestQueue")


def tpmmdSender():
    while True:
        try:
            item = sendQueue.get()
            # the item have to be customised
            #  1. rename "positions" to "trace_information"
            #  2. copy "user_defined_behaviour" to "behaviour"{ "user_defined": []}
            #  3. rename "sensors" to "sensors_information"
            #  4. rename "journeyId" to "journey_id"
            item['trace_information'] = item.pop('positions', [])    # 1.
            item['sensors_information'] = item.pop('sensors', [])    # 2.
            item['behaviour'] = {"app_defined": [],"tpv_defined": [],'user_defined': []}    # 3.
            item['behaviour']['user_defined'] = item.get('user_defined_behaviour', [])              # 3.
            item['behaviour']['app_defined'] = item.get('app_defined_behaviour', [])              # 3.
            item['journey_id']= item.pop('journeyId', "")           # 4.

            item.pop('a_behaviour', [])
            item.pop('u_behaviour', [])
            item.pop('t_behaviour', [])
            item.pop('tpv_defined_behaviour', [])
            item.pop('app_defined_behaviour', [])

            # replace 'journey_id' with temporal new ID
            newID = str(uuid.uuid4())
            # atore the new ID in the dictionary
            newIDs[newID]=item['journey_id']
            #replace the 'journey_id' with the newID
            logger.debug('Replacing original journey_id: ' + item['journey_id'] + ' with a newID: ' + newID)
            logger.debug('newIDs size: ' + str( len(newIDs)))
            item['journey_id']=newID
        except KeyError:
            logger.debug("KeyError in queued message for sendQueue.")

        logger.debug('Sending on journeyId:' + item['journey_id'])
        if(postJourneyTP(item, newIDs.get(newID)) == 2):
            time.sleep(0.0005)
            #time.sleep(1/(sendQueue.qsize()+10))
            requestQueue.put(item['journey_id'])
            #delayedPut(item['journey_id'], 3)
        else:
            #do not keep the newID anymore
            newIDs.pop(newID)
            
        logger.debug('Finished sending journeyId:' + item['journey_id'] + ', sendQueue_size: ' 
                     + str(sendQueue.qsize())+ ', requestQueue_size: ' + str(requestQueue.qsize()))
        sendQueue.task_done()


""" def tpmmdRequester():
    logger.debug("Sleeping 50s ")
    time.sleep(50) # do not start immediate as the queue is empty
    while True:
        logger.debug("Sleeping 20s ")
        time.sleep(20)
        size = requestQueue.qsize()
        logger.debug("requestQueue.qsize = " + str(size))
        for i in range(size):
            item = requestQueue.get()
            logger.debug(f'Requesting item {item}')
            if (False): # result returned back 
                requestQueue.put(item)
            logger.debug(f'Requesting Finished {item}')
            requestQueue.task_done() """

def tpmmdRequester():
    logger.debug("starting tpmmdRequester ")
    #time.sleep(50) # do not start immediate as the queue is empty
    lastSize = 0
    while True:
        try:
            item = requestQueue.get()
            ##logger.debug("Sleeping 20s ")
            if item in rescheduledSet:
                logger.debug("Resheduled item detected: " + item)
                logger.debug("Waiting 10s to let the TP finish the sent requests")
                time.sleep(10)
                rescheduledSet.remove(item)

            time.sleep(2) # as the returnet json is empty
            logger.debug(f'Requesting item {item}')
            response_status = getTPMM( item, newIDs.get(item))
            # nttp_get({item['journeyId']})
            if (response_status != requests.codes.ok): # result returned back 
                logger.debug("Bad reply from TP, resheduling item: " + item)
                requestQueue.put(item)
                rescheduledSet.add(item)
                logger.debug("Waiting 10s to let the TP finish the sent requests")
                time.sleep(10)  
            else:
                newIDs.pop(item)
                logger.debug('newIDs size: ' + str( len(newIDs)))  
            requestQueue.task_done() 
        except KeyError:
            logger.debug("KeyError in queued message for requestQueue.")

def startTPMMD():
    logger.debug("Creating sendThread") 
    # turn-on the worker thread
    # if ('sendThread' in locals()) or ('sendThread' in globals()):
    #     logger.debug("sendThread already exists") 
    #     if sendThread.is_alive():
    #         logger.debug("sendThread is alive")  
    sendThread = threading.Thread(target=tpmmdSender, daemon=True)
    sendThread.start()
    logger.debug("sendThread started") 
    logger.debug("Creating requestThread") 
    requestThread = threading.Thread(target=tpmmdRequester, daemon=True)
    requestThread.start()
    logger.debug("requestThread started") 
