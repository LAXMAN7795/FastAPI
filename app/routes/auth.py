from fastapi import APIRouter,Depends,status,Response,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils,oauth2
router = APIRouter()

@router.post("/login")
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    # user_credential returns username and password
    user = db.query(models.User).filter(models.User.email==user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credential")
    # function verify is in the utils.py to check the plain_password and hashed password is same or not
    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credential")

    #create token
    # return token
    access_token = oauth2.create_access_token(data={"user_id":user.id})# user_id is payload here 
    return {"access_token":access_token,"token_type":"bearer"}
