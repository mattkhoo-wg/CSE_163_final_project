import requests
import json
import pandas as pd


def build_df():
    #countries of interest
    countries = ['GB', 'US', 'FR', 'ID', 'KE', 'NG', 'DE', 'KR', 'AU', 'JP', 'ES', 'CZ', 'PH', 'CA', 'RU', 'MX', 'IT']
    video_df = {'id' : [], 'country' : [], 'title' : [], 'category' : [], 'views' : [], 'likes' : [], 'dislikes' : [], 'comment_count' : []}
    #get video Id from API, 50 most popular videos
    for country in countries:
        parameters = {
            'part' : 'statistics,snippet',
            'chart' : 'mostPopular',
            'maxResults' : 1, #ranges from 1-50
            'regionCode' : country
        }
        videos = requests.get("https://www.googleapis.com/youtube/v3/videos?key=your_api_code", params=parameters)
        videos = videos.json()
        items = videos['items']
        print(items)
        #add video information to dictionary
        for video in items:
            video_df['id'].append(video['id'])
            video_df['country'].append(country)
            video_df['title'].append(video['snippet']['title'])
            video_df['category'].append(video['snippet']['categoryId'])
            video_df['views'].append(video['statistics']['viewCount'])
            video_df['likes'].append(video['statistics']['likeCount'])
            video_df['dislikes'].append(video['statistics']['dislikeCount'])
            if 'commentCount' not in video['statistics']:
                video_df['comment_count'].append('na')
            else:
                video_df['comment_count'].append(video['statistics']['commentCount'])
    video_df = pd.DataFrame(video_df)
    print(video_df)
    return video_df

def build_categories_df(country):
    categories_df = {'id' : [], 'category': []}
    parameters = {
        'part' : 'snippet',
        'regionCode' : country
    }
    cat = requests.get('https://www.googleapis.com/youtube/v3/videoCategories?key=your_api_code', params=parameters)
    cat = cat.json()
    items = cat['items']
    for category in items:
        categories_df['id'].append(category['id'])
        categories_df['category'].append(category['snippet']['title'])
    categories_df = pd.DataFrame(categories_df)
    return categories_df

def main():
    videos_df = build_df()
    #categories_df = build_categories_df('US')
      
if __name__ == '__main__':
    main()