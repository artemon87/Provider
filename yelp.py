import requests
from bs4 import BeautifulSoup
from collections import namedtuple

def lookup(givenProvider, givenLocation):
    base_url = 'https://www.yelp.com/search?find_desc='
    provider = givenProvider
    location = givenLocation
    pageNumber = 0
    while pageNumber < 200:
        url = base_url + provider + "&find_loc=" + location + "&start=" + str(pageNumber)
        yelp_url = requests.get(url)
        yelp_bs = BeautifulSoup(yelp_url.text, 'html.parser')
        providers = yelp_bs.find_all('div', {'class': 'biz-listing-large'})
        for elem in providers:
            providerName = elem.findAll('a', {'class':'biz-name'})[0].text
            print(providerName)
            try:
                providerAddress = elem.findAll('address')[0].contents
            except Exception as e:
                print(e)
                providerAddress = 'NONE'
            if providerAddress != 'NONE':
                for line in providerAddress:
                    if 'br' in str(line):
                        print(line.getText().strip(' \n\t\r'))
                    else:
                        print(line.strip(' \n\t\r'))
            else:
                print(providerAddress)
            try:
                providerPhone = elem.findAll('span', {'class':'biz-phone'})[0].text
            except Exception as e:
                print(e)
                providerPhone = 'NONE'
            print(providerPhone)
        pageNumber += 10
