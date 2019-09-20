import json
import pandas as pd

with open('data/routes.json') as f:
    sample_data = json.loads(f.read())
#print(sample_data)
## Remove an element from JSON data
#import json
#
#with open('data.json', 'r') as data_file:
#    data = json.load(data_file)
#
#for element in data:
#    element.pop('hours', None)
#
#with open('data.json', 'w') as data_file:
#    data = json.dump(data, data_file)

def is_empty(any_structure): #d = {} # Empty dictionary, l = [] # Empty list, ms = set() # Empty set, s = '' # Empty string, t = () # Empty tuple
    if any_structure: #print('Structure is not empty.')
        return False
    else: #print('Structure is empty.')
        return True
def get_coordinates(data):
    clean_data = []
    for element in sample_data:
        element.pop('data', None)
        element.pop('msgid', None)
        element.pop('status', None)
        element.pop('submsgid', None)
        element.pop('svid', None)
        element.pop('type', None)
        element.pop('time', None)
        if not(is_empty(element)):
            clean_data.append(element)
    return clean_data

#print(data_sample)
clean_data = get_coordinates(sample_data)

#print(clean_data)
data_dict = json.loads(json.dumps(sample_data))
#type(data_dict)
#print(data_dict[0]['lat']) #print(data[<keyFromTheJsonFile>])

df = pd.DataFrame.from_dict(clean_data)
json.dumps(clean_data)
#print(df)
lon = df['lon']
lat = df['lat']