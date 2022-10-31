#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')


# In[3]:


movies.head(2)


# In[4]:


movies.shape


# In[5]:


credits.head()


# In[6]:


movies = movies.merge(credits,on='title')


# In[7]:


movies.head()
# budget
# homepage
# id
# original_language
# original_title
# popularity
# production_comapny
# production_countries
# release-date(not sure)


# In[8]:


movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[9]:


movies.head()


# In[10]:


import ast


# In[11]:


def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L 


# In[12]:


movies.dropna(inplace=True)


# In[13]:


movies['genres'] = movies['genres'].apply(convert)
movies.head()


# In[14]:


movies['keywords'] = movies['keywords'].apply(convert)
movies.head()


# In[15]:


import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')


# In[16]:


def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L 


# In[17]:


movies['cast'] = movies['cast'].apply(convert)
movies.head()


# In[18]:


movies['cast'] = movies['cast'].apply(lambda x:x[0:3])


# In[19]:


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 


# In[20]:


movies['crew'] = movies['crew'].apply(fetch_director)


# In[21]:


#movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies.sample(5)


# In[22]:


def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1


# In[23]:


movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)


# In[24]:


movies.head()


# In[25]:


movies['overview'] = movies['overview'].apply(lambda x:x.split())


# In[26]:


movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


# In[27]:


new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
#new.head()


# In[28]:


new['tags'] = new['tags'].apply(lambda x: " ".join(x))
new.head()


# In[29]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
    


# In[30]:


vector = cv.fit_transform(new['tags']).toarray()


# In[31]:


vector.shape


# In[32]:


from sklearn.metrics.pairwise import cosine_similarity


# In[33]:


similarity = cosine_similarity(vector)


# In[34]:


similarity


# In[35]:


new[new['title'] == 'The Lego Movie'].index[0]


# In[36]:


def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new.iloc[i[0]].title)


# In[37]:


recommend('Gandhi')


# In[41]:


import pickle


# In[42]:


pickle.dump(new,open('movie_dict.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))

