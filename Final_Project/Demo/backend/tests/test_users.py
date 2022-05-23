from application.models import UserModel, ExperienceModel, HobbyModel, ContactInfoModel, EducationModel, SkillsModel, \
    CVModel, ImageModel
import urllib.request
import os
from PIL import Image

template_data = {'id': 6, 'email': 'gop88315@gmail.com', 'is_editor': False, 'username': ' johnn',
                 'hashed_password': '$pbkdf2-sha256$29000$1Np77907R8i5lzIGgLB2bg$huQ03qp3DRc.fVVrrSkkRS651.5SLWCzVlT16uQoFnM',
                 'is_active': True, 'CVs_ref': [
        {'name': 'my_cv', 'id': 1, 'user_id': 1, 'experiences': [], 'hobbies': [], 'educations': [], 'contacts': [],
         'skills': [{'extend': 7, 'id': 1, 'cv_id': 1, 'name': 'solving problems'}], 'image': None}]}

just_cv_data_template = {'name': 'my_cv', 'id': 1, 'user_id': 1, 'experiences': [], 'hobbies': [], 'educations': [],
                         'contacts': [], 'skills': [{'extend': 7, 'id': 1, 'cv_id': 1, 'name': 'solving problems'}],
                         'image': None}

choices = {"experiences": ExperienceModel, "hobbies": HobbyModel, "contacts": ContactInfoModel,
           "educations": EducationModel, "skills": SkillsModel}


def test_getting_CVs_from_a_user(client, app, authentication_headers):
    response = client.get(
        '/users/CVs',
        headers=authentication_headers()
    )
    data = response.json()
    print(data)
    assert response.status_code == 200


def test_getting_fields(client, app):
    response = client.get(
        "/users/fields/hobbies")
    data = response.json()
    print(data)
    assert response.status_code == 200


def test_number_of_records(client, app):
    response = client.get(
        "/users/number_records/hobbies")
    data = response.json()
    print(data)
    assert response.status_code == 200


def test_save_cv(client, app):
    response = client.post("/users/save_cv/",
                           json=just_cv_data_template
                           )
    assert response.status_code == 200


def test_get_cv_by_id(client, app):
    response = client.get(
        "/users/get_cv/1")
    data = response.json()
    print(data)
    assert response.status_code == 200


def test_cv_creation(client, app):
    response = client.post("/users/create_cv",
                           json={"name": "new_cv2", "user_id": 1})
    data = response.json()
    print(CVModel.find_by_id(data['new_cv_id']))
    assert response.status_code == 200


def test_delete_record(client, app):
    response = client.delete("/users/delete_record/skills/1")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "record with id (1) was successfully removed."


def test_delete_CV(client, app):
    response = client.delete("/users/delete_cv/1")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "CV with id (1) was successfully removed."


def test_component_patch(client, app):
    client.patch("/users/edit/comp/skills/1",
                 json={
                     "name": "poop",
                     "extend": 3,
                 })
    comp = choices["skills"].find_by_id(1, to_dict=False)
    assert comp.name == "poop"
    assert comp.extend == 3


def test_photo_create(client, app):
    filename = "example_image.png"
    if not os.path.exists(filename):
        urllib.request.urlretrieve(
            'https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png',
            filename)

    if not ImageModel.find_by_foreign_id(1, 0, 10):
        response = client.post("/users/add_photo/1", files={"file": ("filename.png", open(filename, "rb"), "png/jpeg")})
        assert ImageModel.find_by_id(response.json()["new_image_id"])
    else:
        assert True


def test_photo_delete(client, app):
    response = client.delete(f"/users/delete_photo/{ImageModel.find_last().id}")
    assert response.status_code == 200


def test_email_sending(client, app):
    response = client.post("/users/email",
                           json={"email": ["gop88315@gmail.com"], "url": "somewhere"})
    assert response.json()["message"] == "email has been sent"


def test_change_password(client, app):
    client.patch("/users/change_password/1",
                 json={
                     "new_password": "new"
                 })
    assert UserModel.verify_hash("new", UserModel.find_by_id(1)["hashed_password"])
