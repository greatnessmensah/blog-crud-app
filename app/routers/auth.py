from fastapi import status, HTTPException, Response, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
