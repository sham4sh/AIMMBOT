from imdb import Cinemagoer
ia = Cinemagoer()

#id1 = '0000206' # TEST ID 
#### CAN USE THIS CLASS TO GET SPECIFIC DATA ON ANY PERSON ID LISTED IN THE movies_*.csv FILES #### 

class CinemagoerMovie:
    idLength = 7
    movie = None
    id = ''

    def __init__(self,id=''):
        self.id = (len(id)-self.idLength)*'0' + id
        self.movie = ia.get_movie(movieID=self.id) 
    
    def title(self):
        if 'title' in self.movie.keys(): return self.movie['title']
        else: return ''
    
    def year(self):
        if 'year' in self.movie.keys(): year = self.movie['year']
        else: return ''

    def coverURL(self):
        if 'cover url' in self.movie.keys(): coverURL = self.movie['cover url']
        else: return ''
    
    def plot(self):
        if 'plot outline' in self.movie.keys(): plot = self.movie['plot outline']
        else: return ''

    
class CinemagoerPerson:
    idLength = 7
    individual = None
    id = ''

    def __init__(self,id=''):
        self.id = (len(id)-self.idLength)*'0' + id
        self.individual = ia.get_person(self.id) 
    
    def name(self):
        if 'name' in self.individual.keys(): return self.individual['name']
        else:return ''

    def birthdate(self):
        if 'birth date' in self.individual.keys(): return self.individual['birth date']
        else:return ''

    def headshot(self):
        if 'headshot' in self.individual.keys(): return self.individual['headshot']
        else:return ''

    def miniBio(self):
        if 'mini biography' in self.individual.keys(): 
            print(self.individual['mini biography'])
            return self.individual['mini biography']
        else:return ''
    
    def filmography(self): # return list of movie ids of movies the person was involved with 
        filmsID = []
        if 'filmography' in self.individual.keys(): 
            films = self.individual['filmography']['actor']
            #print(films)
            for f in films:
                filmsID.append(ia.get_movie(f.movieID))
        return filmsID


'''
x= ia.get_person(id1)
for y in x.keys():
    print(y, ' ', type(x[y]))

get_person_awards
get_person() attributes below 
['birth info', 'headshot', 'akas', 'filmography', 'imdbID', 'name', 
'nick names', 'birth name', 'height', 'mini biography', 'trade mark',
 'trivia', 'quotes', 'salary history', 'birth date', 'birth notes', 
 'canonical name', 'long imdb name', 'long imdb canonical name', 
 'full-size headshot']

'''
