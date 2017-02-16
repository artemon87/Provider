import difflib
import log
from difflib import SequenceMatcher

roles = [ '-', "'s",'Health', 'Clinic','Ph.d', 'Ph.D', 'WA', 'Facility', 'MD', 'DC', 'ND', 'LMP', 'Dr', 'Doctor']
roles2 = [ '-', "'s",'Health', 'Medical', 'Center' , 'Hospital','Ph.d', 'Ph.D', 'WA', 'Facility', 'MD', 'DC', 'ND', 'LMP', 'Dr', 'Doctor', 'Imaging ', 'D.C.', 'D.C.,', 'Dr.']


def checkForSpecialties(word, lst):
    for i in lst:
        if i.upper() in word.upper():
            return False
    return True

    
def searchFirstDict(word1, dic):
    for key, val in dic.items():
        for i, j in zip(key.Name.upper(), word1.upper()):
            if i == j:
                continue
            else:
                return []
        return key

def searchFirst(word1, word2):
    for i, j in zip(word1.upper(), word2.upper()):
        if i == j:
            continue
        else:
            return False
    return True
    

def search(s1, s2):
    possibleList = {}
    ss1 = s1.upper().replace('CHIRO', 'CHIROPRACTIC').replace('PT', 'PHYSICAL THERAPY')
    ss2 = s2.upper().replace('CHIRO', 'CHIROPRACTIC').replace('PT', 'PHYSICAL THERAPY')
    for i in roles:
        ss1 = ss1.upper().replace(i.upper(), '')
        ss2 = ss2.upper().replace(i.upper(), '')
    match = SequenceMatcher(None, ss1, ss2).find_longest_match(0, len(ss1), 0, len(ss2))
    if 'CHIROPRACTIC' in ss1 or 'CHIROPRACTIC' in ss2:
        if match.size > 15:
            print(ss1[match.a:match.a+match.size])
            return True
    elif 'PHYSICAL THERAPY' in ss1 or 'PHYSICAL THERAPY' in ss2:
        if match.size > 19:
            print(ss1[match.a:match.a+match.size])
            return True
    elif 'MEDICAL CENTER' in ss1 or 'MEDICAL CENTER' in ss2:
        if match.size > 19:
            print(ss1[match.a:match.a+match.size])
            return True
    elif match.size > 4:
        print(ss1[match.a:match.a+match.size])
        return True
    else:
        return False

def searchRatio(s1, s2, ratio):
    ss1 = s1.upper().replace('CHIRO', 'CHIROPRACTIC').replace('PT', 'PHYSICAL THERAPY')
    ss2 = s2.upper().replace('CHIRO', 'CHIROPRACTIC').replace('PT', 'PHYSICAL THERAPY')
    for i in roles2:
        ss1 = ss1.upper().replace(i.upper(), '')
        ss2 = ss2.upper().replace(i.upper(), '')
    match = SequenceMatcher(None, ss1, ss2)
    if match.ratio() >= ratio:
        #match = match.find_longest_match(0, len(ss1), 0, len(ss2))
        #print(ss1[match.a:match.a+match.size])
        return True
    
    

def deepSearch(word, givenList, maxReturn, accuracy):
    try:
        return difflib.get_close_matches(word.upper(), (elem.Name.upper() for elem in givenList), maxReturn, accuracy)
    except Exception as e:
        log.loggingInfo(e)
