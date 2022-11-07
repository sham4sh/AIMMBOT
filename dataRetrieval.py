import os
import pandas as pd
from imdb import Cinemagoer

#### USE getAllData() FUNCTION TO ADD DATA TO THE CSVs FROM CINEMAGOER ####
class DataRetieval:
    # GLOBAL VARIABLES  
    producersLocation = './data/movies_producers.csv'
    linksLocation = './data/links.csv'
    moviesDetailsLocation = './data/movies_detailed.csv'
    genresLocation = './data/movies_genres.csv'
    castLocation = './data/movies_cast.csv'
    writersLocation = './data/movies_writers.csv'
    countriesLocation = './data/movies_countries.csv'
    directorLocation = './data/movies_directors.csv'
    ratings = {'adult':['NC-17','R','TV-MA'],'teen':['PG-13','TV-PG','TV-14'],'preteen':['PG','TV-Y7'],'general':['TV-Y','G','TV-G']}

    def readFile(self,filename): 
        if os.path.exists(filename) and os.path.getsize(filename)>0:
            return pd.read_csv(filename)
        return pd.DataFrame()

    def getLinksFromCSV(self,filename): # returns a list of imdb ids to add to tables 
        imdbIdList = []
        df = self.readFile(filename)
        if not 'imdbId' in df.columns: return imdbIdList
        for x in df.index:
            currImdbId = str(df.loc[x, "imdbId"])
            currImdbId = '0'*(7-len(currImdbId)) + currImdbId
            imdbIdList.append(currImdbId)
        return imdbIdList

    # creates a csv with ['movieId','imdbId','producerId']
    def addProducers(self,movieID, movie,filename = producersLocation):
        cols = ['movieId','imdbId','producerId']
        df = self.readFile(filename)
        if df.empty: 
            df = pd.DataFrame(columns=cols)
            #df.to_csv(filename)
        if 'producer' in movie.keys() and not int(movieID) in set(df['movieId']):
            for p in movie['producer']:
                df = df.append({"movieId":movieID, "imdbId":str(movie.movieID), "producerId":str(p.personID)},ignore_index=True)
            df = df[cols]
            df.to_csv(filename)
                # with open(filename, 'a') as f_object:
                #    dictwriter_object = DictWriter(f_object, fieldnames=cols)
                #    dictwriter_object.writerow({"movieId":movieID, "imdbId":str(movie.movieID), "producerId":str(p.personID)})
                #    f_object.close()

    # adds all cast and their ids to a csv 
    def addCast(self,movieID, movie,filename = castLocation):
        cols = ['movieId','imdbId','castId']
        df = self.readFile(filename)
        if df.empty: 
            df = pd.DataFrame(columns=cols)
        if 'cast' in movie.keys() and not int(movieID) in set(df['movieId']): 
            for c in movie['cast']:
                df = df.append({"movieId":movieID, "imdbId":str(movie.movieID), "castId":str(c.personID)},ignore_index=True)
        df = df[cols]
        df.to_csv(filename)

    # adds all writers and their ids to a csv 
    def addWriter(self,movieID, movie,filename = writersLocation):
        cols = ['movieId','imdbId','writerId']
        df = self.readFile(filename)
        if df.empty: 
            df = pd.DataFrame(columns=cols)
        if 'writer' in movie.keys() and not int(movieID) in set(df['movieId']): 
            for w in movie['writer']:
                df = df.append({"movieId":movieID, "imdbId":str(movie.movieID), "writerId":str(w.personID)},ignore_index=True)
        df = df[cols]
        df.to_csv(filename)

    # adds all writers and their ids to a csv 
    def addDirectors(self,movieID, movie,filename = directorLocation):
        cols = ['movieId','imdbId','directorId']
        df = self.readFile(filename)
        if df.empty: 
            df = pd.DataFrame(columns=cols)
        if 'director' in movie.keys() and not int(movieID) in set(df['movieId']): 
            for d in movie['director']:
                df = df.append({"movieId":movieID, "imdbId":str(movie.movieID), "directorId":str(d.personID)},ignore_index=True)
        df = df[cols]
        df.to_csv(filename)

    # adds all genres to a csv
    def addMovieDetails(self,movieID,movie,filename = moviesDetailsLocation):
        cols = ['movieId','imdbId','title','year','parentalRating','runtime','coverURL','plot']
        title, year, plot,coverURL= '','','',''
        df = self.readFile(filename)
        if df.empty: 
            df = pd.DataFrame(columns=cols)
        
        # adding all relavent data to a dict 
        if 'title' in movie.keys(): title = movie['title']
        if 'year' in movie.keys(): year = movie['year']
        if 'cover url' in movie.keys(): coverURL = movie['cover url']
        if 'plot outline' in movie.keys(): plot = movie['plot outline']
        if not int(movieID) in set(df['movieId']): 
            df = df.append({"movieId":movieID,"imdbId":str(movie.movieID), 'title':title, 'year':year,'parentalRating':self.getCert(movie),'runtime':self.getRuntime(movie),'coverURL':coverURL,"plot":plot},ignore_index=True)
            df = df[cols]
            df.to_csv(filename)

    # returns most conservative rating of a movie 
    def getCert(self,movie):
        rating = ''
        currRatings = {'general':0,'preteen':0,'teen':0,'adult':0}
        if 'certificates' in movie.keys(): 
            certificates = movie['certificates']
            for cert in movie['certificates']:
                if "united states" in cert.lower():
                    cert.split('::')[0]
                if ':' in cert: cert = cert.split(':')
                if len(cert)>1: cert = cert[1]
                else: cert = ''
                for r in self.ratings.keys():
                    if cert in self.ratings[r]: currRatings[r]+=1
        for c in currRatings.keys():
            if currRatings[c]>0: rating = c 
        return rating 

    # gets US runtime for movie (in minutes) 
    def getRuntime(self,movie):
        runtimes = ''
        if 'runtimes' in movie.keys():
            runList = movie['runtime'] 
            if len(runList)==1:
                if str(runList[0]).isdigit(): runtimes = int(runList[0])
            for r in runList:
                if "us:" in r: 
                    runtimes = r.split(':')[1]
        return runtimes

    # add Genres to a csv 
    def addGenres(self,movieID,movie,filename = genresLocation):
        cols = ['movieId','imdbId','genre']
        df = self.readFile(filename)
        if df.empty: 
            df = pd.DataFrame(columns=cols)
        if 'genres' in movie.keys() and not int(movieID) in set(df['movieId']): 
            for g in movie['genres']:
                #print(g)
                df = df.append({"movieId":movieID, "imdbId":str(movie.movieID), "genre":g},ignore_index=True)
        df = df[cols]
        df.to_csv(filename)

    # adds country of origin to a csv 
    def addCountries(self,movieID, movie,filename = countriesLocation):
        cols = ['movieId','imdbId','countries']
        df = self.readFile(filename)
        if df.empty: 
            df = pd.DataFrame(columns=cols)
        if 'countries' in movie.keys() and not int(movieID) in set(df['movieId']): 
            for c in movie['countries']:
                #print(c)
                df = df.append({"movieId":movieID, "imdbId":str(movie.movieID), "countries":c},ignore_index=True)
        df = df[cols]
        df.to_csv(filename)

    def getAllData(self):
        ia = Cinemagoer()
        df = self.readFile(self.linksLocation)
        #################df = df.sample(frac=0.0205,random_state=1)
        #print(len(df))
        if  'imdbId' in df.columns or 'movieId' in df.columns: 
            for x in df.index:
                movieID = int(df.loc[x, "movieId"])
                currImdbId = str(df.loc[x, "imdbId"])
                currImdbId = '0' * (7-len(currImdbId)) + currImdbId
                #movieID = 2 # TEST 
                #currImdbId = '0114709' #TEST 
                movie = ia.get_movie(currImdbId)
                self.addProducers(movieID,movie,self.producersLocation)
                self.addCast(movieID,movie,self.castLocation)
                self.addWriter(movieID,movie,self.writersLocation)
                self.addGenres(movieID,movie,self.genresLocation)
                self.addCountries(movieID,movie,self.countriesLocation)
                self.addMovieDetails(movieID,movie,self.moviesDetailsLocation)
                self.addDirectors(movieID,movie,self.directorLocation)

    def readFileTest(self):
        testLocation = 'data.txt'
        results = self.readFile(testLocation)
        if len(results) == 0: print("Test 1 Passed ")
        testMovie = '0114709'
        # ADD TESTS HERE 

    '''
    add step to make sure imdb movie ID is valid 
    '''
