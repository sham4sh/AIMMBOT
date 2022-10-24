import argparse
import json
import os
import requests
import pprint

FIREBASE_WEB_API_KEY = 'AIzaSyCXkcCfk-cFvZIr5GJ80uwaMLfvxyAQ8gY'
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"





def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)

    
    
    return r.json()


if __name__ == "__main__":
    token = sign_in_with_email_and_password('joshuashamash@gmail.com', 'password')
    pprint.pprint(token)