

import random
did=[]
did1=[]
r=open('names.csv','r').read().splitlines()
for i in r:
    did.append(i.split(',')[0])

r=open('lastnames.csv','r').read().splitlines()
for i in r:
    did1.append(i.split(',')[0])

def fol2_name():
    return did[random.randint(0,12538)] +' '+did1[random.randint(0,1356)]+' '+did[random.randint(0,12538)]

def fol_name():
    return did[random.randint(0,12538)] +' '+did1[random.randint(0,1356)]

def fers_name():
    return did[random.randint(0,12538)]

def fers_fers_name():
    nam=did[random.randint(0,12538)] +' '+did[random.randint(0,12538)]
    return nam
def lsit_name():
    return did1[random.randint(0,1356)]
