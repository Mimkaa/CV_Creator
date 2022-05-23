from fastapi import APIRouter
from application.schemas import CreateCvRequest,CreateEducationRequest
from application.models import CVModel,EducationModel

cvs_router = APIRouter(
    prefix="/cvs",
    tags=["cvs"],
)


@cvs_router.post("/")
async def create(details: CreateCvRequest):
    create = CVModel(user_id =details.user_id, name= details.name
                       )
    CVModel.save_to_db(create)
    return {
        "created_id": create.id
    }
@cvs_router.get("/{cv_id}")
async def get_one(cv_id: int):
    user=CVModel.find_by_id(cv_id)
    if not user:
        return {"message": "the user not found."}
    return user

@cvs_router.post("/education")
async def create_education(details: CreateEducationRequest):
    create=EducationModel(period=details.period,course_school=details.course_school,description=details.description,cv_id=details.cv_id)
    EducationModel.save_to_db(create)
    return {
        "created_id": create.id
    }
