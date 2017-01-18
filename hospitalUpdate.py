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
                log.loggingInfo('Unable to update Multicare fax number' + e)

def updateUW():
    uw_url = 'http://www.uwmedicine.org/patient-resources/medical-records'
    uw = requests.get(uw_url)
    uw_bs = BeautifulSoup(uw.text, 'html.parser')
    p_tags = uw_bs.findAll('p')
    tags = []
    for p in p_tags:
        br_tag = p.findAll('br')
        for br in br_tag:
            if 'Fax' in br.text:
                tags.append(br.text)
                try:
                    return tags[0].replace('Fax', ',').replace('Phone', ',').replace(':', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '').split(',')[2]
                except Exception as e:
                    log.loggingInfo('Unable to update UW fax number' + e)

def updateSeaMar():
    base_url = 'http://www.seamarchc.org/static_pages/contactus.php'
    seamar = requests.get(base_url)
    seamar_bs = BeautifulSoup(seamar.text, 'html.parser')
    tags = seamar_bs.findAll('span',{'class':'Estilo115'})
    b_tags = []
    for b in tags:
        b_tags.append(b.text.replace('\n\n', ','))
        b_tags_sstripped = []
        for b in b_tags:
            b_tags_sstripped = b.strip().split(',')
            b_tags_final = []
            for b in b_tags_sstripped:
                if 'Medical Records' in b:
                    b_tags_final = b.replace('-', '').split()
                    return b_tags_final[len(b_tags_final) -1]
