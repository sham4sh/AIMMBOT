
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
cred = credentials.Certificate("AIMMBOT/aimmbot-ea206-firebase-adminsdk-wb137-2f8132fd73.json")
firebase_admin.initialize_app(cred)

# https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth#firebase_admin.auth.UserRecord 

# THE USER BELOW EXISTS IN THE DB 
email1 = 'test@gmail.com'#input("Enter Email: ")
password1 = '123456' #input("Enter Password: ")

def createUserCred(email, password): # can create with UID 
    try:
        user = auth.create_user(email=email, password=password)
        print("User {0} Created Sucessfully".format(str(user.uid())))
    except auth.EmailAlreadyExistsError:
        print('Email Already Exists!')
    except:
        print("Account already Exists ")

def getUser(email):
    user = auth.get_user_by_email(email)
    print("user id is{0}".format(user.uid))

def getListOfUsers():
    page = auth.list_users()
    userList = []
    while page:
        for us in page.users:
            userList.append(us.uid)
        page = page.get_next_page()
    return userList

def checkUserCred(email,password):
    #try:
        login = auth.get.sign_in_with_email_and_password(email=email,password=password) # does not work for some reason 
        #print(login)
        #print("User {0} Created Sucessfully".format(str(login.user.uid())))
    #except:
    #    print('Invalid email or password')

createUserCred(email1,password1)

#checkUserCred(email1,password1)


