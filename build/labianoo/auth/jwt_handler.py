from os import error
import time
from typing import Dict
import jwt
from decouple import config
from fastapi.encoders import jsonable_encoder

def token_response(token: str , user):
    return {
        
        "access_token": token ,"user": user ,  "status":True  , "expires":time.time() + 24000000000
    }

JWT_SECRET = config('secret')

def signJWT(user_id: str , user , permissions) -> Dict[str, str]:
    # Set the expiry time
    data = jsonable_encoder(user)
    
    data.pop('hashed_password', None)
    payload = {
        'user_id': data,
        'expires': time.time() + 24000000000
    }
    return token_response(jwt.encode(payload, JWT_SECRET, algorithm="HS256") , data)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
        # print(decoded_token)
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}
