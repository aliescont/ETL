import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re

def extract_games(url):
    game_list = []
    tag_list = []
   
    r = requests.get(url)
    data = r.json()
    data_to_parse = data['results_html']

    soup = BeautifulSoup(data_to_parse, 'html.parser')
    
    for game in soup.find_all('a'):
        link = re.search('(https://store.steampowered.com/+[a-z]*)+(/[0-9]*)+(/[aA-zZ]*)', game['href'])

        game_dict = {
            'link' : game['href'],
            'id' : link.group(2).replace('/', '') ,
            'name' : link.group(3).replace('/', ''),
            #'review' : game.find('span', {'class': 'search_review_summary positive'}),
            'tags': add_label(game['href'])
            }
       
        game_list.append(game_dict)
    
    return game_list

def add_label(game_url):
    tag_list = []
    tag_r = requests.get(game_url)
    tag_soup = BeautifulSoup(tag_r.content,'html.parser')

    for label in tag_soup.find_all('a', {'class': 'app_tag'}):
        tag = label.text
        tag = re.sub('([\\r\\n\\t]+)', '', tag)
        tag_list.append(tag)

    return tag_list
     



if __name__ == "__main__":
    game_data = []

    url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1'

    total_games = requests.get(url).json()['total_count']

    for game in range(0, total_games, 50):
        page_url = f'https://store.steampowered.com/search/results/?query&start={game}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1'
        
        game_data.append(extract_games(page_url))
    print(game_data)
    
    game_df = pd.concat([pd.DataFrame(game )for game in game_data])
   
    game_df.to_csv('game_data.csv', index = False)