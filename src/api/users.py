import base64
import os
from typing import List
from fastapi import APIRouter, HTTPException
import sqlalchemy
import hashlib
from pydantic import BaseModel



from src import database as db

from fastapi.params import Query


router = APIRouter()

class LoginJson(BaseModel):
    username: str
    password: str


@router.post("/register_user/", tags=["add_user"])
def add_user(LoginJson: LoginJson):
    """
    This endpoint will allow users to create a new user. The user must provide a username
    and password. This endpoint check to make sure no duplicate usernames can be used.
    All passwords will be stored as hashes to protect user privacy. This endpoint will return
    the user_id of the newly created user.
    """
    username = LoginJson.username
    password = LoginJson.password

    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-16'), salt, 100000)
    hashed_password = salt + key

    stmt = sqlalchemy.select(db.users.c.user_id).where(db.users.c.user_name == username)
    with db.engine.begin() as conn:
      check_valid = conn.execute(stmt)
      if check_valid .rowcount > 0:
        raise HTTPException(status_code=404, detail="username already exists")
      
      # Encode hashed password using base64 
      encoded_password = base64.b64encode(hashed_password).decode('utf-8')

      conn.execute(
              sqlalchemy.insert(db.users),
              [
                  {"user_name": username,
                  "password": encoded_password },
              ],
            
      )

      stmt = sqlalchemy.select(db.users.c.user_id, db.users.c.password).where(db.users.c.user_name == username)
      result = conn.execute(stmt)
      for row in result:
         user_id = row.user_id
         hashed_password = row.password

    return user_id


@router.post("/login_user/", tags=["validate_user"])
def validate_user_login(LoginJson: LoginJson):
   """
    This endpoint will allow users to check if their password is valid. This endpoint 
    will throw an error if the user does not exist, or if the passowrd is incorrect.
    """
   
   username = LoginJson.username
   password = LoginJson.password

   stmt = sqlalchemy.select(db.users.c.password).where(db.users.c.user_name == username)
   with db.engine.begin() as conn:
      result = conn.execute(stmt)
      if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="user not found")
      for row in result:
         hashed_password = row.password

    # Decode hashed password from base64
   hashed_password = base64.b64decode(hashed_password.encode('utf-8'))

   salt =hashed_password[:32]
   key = hashed_password[32:]
   check_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-16'), salt, 100000)

   if key == check_key:
        return {"message": "Password is correct"}
   else:
        return {"message": "Password is incorrect"}
   
