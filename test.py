import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from UserCSVData import UserCSVDataAccess
from algorithms.primaryAlgorithm import PrimaryAlgorithm
from UserDataFirebase import FirestoreDataAccess
'''
x = UserCSVDataAccess()
x.addFav('a','1231587',5)
x.addFav('a','1007028',4)
x.addFav('a','357413',3)
x.addFav('b','316654',5)
x.addFav('b','78346',3)
x.addFav('b','86893',4)
x.addFav('b','81573',4)
x.addFav('b','100758',4)

testing = PrimaryAlgorithm()
print(testing.get_top_n('a',10))
print(testing.get_top_n('b',10))
'''

UID = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjNmNjcyNDYxOTk4YjJiMzMyYWQ4MTY0ZTFiM2JlN2VkYTY4NDZiMzciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vYWltbWJvdC1lYTIwNiIsImF1ZCI6ImFpbW1ib3QtZWEyMDYiLCJhdXRoX3RpbWUiOjE2NjY1Njg0MjcsInVzZXJfaWQiOiJKUHVGNTlDV3BiU0lHUnl1UnhMVmNDM01NTVQyIiwic3ViIjoiSlB1RjU5Q1dwYlNJR1J5dVJ4TFZjQzNNTU1UMiIsImlhdCI6MTY2NjU2ODQyNywiZXhwIjoxNjY2NTcyMDI3LCJlbWFpbCI6Impvc2h1YXNoYW1hc2hAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImpvc2h1YXNoYW1hc2hAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.DUx-1V5c-SKgoq8_OQkY--nvEuRVRsjlwlQaP2rB42ccvvgB0n1SqTAY6iRTZV4pC4LpgWbmMyZjt7blwpKzj1pl5Mb_R0c9UpseelQ-WcQvjoceo6pCbWj9EGqZ5j78RpUOmxtA3U-L8JQ1rBlEcwaoar7YZZD8s0CGXsPW4E0X4FZFq0fC_qh0fEaCQCUuQueEe868BFdqGFfIYwqy6OabOO4be7cm13sqzHTmoZsz4HjfvbG57qGNjUvuZdmrzIcD9g2B-ki5QR4dXeIdVB3Zx9TTWE363EVkVWr27X80zO1qo5UW67AGtgwSt8QEhQ0FVzNIXDzhtGVNDlx3aQ'
cred = credentials.Certificate('aimmbot-ea206-firebase-adminsdk-wb137-2f8132fd73.json') # this should be a service account 
app = firebase_admin.initialize_app(cred)
FDA = FirestoreDataAccess(app=app)

favsDict = FDA.getFavs(UID)

ids = favsDict.keys()
ratings = favsDict.values()

df = pd.DataFrame()
df['userId'] = [UID]*len(ids)
df['movieId'] = len(ids)
df['imdbId'] = ids
df['rating'] = ratings
df2 = pd.read_csv('data/ratings.csv')
temp = pd.concat([df,df2])

print(temp[temp['userId']==UID])

#df = pd.DataFrame([uids, ids, ratings])#, columns=['userId', 'imdbId', 'ratings'])

#print(df.head())
