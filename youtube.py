import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def build_df():
    #countries of interest
    countries = ['GB', 'US', 'FR', 'ID', 'KE', 'NG', 'DE', 'KR', 'AU', 'JP', 'ES', 'CZ', 'PH', 'CA', 'RU', 'MX', 'IT']
    video_df = {'id' : [], 'country' : [], 'title' : [], 'category' : [], 'views' : [], 'likes' : [], 'dislikes' : [], 'comment_count' : []}
    #get video Id from API, 50 most popular videos
    for country in countries:
        parameters = {
            'part' : 'statistics,snippet',
            'chart' : 'mostPopular',
            'maxResults' : 5, #ranges from 1-50
            'regionCode' : country
        }
        videos = requests.get("https://www.googleapis.com/youtube/v3/videos?key=AIzaSyCA3J2YCCTjp8ZlAkJ27zfS02kC-U1GOOk", params=parameters)
        videos = videos.json()
        items = videos['items']
        #add video information to dictionary
        for video in items:
            video_df['id'].append(video['id'])
            video_df['country'].append(country)
            video_df['title'].append(video['snippet']['title'])
            video_df['category'].append(video['snippet']['categoryId'])
            video_df['views'].append(int(video['statistics']['viewCount']))
            if 'likeCount' not in video['statistics']:
                video_df['likes'].append('na')
            else:
                video_df['likes'].append(int(video['statistics']['likeCount']))
            if 'dislikeCount' not in video['statistics']:
                video_df['dislikes'].append('na')
            else:
                video_df['dislikes'].append(int(video['statistics']['dislikeCount']))
            if 'commentCount' not in video['statistics']:
                video_df['comment_count'].append('na')
            else:
                video_df['comment_count'].append(int(video['statistics']['commentCount']))
    #create data frame
    video_df = pd.DataFrame(video_df)
    return video_df

def build_categories_df():
    categories_df = {'id' : [], 'category_name': []}
    parameters = {
        'part' : 'snippet',
        'regionCode' : 'US'
    }
    cat = requests.get('https://www.googleapis.com/youtube/v3/videoCategories?key=AIzaSyCA3J2YCCTjp8ZlAkJ27zfS02kC-U1GOOk', params=parameters)
    cat = cat.json()
    items = cat['items']
    for category in items:
        categories_df['id'].append(category['id'])
        categories_df['category_name'].append(category['snippet']['title'])
    categories_df = pd.DataFrame(categories_df)
    return categories_df


def plot_likes_dislikes_ratio(category_df):
    countries = ['GB', 'US', 'FR', 'ID', 'KE', 'NG', 'DE', 'KR', 'AU', 'JP', 'ES', 'CZ', 'PH', 'CA', 'RU', 'MX', 'IT']
    video_df = {'country' : [], 'category' : [], 'likes/dislikes' : []}
    for country in countries:
        parameters = {
            'part' : 'statistics,snippet',
            'chart' : 'mostPopular',
            'maxResults' : 5, #ranges from 1-50
            'regionCode' : country
        }
        videos = requests.get("https://www.googleapis.com/youtube/v3/videos?key=AIzaSyCA3J2YCCTjp8ZlAkJ27zfS02kC-U1GOOk", params=parameters)
        videos = videos.json()
        items = videos['items']
        #add video information to dictionary
        for video in items:
            video_df['country'].append(country)
            video_df['category'].append(video['snippet']['categoryId'])
            if 'likeCount' not in video['statistics']:
                video_df['likes/dislikes'].append(0)
            elif 'dislikeCount' not in video['statistics']:
                video_df['likes/dislikes'].append(0)
            else:
                likes = int(video['statistics']['likeCount'])
                dislikes = int(video['statistics']['dislikeCount'])
                ratio = round(likes / dislikes, 2)
                video_df['likes/dislikes'].append(ratio)
    video_df = pd.DataFrame(video_df)
    #do bar plot
    max_ratio = video_df.groupby('country')['likes/dislikes'].max()
    merged = max_ratio.to_frame().merge(video_df, on=['country', 'likes/dislikes'], how='left')
    merge_category = merged.merge(category_df, left_on='category', right_on='id', how='left')
    sns.catplot(x='country', y='likes/dislikes', hue='category_name', kind='bar', data=merge_category)
    plt.xticks(rotation=-45)
    plt.title('Category with Highest Like to Dislike Ratio in each Country')
    plt.xlabel('Country')
    plt.ylabel('Ratio of Like:Dislike') 
    plt.savefig('/Users/matthewkhoo/Desktop/CSE_163_proj/likes_dislikes_ratio.png', bbox_inches='tight') 


def world_like_dislike_raio(videos_df, categories_df):
    likes_df = videos_df.groupby('category')['likes'].sum()
    dislikes_df = videos_df.groupby('category')['dislikes'].sum()
    merged = likes_df.to_frame().merge(dislikes_df.to_frame(), on='category', how='left')
    merged['ratio'] = round(merged['likes'] / merged['dislikes'], 2)
    add_category_name = merged.merge(categories_df, left_on='category', right_on='id', how='left')
    sns.catplot(x='category_name', y='ratio', kind='bar', data=add_category_name)
    plt.xticks(rotation=-45)
    plt.title('Category by Like:Dislike Ratio')
    plt.xlabel('Category')
    plt.ylabel('Ratio of Like:Dislike') 
    plt.savefig('/Users/matthewkhoo/Desktop/CSE_163_proj/world_like_dislike_ratio.png', bbox_inches='tight') 
    

def world_views_plot(videos_df, categories_df):
    views_df = videos_df.groupby('category')['views'].sum()
    merged = views_df.to_frame().merge(categories_df, left_on='category', right_on='id', how='left')
    sns.catplot(x='category_name', y='views', kind='bar', data=merged)
    plt.xticks(rotation=-45)
    plt.title('Category by Total Views')
    plt.xlabel('Category')
    plt.ylabel('Views') 
    plt.savefig('/Users/matthewkhoo/Desktop/CSE_163_proj/world_views.png', bbox_inches='tight') 


def main():
    video_df = build_df()
    categories_df = build_categories_df()
    #plot_likes_dislikes_ratio(categories_df)
    #world_views_plot(video_df, categories_df)
    world_like_dislike_raio(video_df, categories_df)
      
if __name__ == '__main__':
    main()