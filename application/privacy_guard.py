from random import randint

def rangen():
    value = randint(1000000,9999999)
    return value

def anonymize(adict, k, v):
    for key in adict.keys():
        if key == k:
            adict[key] = v
        elif type(adict[key]) is dict:
            anonymize(adict[key], k, v)
    return adict
    
def enc_journey(enc_keys):
    #key: journeyId, value: tp_key
    if enc_keys is not None:
        '''my_dict = {}
        for item in enc_keys:
            my_dict[item[0]] = item[1]
        for item in enc_keys:
            item['journeyId'] = item['tp_key']
            item.pop('tp_key')'''
        for enc_key in enc_keys:
            my_dict = dict(enc_key.__dict__)
            my_dict.pop('_sa_instance_state', None)
            my_dict['journeyId'] = my_dict['tp_key']
            my_dict.pop('tp_key')
    else:
        my_dict = {}
    return my_dict