import jwt
from fastapi import APIRouter, Depends, Request, UploadFile
from application.schemas import CreateUserRequest, PatchUserRequest, ChangePassword
from application.models import UserModel, ExperienceModel, HobbyModel, ContactInfoModel, EducationModel, SkillsModel, \
    CVModel, ImageModel
from application.auth import AuthJWT
from fastapi.security import OAuth2PasswordBearer

from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import List

from application.config import Config
import boto3

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

choices = {"experiences": ExperienceModel, "hobbies": HobbyModel, "contacts": ContactInfoModel,
           "educations": EducationModel, "skills": SkillsModel}


@users_router.get("/CVs")
def get_one(token: str = Depends(oauth2_scheme), Authorize: AuthJWT = Depends()):
    """An endpoint to retrieve a user with his/her CVs by id that is stored in payload of a JWT.

            Args:
                token: a token (long string with: header, payload, signature),
            Authorize: a class of fastapi_jwt_auth library with set up secret for JWTs
            (all endpoints with auth. should have it as "Depends" )


            Returns:
                dict/json because fastapi converts it automatically

            """
    Authorize.jwt_required()
    payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
    user = UserModel.find_by_id(id=payload.get("id"))
    return user


@users_router.get("/fields/{fields_of}")
def get_details_fields(fields_of: str) -> list:
    """An endpoint for getting fields of cv details (allows us not to care about front if a model gets changed).

                fields_of:
                    a string-key in choices dict at the top

                """
    return choices[fields_of].get_changeable_fields()


@users_router.get("/number_records/{record_of}")
def get_number_of_records(record_of: str) -> int:
    """I wanted to create records of CV details dynamically and apparently I needed some kind of a method to set id,
     so this thing does just that(utilizes a shared method of modals)

                   record_of:
                    a string-key in choices dict at the top
                   """
    return choices[record_of].get_index()


@users_router.post("/save_cv/")
async def save_cv(request: Request) -> None:
    """When I have created a couple of records on the front end I send them to be saved in a db
    there is the logic for that
                 Args:
                       request:
                        a Request object to get differing json from the body
                       """
    cv_data = await request.json()
    for k, v in cv_data.items():
        if type(v) == list:
            for comp in v:
                if not choices[k].find_by_id(comp["id"]):
                    new_record = choices[k](**comp)
                    new_record.save_to_db()


@users_router.get("/get_cv/{cv_id}")
def get_cv(cv_id: int):
    """A simple endpoint to get a CV by id
         Args:
               cv_id : int
         Returns:
                dict/json because fastapi converts it automatically
    """

    return CVModel.find_by_id(cv_id)


@users_router.post("/create_cv")
async def create_cv(request: Request, Authorize: AuthJWT = Depends()):
    """There a new CV is created
             Args:
                    request:
                        a Request object to get differing json from the body
                    Authorize :
                        if needed just add  Authorize.jwt_required() to enable dependence on a token
             Returns:
                    dict/json because fastapi converts it automatically
        """
    data_for_creation = await request.json()
    create = CVModel(**data_for_creation)
    CVModel.save_to_db(create)
    return {"new_cv_id": CVModel.find_last().id}


@users_router.delete("/delete_record/{type}/{record_id}")
async def delete_record(record_id: int, type: str):
    """There we just delete one of cv details by id
         Args:
                record_id:
                    speaks for itself
                type:
                    a string to find as a key in out choices dict
         Returns:
                dict/json because fastapi converts it automatically
    """
    code = choices[type].delete_by_id(record_id)
    if code == 404:
        return {"message": "something went wrong."}
    else:
        return {"message": f"record with id ({record_id}) was successfully removed."}


@users_router.delete("/delete_cv/{cv_id}")
async def delete_cv(cv_id: int, Authorize: AuthJWT = Depends()):
    """There we delete an entire cv
             Args:
                    cv_id:
                        speaks for itself
                    Authorize :
                        if needed just add  Authorize.jwt_required() to enable dependence on a token
                        (I am just not sure if it has to be here, it works with and without it, just this way it is simpler
                        when it is not utilized)
             Returns:
                    dict/json because fastapi converts it automatically
    """
    code = CVModel.delete_by_id(cv_id)
    if code == 404:
        return {"message": "something went wrong."}
    else:
        return {"message": f"CV with id ({cv_id}) was successfully removed."}


@users_router.patch("/edit/comp/{type}/{comp_id}")
async def edit_comp(comp_id: int, type: str, request: Request):
    """If any record was changed on front saving to db will happen here
                 Args:
                        comp_id:
                            a component id
                        type:
                            a string to find as a key in out choices dict
                        request:
                            a Request object to get differing json from the body
                 Returns:
                        dict/json because fastapi converts it automatically
        """
    comp = choices[type].find_by_id(comp_id, to_dict=False)
    update_data = await request.json()
    for k, v in update_data.items():
        setattr(comp, k, v)
    comp.save_to_db()
    return {"message": "updated"}


@users_router.post('/add_photo/{curriculum_vitae_id}')
async def add_photo(file: UploadFile, curriculum_vitae_id: int):
    """This is an interesting one, I have utilized s3 buckets from AWS for storing images
    so there we save an image that we chose on the frontend in a S3 Bucket, and then in our database
    go name and link to  the bucket
                     Args:
                            file:
                                it is a file but in majority of cases it will be an image)
                            curriculum_vitae_id:
                               cv_id

                     Returns:
                            dict/json because fastapi converts it automatically
    """

    # Upload to AWS S3
    s3 = boto3.resource(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.REGION,

    )
    bucket = s3.Bucket(Config.S3_BUCKET_NAME)
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={"ACL": "public-read"})
    uploade_file_url = f'https://{Config.S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}'

    # saving to db
    create = ImageModel(photoname=file.filename, photo_url=uploade_file_url, cv_id=curriculum_vitae_id)
    create.save_to_db()
    return {"new_image_id": ImageModel.find_last().id}


@users_router.delete("/delete_photo/{photo_id}")
async def delete_photo(photo_id: int):
    """And there an image is deleted
        Args:
               photo_id:
                   id of a photo


        Returns:
               dict/json because fastapi converts it automatically
       """

    code = ImageModel.delete_by_id(photo_id)
    if code == 404:
        return {"message": "something went wrong."}
    else:
        return {"message": f"photo with id ({photo_id}) was successfully removed."}


# mail stuff
class EmailSchema(BaseModel):
    email: List[EmailStr]
    url: str


conf = ConnectionConfig(
    MAIL_USERNAME=Config.SENDER_EMAIL,
    MAIL_PASSWORD=Config.SENDER_PASSWORD,
    MAIL_FROM=Config.SENDER_EMAIL,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


@users_router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    """this one is for sending a link to the form for password changing
            Args:
                   email:
                       must be something like that
                       {"email":["smt@smt.com"], "url": link to password changing form}



           """
    html = f"""
    <a href={email.url} >Change your password here</a>
    """
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@users_router.patch("/change_password/{user_id}")
async def change_password(user_id: int, request: Request):
    """And it is the actual password changing endpoint
               Args:
                      user_id:
                          id of a user
                    request:
                            a Request object to get differing json from the body


              """
    comp = UserModel.find_by_id(user_id, to_dict=False)
    passworddata = await request.json()
    new_encoded_password = UserModel.generate_hash(passworddata['new_password'])
    comp.hashed_password = new_encoded_password
    UserModel.save_to_db(comp)
    return {"message": "updated"}
