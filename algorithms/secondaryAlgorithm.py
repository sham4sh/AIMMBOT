from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd
# this is a KNN algorithm that uses cosine smilarity to calculate the closest neighbors/movies

class SecondaryAlgorithm:
    moviesLocation  = 'data/movies_detailed.csv'
    ratingsLocation = 'data/ratings.csv'
    csr_data = None 
    data_final = None 
    ratings = None
    #movies = None

    def __init__(self):
        self.processData()

    def getDataHelper(self): # HELPER FUNCTION 
        try:
            movies = pd.read_csv(self.moviesLocation)
            ratings = pd.read_csv(self.ratingsLocation)
            if np.in1d(np.array(['userId','imdbId','rating']), ratings.columns).all():
                ratings = ratings[['userId','imdbId','rating']]
        except FileNotFoundError as e:
            print("Sec Algorithm - File Not Found - do not return a widget with user based recommendations.")
        except Exception as e:
            print(type(e).__name__, e.args)
        self.ratings = ratings 
        #self.movies = movies 

    def processData(self):
        self.getDataHelper()
        data = pd.pivot(index = 'imdbId',columns = 'userId', data = self.ratings,values ='rating')
        numberOf_user_voted_for_movie = pd.DataFrame(self.ratings.groupby('imdbId')['rating'].agg('count'))
        numberOf_user_voted_for_movie.reset_index(level = 0,inplace = True)
        data.shape
        numberOf_movies_voted_by_user = pd.DataFrame(self.ratings.groupby('userId')['rating'].agg('count'))     
        numberOf_movies_voted_by_user.reset_index(level = 0,inplace = True)
        data.fillna(0,inplace = True)
        data_final = data.loc[numberOf_user_voted_for_movie[numberOf_user_voted_for_movie['rating'] > 10]['imdbId'],:]
        data_final = data_final.loc[:,numberOf_movies_voted_by_user[numberOf_movies_voted_by_user['rating'] > 60]['userId']]
        self.csr_data = csr_matrix(data_final.values)
        self.data_final = data_final.reset_index(inplace=True)
        self.data_final = data_final

    def getPredictionsHelper(self,mid, n):
        knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20)
        knn.fit(self.csr_data)
        movie_counter = n
        movie_idx= self.ratings.index[self.ratings['imdbId']==int(mid)].tolist()[0]
        distances , indices = knn.kneighbors(self.csr_data[movie_idx],n_neighbors = movie_counter + 1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze(),distances.squeeze())), key = lambda x: x[1])[1::1]
        imdbIds = []
        #print(rec_movie_indices)
        for val in rec_movie_indices:
            movie_idx = self.data_final.iloc[val[0]]['imdbId']
            idx = self.ratings[self.ratings['imdbId'] == movie_idx].index
            imdbIds.append(int(movie_idx))
            #print(movie_idx, self.movies.iloc[idx]['title'].values[0])
        return imdbIds
    
    def get_top_n(self, mid, n=10):
        
        predictions = self.getPredictionsHelper(mid, n)
        return predictions[:10]


#movie = input("Enter a movie: ")
#print(get_movie_recommendation(movie))

def test():
    x = SecondaryAlgorithm()
    print(x.get_top_n(13442))
    print(x.get_top_n('20629'))
    print(x.get_top_n('21814'))