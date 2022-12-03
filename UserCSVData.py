import pandas as pd 
from csv import DictWriter
class UserCSVDataAccess:
    ratingsLocation = 'data/ratings.csv'
    def __init__(self):
        pass
    
    def addFav(self, uid, mid, rating):
        assert type(uid) == type(mid) == type("") 
        assert mid.isdigit() == True 
        try:
            field_names = ['userId','movieId','imdbId','rating']
            with open(self.ratingsLocation, 'a') as file:
                writer = DictWriter(file, fieldnames=field_names)
                writer.writerow({'userId':uid, 'movieId':-1, 'imdbId':mid, 'rating':rating})
                file.close()
        except FileNotFoundError as e:
            print("CSVDataAccess - File Not Found - do not return a widget with user based recommendations.")    
        return True
    
    def removeFav(self, uid, mid):
        assert type(uid) == type(mid) == type("") 
        assert mid.isdigit() == True
        ratings = pd.read_csv(self.ratingsLocation,dtype = {'userId':str,'movieId':int,'imdbId':int,'rating':float})
        df_filtered = ratings[ratings['userId'].values==uid].index
        df_filtered = ratings.iloc[df_filtered]
        print(df_filtered)
        #ind = df_filtered.loc[:,]
        ind = df_filtered[df_filtered[['imdbId']].values==int(mid)].index.tolist()
        print(ind)
        if len(ind)>0:ratings.drop(index=ind, inplace=True)
        ratings = ratings[['userId','movieId','imdbId','rating']]
        ratings.to_csv(self.ratingsLocation,index=False)
        return True 

def test():
    print(UserCSVDataAccess().addFav('ab', '3', 1))
    print(UserCSVDataAccess().removeFav('ab', '3'))