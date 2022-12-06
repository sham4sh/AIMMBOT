import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

def search_by_year(title):
    movies["clean_title"] = movies["title"].apply(clean_title)
    vectorizer = TfidfVectorizer(ngram_range=(1,5))
    tfidf = vectorizer.fit_transform(movies["clean_title"])
    
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -10)[-20:]
    results = movies.iloc[indices].iloc[::-1]
    return results

title = input("Enter your favorite year ")
movies = pd.read_csv("SecondaryAlgoGenreBasedDatabase.csv")
print(search_by_year(title))