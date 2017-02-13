import requests
from bs4 import BeautifulSoup
from collections import namedtuple

def findAllHospitals():
    HL = namedtuple('HL',  'Name Address City State Zip Phone Fax Link')
    url_list = []
    business_info = []
    list_of_all = []
    url = 'http://www.wsha.org/for-patients/find-a-hospital'
    hosp_url = requests.get(url)
    hosp_bs = BeautifulSoup(hosp_url.text, 'html.parser')
    providers = hosp_bs.find_all('table', {'id': 'find-hospital-list'})
    #print(providers)
    for elem in providers:
        provider = elem.findAll('tr')
        for tag in provider:
            try:
                providerURL = tag.a['href']
                providerName = tag.findAll('td')[0].text
                url_list.append(providerURL)
            except Exception as e:
                print(e)
        base_url = 'http://www.wsha.org'
        for i in url_list:
            new_url = base_url+i
            url = requests.get(new_url)
            url_bs = BeautifulSoup(url.text, 'html.parser')
            hosp_name = url_bs.find_all('h1', {'class':'entry-title'})[0].text
            hosp_inf = url_bs.find_all('div', {'class':'col-sm-5'})
            for tag in hosp_inf:
                p_tag = tag.findAll('p')
                loop = 0
                for p in p_tag:
                    phone = fax = website = 'NONE'
                    if 'br' in str(p):
                        index = p.getText().strip(' \n\t\r').replace('\r', '').replace('\t', '').split('\n')
                    if loop == 0:
                        try:
                            if index[0].startswith('Congressional') or index[0].startswith('Phone'):
                                continue
                            else:
                                business_info.append(index[0])
                                address = index[1].split('OR')
                                address = index[1].split('WA')
                                business_info.append(address[0])
                                business_info.append('WA')
                                business_info.append(address[1])
                            #business_info.append(index[1].split())
                            loop += 1
                        except Exception as e:
                            print('My first loop ', index,  e)
                    elif loop == 1:
                        try:
                            if index[0].startswith('Phone'):
                                phone = index[0]
                            elif index[0].startswith('Fax'):
                                fax = index[0]
                            else:
                                phone = 'NONE'
                            business_info.append(phone)
                            if index[1].startswith('http'):
                                website = index[1]

                            
                            if website == 'NONE' and index[2].startswith('Fax'):
                                fax = index[2]
                            elif fax != 'NONE' and website == 'NONE':
                                website = index[2]
                            else:
                                fax = 'NONE'
                            business_info.append(fax)
                            if website != 'NONE':
                                pass
                            elif fax == 'NONE':
                                website = index[2]
                            elif fax != 'NONE' and len(index) == 3:
                                website = 'NONE'
                            else:
                                website = index[3]
                            business_info.append(website)
                            loop += 1
                        except Exception as e:
                            print('My second loop ', index,  e)
                    elif loop == 2:
                        loop = 0
                try:
                    inst = HL(hosp_name.upper(),
                              business_info[0].upper(),
                              business_info[1].replace(',', '').upper(),
                              business_info[2].replace(',', '').upper(),
                              business_info[3],
                              business_info[4].replace('Phone: ', '').replace('(', '').replace(') ', '').replace('-', ''),
                              business_info[5].replace('Fax: ', '').replace('(', '').replace(') ', '').replace('-', ''),
                              business_info[6])
                    list_of_all.append(inst)
                    business_info = []
                except Exception as e:
                    print(e)
                
    return list_of_all
    
