from fastapi import Depends, HTTPException, APIRouter
from fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordBearer
from .schemas_auth import AuthModel, AuthModelLoging
from pydantic import BaseModel
from application.config import Config
from application.models import UserModel,RevokedTokenModel

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class Settings(BaseModel):
    authjwt_secret_key: str = Config.JWT_SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()


@auth_router.post('/login')
def login(user_find: AuthModelLoging, Authorize: AuthJWT = Depends()):
    user = UserModel.find_by_username(user_find.username)
    if not user:
        raise HTTPException(status_code=401, detail="No such user")
    if not UserModel.verify_hash(user_find.password,user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect  password ")
    additional = {'is_editor': user["is_editor"],"id": user["id"]}
    access_token = Authorize.create_access_token(subject=user["username"], user_claims=additional)
    refresh_token = Authorize.create_refresh_token(subject=user["username"], user_claims=additional)
    return {"access_token": access_token, "refresh_token": refresh_token}


@auth_router.post("/register")
def register(user_create: AuthModel, Authorize: AuthJWT = Depends()):
    user = UserModel(username = user_create.username, email = user_create.email, is_editor = user_create.is_editor,
                     hashed_password = UserModel.generate_hash(user_create.password))

    user.save_to_db()
    id = UserModel.find_by_username(user_create.username)["id"]
    additional = {'is_editor': user_create.is_editor,"id": id}
    access_token = Authorize.create_access_token(subject=user_create.username, user_claims=additional)
    refresh_token = Authorize.create_refresh_token(subject=user_create.username, user_claims=additional)
    return {"access_token": access_token, "refresh_token": refresh_token, "created_user_id": user.id}




@auth_router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    is_editor= Authorize.get_raw_jwt()["is_editor"]
    id=Authorize.get_raw_jwt()["id"]
    new_access_token = Authorize.create_access_token(subject=current_user, user_claims={"is_editor": is_editor,"id":id})
    return {"access_token": new_access_token}


@auth_router.post("/logout_access")
def logout_access(Authorize: AuthJWT = Depends(),token: str = Depends(oauth2_scheme)):
    Authorize.jwt_required()
    jti = Authorize.get_jti(token)
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.save_to_db()
        return {'message': 'Access token has been revoked'}
    except Exception as e:
        return {
            "message": "Something went wrong while revoking token",
            "error": repr(e)
        }, 500

@auth_router.post("/logout_refresh")
def logout_refresh(Authorize: AuthJWT = Depends(),token: str = Depends(oauth2_scheme)):
    Authorize.jwt_refresh_token_required()
    jti = Authorize.get_jti(token)
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.save_to_db()
        return {'message': 'Refresh token has been revoked'}
    except Exception as e:
        return {
            "message": "Something went wrong while revoking token",
            "error": repr(e)
        }, 500

# @auth_router.get("/revoked_tokens")
# def revoked(offset: int = 0, limit: int = 10):
#     return RevokedTokenModel.return_all(offset, limit)

