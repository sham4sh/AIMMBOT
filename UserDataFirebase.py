import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import UserCSVData 


class FirestoreDataAccess:
    db = None 
    users_ref = None
    movies_ref = None  
    app = None 
    def __init__(self, app): # need to confirm that instance of app is passed 
        assert app is not None 
        self.db = firestore.client(app=app)
        self.users_ref = self.db.collection(u'users')
      
    def getFavs(self, userId):
        assert type(userId) == type("")
        favsDict = {}
        doc_ref = self.users_ref.document(userId)
        doc = doc_ref.get()
        if doc.exists:
            #print(f'Document data: {doc.to_dict()}')
            favsDict = doc.to_dict()
        else:
            print(u'No such document!')
        return favsDict
    
    def addFav(self,userId, movieId, rating):
        assert type(userId) == type(movieId) == type("") 
        assert movieId.isdigit() == True
        validAndProcessed = False
        if type(rating) == type(0.0)or type(rating) == type(1): # checks if valid input 
            if rating>=0.0 and rating<=5.0:
                doc_ref = self.users_ref.document(userId)
                doc = doc_ref.set({movieId:rating}, merge=True)
                #UserCSVData().addFav(userId, movieId, rating)
                validAndProcessed = True
        return validAndProcessed # returns boolean that tells if the rating is valid and processed 
        
    def removeFav(self,userId, movieId):
        assert type(userId) == type(movieId) == type("") 
        assert movieId.isdigit() == True
        doc_ref = self.users_ref.document(userId)
        doc = doc_ref.update({movieId:firestore.DELETE_FIELD}) # if field does not exist nothing happens 
        #UserCSVData().removeFav(userId, movieId)
        return True

    
def test():
    cred = credentials.Certificate('aimmbot-ea206-firebase-adminsdk-wb137-2f8132fd73.json') # this should be a service account 
    app = firebase_admin.initialize_app(cred)
    FDA = FirestoreDataAccess(app=app)
    UID = 'testUser'
    values = FDA.getFavs(UID)
    if len(values.keys())>0: print(f'getFavsTest - Test 1 passed. output size is {len(values.keys())} and is not empty or null ')
    else: print(f'getFavsTest - Test 1 FAILED . output size is {len(values.keys())}. No dictionary was returned')
    #values = FDA.removeFav(UID,'1007028')
    values = FDA.addFav(UID,'1007028',4)

#test()
