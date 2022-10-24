from surprise import Prediction, Reader, Dataset,accuracy #,similarities
import pandas as pd
import surprise
from surprise.model_selection import cross_validate, train_test_split
from collections import defaultdict


df = pd.read_csv('data/ratings.csv')
df.drop('timestamp',axis=1, inplace=True)
#print(df.head())

reader = Reader(rating_scale=(0.5,5.0)) # used to parse file containing ratings - REQUIRED 

data = Dataset.load_from_df(df[['userId','movieId','rating']],reader)

def displayResults(algo):
    for i in algo.keys(): print(i, ":", algo[i])

####algorithms = [surprise.SVD, surprise.SlopeOne, surprise.NMF, surprise.NormalPredictor, surprise.KNNBaseline, surprise.KNNBasic, surprise.KNNWithMeans, surprise.KNNWithZScore, surprise.BaselineOnly, surprise.CoClustering]
algorithms = [surprise.SVD,surprise.KNNBaseline, surprise.BaselineOnly]
# SVD 
#svd = cross_validate(surprise.SVD(),data, measures=['RMSE','MAE'],cv=5,verbose=True)
#displayResults(svd)
'''
for a in algorithms:
    algo = cross_validate(a(),data, measures=['RMSE','MAE'],cv=3,verbose=True)
    displayResults(algo)
'''
# SVD 
#svd = cross_validate(.,data, measures=['RMSE','MAE'],cv=5,verbose=True)
#displayResults("SVD algorithm Error ", svd)

#trainset, testset = train_test_split(data, test_size=0.25)
#algo = surprise.SVD()
#algo.fit(trainset)
#predictions = algo.test(testset)

# Then compute RMSE
#print(accuracy.rmse(predictions))
accuracy.rmse(predictions)
accuracy.

def get_top_n(predictions, n=10):
    #Return the top-N recommendation for each user from a set of predictions.

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n

'''
top_n = get_top_n(predictions, n=10)

# Print the recommended items for each user
for uid, user_ratings in top_n.items():
    print(uid, [mid for (mid, _) in user_ratings]) # mid is movie id 
'''