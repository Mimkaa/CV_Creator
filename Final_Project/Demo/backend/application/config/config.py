import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    MOCK_SQLALCHEMY_DATABASE_URI = os.getenv('MOCK_SQLALCHEMY_DATABASE_URI')
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    REGION = os.getenv("REGION")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    LINK_CHANGE_PASSWORD = os.getenv("LINK_CHANGE_PASSWORD")