import numpy as np
import pandas as pd
import difflib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

genre_data = pd.read_csv('movies.csv')
selected_features = ['genres']

for feature in selected_features:
    genre_data[feature] = genre_data[feature].fillna('')
  
combined_features = genre_data['genres']
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)
searched_genre = input(' Enter your favorite genre : ')

list_of_all_genres = genre_data['genres'].tolist()
find_close_match = difflib.get_close_matches(searched_genre, list_of_all_genres)
close_match = find_close_match[0]
index_of_the_genre = genre_data[genre_data.genres == close_match]['movieId'].values[0]
similarity_score = list(enumerate(similarity[index_of_the_genre]))
sorted_similar_genres = sorted(similarity_score, key = lambda x:x[1], reverse = True) 

print('Movies suggested for you : \n')

i = 0

for genre in sorted_similar_genres:
  index = genre[0]
  genres_from_movieId = genre_data[genre_data.index==index]['genres'].values[0]
  title_from_index = genre_data[genre_data.index==index]['title'].values[0]
  if (i<21):
    print(i, title_from_index, genres_from_movieId)
    i+=1