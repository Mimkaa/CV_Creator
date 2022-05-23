from pydantic import BaseModel
from typing import Optional


class CreateExperienceRequest(BaseModel):
    period: str
    company: str
    description: str

class CreateEducationRequest(BaseModel):
    period: str
    course_school: str
    description: str
    cv_id: int

class CreateSkillRequest(BaseModel):
    name: str
    extend: int

class CreateHobbyRequest(BaseModel):
    name: str
    description: str

class CreateContactRequest(BaseModel):
    address: str
    phone_num: str
    email: str
    facebook: str
    telegram: str


# for user

class CreateUserRequest(BaseModel):
    username: str
    email: str
    hashed_password: str

class PatchUserRequest(BaseModel):
    username: Optional[str]=None
    email: Optional[str]=None

# for cv

class CreateCvRequest(BaseModel):
    user_id: int
    name:str

class ChangePassword(BaseModel):
    new_password: str




