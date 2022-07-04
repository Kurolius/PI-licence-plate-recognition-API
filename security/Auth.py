import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler():
    security = HTTPBearer()  # security is a class
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # deprecated is a string
    secret = 'SECRET' # secret key used to generate the token

    def get_password_hash(self, password):
        return self.pwd_context.hash(password) # return the hashed password

    def verify_password(self, plain_password, hashed_password): 
        return self.pwd_context.verify(plain_password, hashed_password) # return true if the password is correct

    def encode_token(self, user_id):
        payload = { # payload is a dictionary
            'exp': datetime.utcnow() + timedelta(days=0, minutes=60),# expires after 1 hour
            'iat': datetime.utcnow(),                               # issued at time of token generation    - token is valid from this time
            'sub': user_id # subject of the token
        }
        return jwt.encode(
            payload,# payload
            self.secret, # secret key used to generate the token
            algorithm='HS256' # algorithm used to generate the token
        )

    def decode_token(self, token): # token is a string
        try:# try to decode the token
            payload = jwt.decode(token, self.secret, algorithms=['HS256']) # here we decode the token
            return payload['sub'] # return the user id
        except jwt.ExpiredSignatureError: # if the token is expired
            #raise HTTPException(status_code=401, detail='Signature has expired') # raise an exception
            return "Signature has expired"
        except jwt.InvalidTokenError as e: # if the token is invalid
            #raise HTTPException(status_code=401, detail='Invalid token') # raise an exception
            return "Invalid token"

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)): # auth is a tuple (scheme, credentials) (scheme is a class) (credentials is a string) (auth is a class) 
        return self.decode_token(auth.credentials) # return the user id