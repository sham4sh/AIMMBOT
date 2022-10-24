import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

df = pd.read_csv('data/ratings.csv')
df = df.drop(['timestamp'],axis=1)
#print(df.head())
def ratingsDistributionBarGraph():
    data = df['rating'].value_counts().sort_index(ascending=False)
    plt.bar(data.index,data.values)
    plt.title("Distribution of {} Movie Ratings".format(df.shape[0]))
    plt.xlabel('Ratings')
    plt.ylabel('Count')
    plt.show()

def ratingDistByMovie():
    data = df.groupby('movieId')['rating'].count().clip(upper=200)
    plt.hist(x=data.values, bins=10)
    plt.title("Distribution of # of Movie Ratings - Clipped at 200".format(df.shape[0]))
    plt.xlabel('Number of Ratings per Movie')
    plt.ylabel('Count')
    plt.show()

def ratingDistByUser():
    data = df.groupby('userId')['rating'].count().clip(upper=1000)
    print(data.head())
    plt.hist(x=data.values, bins=10)
    plt.title("Distribution of # of User Ratings - Clipped at 1000")
    plt.xlabel('Number of Ratings per User')
    plt.ylabel('Count')
    plt.show()

#ratingDistByMovie()
