from datetime import datetime
from requests import session
from sqlalchemy import Integer, String, Column, ForeignKey, Boolean, DateTime, event
from sqlalchemy.orm import relationship
from application.database import Base, Session
from sqlalchemy.orm import declared_attr, declarative_mixin
from passlib.hash import pbkdf2_sha256 as sha256
import boto3
from application.config import Config


# cv and dependencies

@declarative_mixin
class RefTargetMixinCv:
    """ This is a mixin to provide all model instances in one-to-many relationship with cv model with cv
    and cv_id fields

    """

    @declared_attr
    def cv_id(cls):
        return Column('cv_id', ForeignKey('CVs.id'))

    @declared_attr
    def cv(cls):
        return relationship("CVModel", back_populates=cls.__tablename__.split("_")[0])


# @declarative_mixin
# class RefTargetMixinTemp:
#     @declared_attr
#     def template_id(cls):
#         return Column('template_id', ForeignKey('templates.id'))
#
#     @declared_attr
#     def template(cls):
#         return relationship("TemplateModel", back_populates=cls.__tablename__.split("_")[0])


class CommonMethods:
    """ This bad guy provides all models with common methods that contain the same logic,
    if they inherit from it (I think that it was a cool idea to make something like that)

    """

    @classmethod
    def find_by_id(cls, id, to_dict=True):
        """As the name of the method says it finds an instance of a model by id
                       Args:
                              id : int

                               cls:
                                   this method is used on a class, not on a class instance

                            to_dict:
                                    toggles the for of returned thing: if it is true returns a dict, else returns an
                                    Object


        """
        item = Session.query(cls).filter_by(id=id).first()
        if not item:
            return {}
        if to_dict:
            return cls.to_dict(item)
        else:
            return item

    @classmethod
    def find_by_foreign_id(cls, foreign_id, offset, limit) -> list:
        """This one is solely used for cv dependent models, it returns all records that have the foreign_id param
        as cv_id
           Args:
                foreign_id : int

                cls:
                                   this method is used on a class, not on a class instance

                offset:
                        how much to offset from the beginning of returned list
                limit:
                        how many to include starting from the offset


        """
        items = Session.query(cls).filter_by(cv_id=foreign_id).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(e) for e in items]

    @classmethod
    def return_all(cls, offset, limit, omit="") -> list:
        """returns all model records under the limit from the offset
                   Args:
                        foreign_id : int

                         cls:
                                   this method is used on a class, not on a class instance

                        offset:
                            how much to offset from the beginning of returned list
                        limit:
                            how many to include starting from the offset


        """
        items = Session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        retrieved = [cls.to_dict(a) for a in items]
        for d in retrieved:
            if omit in d.keys():
                d.pop(omit)
        return retrieved

    @classmethod
    def get_index(cls) -> int:
        """this is the method I use for returning an id for a newly create cv record in one of endpoints

                        Args:
                                 cls:
                                   this method is used on a class, not on a class instance




        """
        num_recs = Session.query(cls).count()
        return 1 if num_recs == 0 else (Session.query(cls).order_by(cls.id.desc()).first()).id + 1

    @classmethod
    def find_last(cls):
        """Finds the last record of a model in the db
                           Args:
                                cls:
                                   this method is used on a class, not on a class instance

                            returns:
                                an Object, do not remember name


        """
        return Session.query(cls).order_by(cls.id.desc()).first()

    @classmethod
    def delete_by_id(cls, id) -> int:
        """ Here we provide with a possibility of on instance deletion by id
                           Args:
                                id : int

                                 cls:
                                           this method is used on a class, not on a class instance


        """
        item = Session.query(cls).filter_by(id=id).first()
        if item:
            Session.delete(item)
            Session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        Session.add(self)
        Session.commit()

    @staticmethod
    def to_dict(item) -> dict:
        """An interesting method as for me, it turns an instance of a method into  a dict
        and then if it has any dependent instances of methods in one-to-many relation with it
        will turn them into a dict too, kinda like a recursion (or maybe it is)
                           Args:
                                item: it is a class
        """
        discerned = {name: v for name, v in item.__dict__.items() if
                     not (name.isascii() and name.startswith('__') and name.endswith(
                         '__') or name == 'cv' or name == 'template' or name == 'user')}

        for k, v in discerned.items():
            if type(v) == list:
                discerned[k] = [model.to_dict(model) for model in v]

        return discerned

    @classmethod
    def get_changeable_fields(item) -> list:
        """I needed this one for updating of a detail of a cv, to make long story short it gives me feilds
         that are not id cause I am not supposed to be changing these (I noticed that I accidentally passed a class
          as an item, I know that the convention does not allow it, but I am too tired of fixing stuff right now)
        """
        discerned = {name: v for name, v in item.__dict__.items() if
                     not (name.isascii() and name.startswith('__') and name.endswith(
                         '__') or name == 'cv' or name == 'template' or name == 'user')}
        return [k for k in discerned.keys() if ("id" not in k and not k == "_sa_class_manager")]


class ExperienceModel(CommonMethods, RefTargetMixinCv, Base):
    __tablename__ = "experiences_table"
    id = Column(Integer, primary_key=True)
    period = Column(String(150), nullable=False)
    company = Column(String(150), nullable=False)
    description = Column(String(500), nullable=False)


class EducationModel(CommonMethods, RefTargetMixinCv, Base):
    __tablename__ = "educations_table"
    id = Column(Integer, primary_key=True)
    period = Column(String(150), nullable=False)
    course_school = Column(String(150), nullable=False)
    description = Column(String(500), nullable=False)


class SkillsModel(CommonMethods, RefTargetMixinCv, Base):
    __tablename__ = "skills_table"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    extend = Column(Integer, nullable=False)


class HobbyModel(CommonMethods, RefTargetMixinCv, Base):
    __tablename__ = "hobbies_table"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String(500), nullable=False)


class ContactInfoModel(CommonMethods, RefTargetMixinCv, Base):
    __tablename__ = "contacts_table"
    id = Column(Integer, primary_key=True)
    address = Column(String(250), nullable=False)
    phone_num = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    facebook = Column(String(250), nullable=True)
    telegram = Column(String(250), nullable=True)


class ImageModel(CommonMethods, Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    photoname = Column(String(500), nullable=False)
    photo_url = Column(String(500), nullable=False)
    cv_id = Column(Integer, ForeignKey('CVs.id'))
    cv = relationship("CVModel", back_populates='image')


class CVModel(CommonMethods, Base):
    __tablename__ = 'CVs'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserModel", back_populates='CVs_ref')
    experiences = relationship(ExperienceModel, lazy=False,
                               cascade="all, delete-orphan",
                               foreign_keys="ExperienceModel.cv_id")

    educations = relationship(EducationModel, lazy=False,
                              cascade="all, delete-orphan",
                              foreign_keys="EducationModel.cv_id")

    skills = relationship(SkillsModel, lazy=False,
                          cascade="all, delete-orphan",
                          foreign_keys="SkillsModel.cv_id")

    hobbies = relationship(HobbyModel, lazy=False,
                           cascade="all, delete-orphan",
                           foreign_keys="HobbyModel.cv_id")

    contacts = relationship(ContactInfoModel, lazy=False,
                            cascade="all, delete-orphan",
                            foreign_keys="ContactInfoModel.cv_id")

    image = relationship(ImageModel, lazy=False,
                         uselist=False,
                         cascade="all, delete-orphan",
                         foreign_keys="ImageModel.cv_id")

    @classmethod
    def find_by_foreign_id(cls, foreign_id, offset, limit):
        """In this case it is just an overriding
        """
        items = Session.query(cls).filter_by(user_id=foreign_id).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(e) for e in items]


class UserModel(CommonMethods, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    hashed_password = Column(String(500), nullable=False)
    is_editor = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    CVs_ref = relationship(CVModel, lazy=False,
                           cascade="all, delete-orphan",
                           foreign_keys="CVModel.user_id")

    @staticmethod
    def generate_hash(password) -> sha256.hash:
        """there we generate a hash for a user password

            Args:
                password: str





        """
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash) -> bool:
        """there we verify a hash of a user password

                    Args:
                        password: str
                    hash:
                        sha256.hash

        """
        return sha256.verify(password, hash)

    @classmethod
    def find_by_username(cls, username, to_dict=True):
        """the same thing as find by Id but it finds by username
            Args:
                username:str,

                cls:
                    this method is used on a class, not on a class instance,

                to_dict:
                    toggles the for of returned thing: if it is true returns a dict, else returns an
                    Object

        """
        user = Session.query(cls).filter_by(username=username).first()
        if not user:
            return {}
        if to_dict:
            return cls.to_dict(user)
        else:
            return user


# class TemplateModel(CommonMethods, Base):
#     __tablename__ = "templates"
#     id = Column(Integer, primary_key=True)
#     experiences = relationship(ExperienceModel, lazy=False,
#                                cascade="all, delete-orphan",
#                                foreign_keys="ExperienceModel.template_id")
#
#     educations = relationship(EducationModel, lazy=False,
#                               cascade="all, delete-orphan",
#                               foreign_keys="EducationModel.template_id")
#
#     skills = relationship(SkillsModel, lazy=False,
#                           cascade="all, delete-orphan",
#                           foreign_keys="SkillsModel.template_id")
#
#     hobbies = relationship(HobbyModel, lazy=False,
#                            cascade="all, delete-orphan",
#                            foreign_keys="HobbyModel.template_id")
#
#     contacts = relationship(ContactInfoModel, lazy=False,
#                             cascade="all, delete-orphan",
#                             foreign_keys="ContactInfoModel.template_id")


class RevokedTokenModel(CommonMethods, Base):
    __tablename__ = 'revoked_tokens'
    id_ = Column(Integer, primary_key=True)
    jti = Column(String(120))
    blacklisted_at = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def is_jti_blacklisted(cls, jti) -> bool:
        """Checks if a token is in this table
                           Args:
                                jti : tiken id

                                 cls:
                                           this method is used on a class, not on a class instance




                """
        query = Session.query(cls).filter_by(jti=jti).first()
        return bool(query)

    @classmethod
    def return_all(cls, offset, limit, omit=''):
        """I suppose it is not supposed to be here but I wonna sleep, so I have no eager to investigate for now
                """
        items = Session.query(cls).order_by(cls.id_).offset(offset).limit(limit).all()
        retrieved = [cls.to_dict(a) for a in items]
        for d in retrieved:
            if omit in d.keys():
                d.pop(omit)
        return retrieved


# if an instance of ImageModel is deleted or cascaded removes an image binded with it and  stored in s3 database
@event.listens_for(ImageModel, "before_delete")
def delet_image_in_s3(mapper, connect, target) -> None:
    """This one is a pretty interesting too, whenever an instance of ImageModel is deleted whether it was using a
    "delete"
    endpoint or by cascading, in both cases it will delete the image stored in a s3 bucket
            Args:
                target:
                    ImageModel instance

                to be honest do not know what other params do

            """
    s3 = boto3.resource(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.REGION,

    )
    my_bucket = s3.Bucket(Config.S3_BUCKET_NAME)
    my_bucket.delete_objects(Delete={'Objects': [{'Key': target.photoname}]})
