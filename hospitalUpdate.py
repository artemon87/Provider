import requests
from bs4 import BeautifulSoup
import log

def updateSwedish():
    swedish_url = base_url = 'http://www.swedish.org/patient-visitor-info/medical-records'
    sw = requests.get(swedish_url)
    swedish_bs = BeautifulSoup(sw.text, 'html.parser')
    p_tags = swedish_bs.findAll('p')
    tags = []
    all_tags = []
    for p in p_tags:
        if 'FAX' in p.text:
            tags.append(p.text)
    try:
        tag = tags[0].split('\n')
        for t in tag:
            if 'FAX' in t:
                return t.split(' ')[1].replace('-', '')
    except Exception as e:
        log.loggingInfo(e)

def updateMulticare():
    multicare_url = 'https://www.multicare.org/medical-records/'
    mc = requests.get(multicare_url)
    multicare_bs = BeautifulSoup(mc.text, 'html.parser')
    li_tags = multicare_bs.findAll('li')
    tags = []
    for li in li_tags:
        if 'Fax' in li.text:
            try:
                tag = li.findAll('br')[0].text
                tags.append(tag.strip('\n\r\t -').replace('-', '')[:10])
                print(tags[0])
                return tags[0]            
            except Exception as e:
                log.loggingInfo(e)
    
    
