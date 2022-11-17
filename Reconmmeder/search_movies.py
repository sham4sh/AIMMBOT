import numpy as np
import pandas as pd

csv_file = 'movies.csv'
df = pd.read_csv(csv_file)
csv_files = ['movies.csv']

columns = ['genres']
#print (df[columns].head(5))

def get_genres(data):
    genres = []
    for i in range(0, data.shape[0]):
        genres.append(data['genres'][i])
    return genres

df['genres'] = get_genres(df)
#print(df.head(10))

for genre in csv_files:
    searched_genre = input('Search a movie based on genre: ')
    df = pd.read_csv(genre)
    Adventure = df['title'].where(df['genres'] == 'Adventure').dropna()
    Animation = df['title'].where(df['genres'] == 'Animation').dropna()
    Children = df['title'].where(df['genres'] == 'Children').dropna()
    Comedy = df['title'].where(df['genres'] == 'Comedy').dropna()
    Fantasy = df['title'].where(df['genres'] == 'Fantasy').dropna()
    Romance = df['title'].where(df['genres'] == 'Romance').dropna()
    Action = df['title'].where(df['genres'] == 'Action').dropna() 
    Crime = df['title'].where(df['genres'] == 'Crime').dropna()
    Thriller = df['title'].where(df['genres'] == 'Thriller').dropna()
    Drama = df['title'].where(df['genres'] == 'Drama').dropna()
    Horror = df['title'].where(df['genres'] == 'Horror').dropna()
    Mystery = df['title'].where(df['genres'] == 'Mystery').dropna()
    Sci_Fi = df['title'].where(df['genres'] == 'Sci_Fi').dropna()
    War = df['title'].where(df['genres'] == 'War').dropna()
    Musical = df['title'].where(df['genres'] == 'Musical').dropna()
    Documentary = df['title'].where(df['genres'] == 'Documentary').dropna()
    Western = df['title'].where(df['genres'] == 'Western').dropna()
    Film_Noir = df['title'].where(df['genres'] == 'Film_Noir').dropna()
    
    if searched_genre == 'Adventure':
        print(Adventure)
    if searched_genre == 'Animation':
        print(Animation)
    if searched_genre == 'Children':
        print(Children)
    if searched_genre == 'Comedy':
        print(Comedy)
    if searched_genre == 'Fantasy':
        print(Fantasy)
    if searched_genre == 'Romance':
        print(Romance)
    if searched_genre == 'Action':
        print(Action)
    if searched_genre == 'Crime':
        print(Crime)
    if searched_genre == 'Thriller':
        print(Thriller)
    if searched_genre == 'Drama':
        print(Drama)
    if searched_genre == 'Horror':
        print(Horror)
    if searched_genre == 'Mystery':
        print(Mystery)
    if searched_genre == 'Sci_Fi':
        print(Sci_Fi)
    if searched_genre == 'War':
        print(War)
    if searched_genre == 'Musical':
        print(Musical)
    if searched_genre == 'Documentary':
        print(Documentary)
    if searched_genre == 'Western':
        print(Western)
    if searched_genre == 'Film_Noir':
        print(Film_Noir)

