## CV builder

#### Quick description :
    It is a fully functioning app where a person can create a brief cv. I utilized React, Python fastapi, 
    and AWS S3 buckets.
#### How to launch it :
    You have to run 2  things: the backend and the frontend servers
    to run the backend simply run the file "run.py" with python:
```sh
python3 run.py
```
    
    and to start the frontend server :
    enter frontend directory and run this command:
```sh
npm start
```
## Functional
    1. First of all the user can registe or login 
![This is a alt text.](Final_Project/instances/ins1.png "This is a sample image.")

    2.  Then on the next page a user can create a new cvs (as many as he or she wants), logout, and change a password
    to change it the user will recieve a link on the email and then following it will be redirected to password changing form, by clicking a cv name a user will be redirected to the page of cv details
![This is a alt text.](Final_Project/instances/ins2.png "This is a sample image.")
    
    3. On this page users can add some information about them, and save it then as a pdf
    
![This is a alt text.](Final_Project/instances/ins3.png "This is a sample image.")
    
    4. in order for it to work the environmental variables have to be provided:
    
    SQLALCHEMY_DATABASE_URI
    MOCK_SQLALCHEMY_DATABASE_URI
    JWT_SECRET_KEY
    S3_BUCKET_NAME
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    REGION - not compulsory
    SENDER_EMAIL
    SENDER_PASSWORD
    LINK_CHANGE_PASSWORD
    



## Features

- S3 buckets are utilized to store images
- dynamically updated fields of cv details (whenever we change a model we do not have to do anything with the frontend)


