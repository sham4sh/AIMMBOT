import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


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
        print(userId)
        favsDict = {}
        doc_ref = self.users_ref.document(userId)
        doc = doc_ref.get()
        if doc.exists:
            print(f'Document data: {doc.to_dict()}')
            favsDict = doc.to_dict()
        else:
            print(u'No such document!')
        return favsDict
    
    def addFav(self,userId, movieId, rating):
        doc_ref = self.users_ref.document(userId)
        doc_ref.set({movieId:rating}, merge=True)
        return True
        
    def removeFav(self,userId, movieId):
        doc_ref = self.users_ref.document(userId)
        doc_ref.update({movieId:firestore.DELETE_FIELD}) # if field does not exist nothing happens 
        return True

    
def test():
    cred = credentials.Certificate('aimmbot-ea206-firebase-adminsdk-wb137-2f8132fd73.json') # this should be a service account 
    app = firebase_admin.initialize_app(cred)
    FDA = FirestoreDataAccess(app=app)
    UID = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjNmNjcyNDYxOTk4YjJiMzMyYWQ4MTY0ZTFiM2JlN2VkYTY4NDZiMzciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vYWltbWJvdC1lYTIwNiIsImF1ZCI6ImFpbW1ib3QtZWEyMDYiLCJhdXRoX3RpbWUiOjE2NjY1Njg0MjcsInVzZXJfaWQiOiJKUHVGNTlDV3BiU0lHUnl1UnhMVmNDM01NTVQyIiwic3ViIjoiSlB1RjU5Q1dwYlNJR1J5dVJ4TFZjQzNNTU1UMiIsImlhdCI6MTY2NjU2ODQyNywiZXhwIjoxNjY2NTcyMDI3LCJlbWFpbCI6Impvc2h1YXNoYW1hc2hAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImpvc2h1YXNoYW1hc2hAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.DUx-1V5c-SKgoq8_OQkY--nvEuRVRsjlwlQaP2rB42ccvvgB0n1SqTAY6iRTZV4pC4LpgWbmMyZjt7blwpKzj1pl5Mb_R0c9UpseelQ-WcQvjoceo6pCbWj9EGqZ5j78RpUOmxtA3U-L8JQ1rBlEcwaoar7YZZD8s0CGXsPW4E0X4FZFq0fC_qh0fEaCQCUuQueEe868BFdqGFfIYwqy6OabOO4be7cm13sqzHTmoZsz4HjfvbG57qGNjUvuZdmrzIcD9g2B-ki5QR4dXeIdVB3Zx9TTWE363EVkVWr27X80zO1qo5UW67AGtgwSt8QEhQ0FVzNIXDzhtGVNDlx3aQ'
    values = FDA.getFavs(UID)
    if len(values.keys())>0: print(f'getFavsTest - Test 1 passed. output size is {len(values.keys())} and is not empty or null ')
    else: print(f'getFavsTest - Test 1 FAILED . output size is {len(values.keys())}. No dictionary was returned')
    values = FDA.removeFav(UID,'87469')
    values = FDA.addFav(UID,'87469',4)

#test()
