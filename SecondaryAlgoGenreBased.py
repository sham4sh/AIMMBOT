import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("SecondaryAlgoGenreBasedDatabase.csv")

def clean_genres(genres):
    genres = re.sub("[^a-zA-Z0-9 ]", " ", genres)
    return genres

genre = input("Enter your favorite genre(s) ")

def search(genre):
    movies["clean_genres"] = movies["genres"].apply(clean_genres)
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(movies["clean_genres"])
    
    genre = clean_genres(genre)
    query_vec = vectorizer.transform([genre])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -10)[-10:]
    results = movies.iloc[indices][::-1]
    return results

print(search(genre))
    