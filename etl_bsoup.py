import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
import sqlalchemy
#pip3 install psycopg2

def extract_games(url):
    game_list = []
    tag_list = []
    game_dict = {}

    r = requests.get(url)
    data = r.json()
    data_to_parse = data['results_html']

    soup = BeautifulSoup(data_to_parse, 'html.parser')

    for game in soup.find_all('a'):
        link = re.search('(https://store.steampowered.com/+[a-z]*)+(/[0-9]*)+(/[0-aA-zZ]*)', game['href'])
        print(game['href'])
        game_id = link.group(2).replace('/', '')

        try:
            game_detail = add_label(game['href'])
       

            genre_game = game_detail[1][0] if len(game_detail[1]) > 0 else 'no_genre'
        except:
            game_detail = ['no_user_tags']
            genre_game = ['no_genre']

        print(game_detail)
            
        game_dict = {
            'link': game['href'],
            'id': game_id,
            'name': game.find('span', {'class': 'title'}).text,
            'price': game.find('div', {'class': 'search_price'}).text.strip().split('€')[0],
            'tags': game_detail[0],
            'genre': genre_game
        }

        game_list.append(game_dict)

    return game_list


def add_label(game_url):
    tag_list = []
    tag_r = requests.get(game_url)
    tag_soup = BeautifulSoup(tag_r.content, 'html.parser')

    for label in tag_soup.find_all('a', {'class': 'app_tag'}):
        tag = label.text
        tag = re.sub('([\\r\\n\\t]+)', '', tag)
        tag_list.append(tag)

    detail_list = []
    for detail in tag_soup.find_all('div', {'class': 'details_block'}):
        try:
            genre = detail.find('a').text
            detail_list.append(genre)
        except:
            detail_list = ['No_genre']
    return tag_list, detail_list


def transform(df):

    # check null values
    if df.isnull().values.any():
        raise Exception('There are some missing values')

    return True


if __name__ == "__main__":
    game_data = []

    url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1'

    total_games = requests.get(url).json()['total_count']

    for game in range(0, total_games, 50):
        page_url = f'https://store.steampowered.com/search/results/?query&start={game}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1'

        game_data.append(extract_games(page_url))

    
    game_df = pd.concat([pd.DataFrame(game )for game in game_data])

    if transform(game_df):
        print('Data OK')

    game_df.drop_duplicates(subset=['id'])

    game_df.to_csv('game_data_export.csv', index = False)

    #data = pd.read_csv('game_data_export.csv')

    #load data

    engine = sqlalchemy.create_engine('postgresql://aliescont:c0d1ng@localhost:5432/postgres')
    con = engine.connect()

    table_name = 'games'
    game_df.to_sql(table_name, con, if_exists= 'append', index = False)
    con.close()