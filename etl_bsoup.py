import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re

def extract_data(url):
    game_list = []
   
    r = requests.get(url)
    data = r.json()
    data_to_parse = data['results_html']

    soup = BeautifulSoup(data_to_parse, 'html.parser')
    
    for game in soup.find_all('a'):
        link = re.search('(https://store.steampowered.com/+[a-z]*)+(/[0-9]*)+(/[aA-zZ]*)', game['href'])

        game_dict = {
            'link' : game['href'],
            'id' : link.group(2).replace('/', '') ,
            'name' : link.group(3).replace('/', '')
            
            }
       
        game_list.append(game_dict)
    
    return game_list

data_extract = extract_data('https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1')
print(data_extract)