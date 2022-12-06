import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

def clean_genres(genres):
    genres = re.sub("[^a-zA-Z0-9 ]", " ", genres)
    return genres

def search_by_year(title):
    movies["clean_title"] = movies["title"].apply(clean_title)
    vectorizer = TfidfVectorizer(ngram_range=(1,5))
    tfidf = vectorizer.fit_transform(movies["clean_title"])
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -10)[-10:]
    results_year = movies.iloc[indices].iloc[::-1]
    return results_year

def search_by_genre(genre):
    movies["clean_genres"] = movies["genres"].apply(clean_genres)
    vectorizer = TfidfVectorizer(ngram_range=(1,5))
    tfidf = vectorizer.fit_transform(movies["clean_genres"])
    genre = clean_genres(genre)
    query_vec = vectorizer.transform([genre])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -10)[-10:]
    results_genre = movies.iloc[indices][::-1]
    return results_genre

movies = pd.read_csv("SecondaryAlgoGenreBasedDatabase.csv")
genre = input("Enter your favorite genre(s) ")
print(search_by_genre(genre))
title = input("Enter your favorite year ")
print(search_by_year(title))