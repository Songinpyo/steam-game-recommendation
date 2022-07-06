import requests
import time
import pandas as pd

def get_reviews(appid, params={'json': 1}):
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url + str(appid), params=params, headers={'User-Agent': 'Mozilla/5.0'})
    return response.json()

def get_n_reviews(appid, n=100):
    reviews = []
    cursor = '*'
    params = {
        'json': 1,
        'filter': 'all',
        'language': 'koreana',
        'day_range': 9223372036854775807,
        'review_type': 'all',
        'purchase_type': 'all'
    }

    while n > 0:
        time.sleep(2)
        params['cursor'] = cursor.encode()
        params['num_per_page'] = min(100, n)
        n -= 100

        response = get_reviews(appid, params)
        cursor = response['cursor']
        reviews += response['reviews']

        if len(response['reviews']) < 100: break

    return reviews

data = pd.read_csv('steam_games_information.csv')
game = data['game']
appid = data['appid']

review_df = pd.DataFrame() # 모든 게임들의 리뷰를 담을 DF

for i in range(len(data['appid'])):
    df_reviews = []
    df_voted_up = []

    # 100개의 리뷰 수집
    reviews = get_n_reviews(appid[i], n=100)
    for j in range(100):
        try:
            df_reviews.append(reviews[j]['review'])
            df_voted_up.append(reviews[j]['voted_up'])
        except:
            pass

    df = pd.DataFrame({'reviews': df_reviews, 'voted_up':df_voted_up})
    
    # 리뷰 수에 맞추어 추천 여부와 게임 이름과 id를 넣어준다.
    df['game'] = data['game'][i]
    df['appid'] = data['appid'][i]

    review_df = pd.concat([review_df, df], ignore_index=True)

# voted up column one hot encoding, Ture=1, False=0
for i in range(len(review_df)):
    if review_df['voted_up'][i] == 'True':
        review_df['voted_up'][i] = 1
    else:
        review_df['voted_up'][i] = 0

review_df.to_csv('steam_games_review.csv', index=False, encoding="utf-8-sig")