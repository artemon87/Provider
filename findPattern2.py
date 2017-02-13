roles = ['Ph.d', 'Ph.D', 'WA', 'Community', 'Physician', 'Physicians', 'Chiropractic', 'Chiro', 'Medical', 'Center', 'Hospital', 'Facility', 'Clinic', 'MD', 'DC', 'ND', 'LMP', 'Dr', 'Doctor', 'Phys']

def abr(s1, s2):
    for i, j in zip(s1.upper(), s2.upper()):
        if i != j:
            return False
    return True


def search(s1, s2):
    totalMisses = 0
    for i in roles:
        ss1 = s1.replace(i.upper(), '')
        ss2 = s2.replace(i.upper(), '')
    ss1 = (ss1.upper().replace('-', ' ').replace("'", '').replace('.', ' ').replace(',', ' ').split())
    ss2 = (ss2.upper().replace('-', ' ').replace("'", '').replace('.', ' ').replace(',', ' ').split())
    dic = {}
    for i in ss1:
        if i not in dic:
            dic[i] = 1
        else:
            dic[i] += 1
    for i in ss2:
        if i in dic:
            dic[i] -= 1
        else:
            dic[i] = 1
    for key, value in dic:
        if value > 0:
            totalMisses += 1
    if totalMisses > 1:
        pass
    else:
        return s2



            
    ss1 = sorted(ss1)
    ss2 = sorted(ss2)
    for i,j in zip(ss1, ss2):
        matches = abr(s1, s2)
        if matches:
            totalMatches += 1
    minSize = min(len(ss1), len(ss2))
    if totalMatches >= minSize:
        return s2
    elif len(ss2) < 2:
        #return False
        pass
    else:
        return searchMore(s1, s2)



def searchMore(s1, s2):
    ss1 = sorted(s1.upper().replace('-', ' ').replace("'", '').replace('.', ' ').replace(',', ' '))
    ss2 = sorted(s2.upper().replace('-', ' ').replace("'", '').replace('.', ' ').replace(',', ' '))
    misses = 0
    for j, i in zip(ss1, ss2):
        if j != i:
            misses += 1
    if misses > 1:
	    return searchEvenMore(s1, s2)
    else:
	    return s2



def searchEvenMore(s1, s2):
    ss1 = s1.upper()
    ss2 = s2.upper()
    for i in roles:
        ss1 = ss1.replace(i.upper(), '')
        ss2 = ss2.replace(i.upper(), '')
    sss1 = sorted(ss1.replace('-', ' ').replace("'", '').replace('.', ' ').replace(',', ' ').split())
    sss2 = sorted(ss2.replace('-', ' ').replace("'", '').replace('.', ' ').replace(',', ' ').split())
    if sss1 is not []:
        for i, j in zip(sss1, sss2):
            matches = abr(i, j)
            if matches:
                return s2
			    #return True
            else:
                #return False
                pass
    else:
        #return False
        pass

	
