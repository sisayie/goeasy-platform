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

