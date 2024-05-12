
import os
try:

    import indian_names
    from chinesename import ChineseName
    from vn_fullname_generator import generator
    from korean_name_generator import namer
    from russian_names import RussianNames
except:
    os.system('python3.9 -m pip install --upgrade pip')
    os.system('pip install chinesename')
    os.system('pip install vn-fullname-generator')
    os.system('pip install indian-names')
    os.system('pip install korean-name-generator')
    os.system('pip install russian-names')

def Russian():
    return RussianNames

def korean():
    return namer
def vn_fullname():
    return generator
def Chines():
    return ChineseName
def indian():
    return indian_names