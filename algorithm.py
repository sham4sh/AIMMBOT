from surprise import Reader, Dataset 
import pandas as pd
import surprise
#from surprise.model_selection import cross_validate, train_test_split
from collections import defaultdict
import numpy as np


# NOTES:
    # Add all new users to the filelocation. 
    # Then instantiate this class or run processData function 
    # then use get_top_n() to get the predictions 
class PrimaryAlgorithm:
    uid = None 
    data = None
    filelocation = 'data/ratings.csv'

    def __init__(self) -> None:
        df = self.processData()

    def getDataHelper(self): # HELPER FUNCTION 
        try:
            df = pd.read_csv(self.filelocation)
            if np.in1d(np.array(['userId','movieId','rating']), df.columns).all():
                df = df[['userId','movieId','rating']]
        except FileNotFoundError as e:
            print("Prim Algorithm - File Not Found - do not return a widget with user based recommendations.")
        except Exception as e:
            print(type(e).__name__, e.args)
        return df 

    def processData(self):
        df = self.getDataHelper()
        reader = Reader(rating_scale=(0.5,5.0)) # used to parse file containing ratings - REQUIRED 
        data = Dataset.load_from_df(df[['userId','movieId','rating']],reader).build_full_trainset()
        self.data = data
        return self.data
    
    def getPredictionsHelper(self):
        algo = surprise.SVD()
        algo.fit(self.data)
        userData = self.data.build_testset()
        algo = surprise.SVD()
        algo.fit(self.data)
        predictions = algo.test(userData)
        return predictions

    def get_top_n(self, uid, n=10):
        uid = str(uid)
        predictions = self.getPredictionsHelper()
        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))

        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]
        
        if uid in top_n.keys():
            return([mid for (mid, _) in top_n[uid]])
        else: return list()

    def test(self):
        prim = PrimaryAlgorithm()
        df = prim.processData()
        top_n = prim.get_top_n('1', 10)
        print(prim.get_top_n('1',15))
#END CLASS 


def getImdbId(mid):
    mid = int(mid)
    df = pd.read_csv('data/links.csv')
    assert 'movieId' in df.columns and 'imdbId' in df.columns
    return df.loc[mid,'imdbId']

print(getImdbId('1'))