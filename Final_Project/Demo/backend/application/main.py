from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine
from .views import users_router, cvs_router
from .auth import auth_router
from fastapi.middleware.cors import CORSMiddleware


def setup_database(app) -> None:
    """A function to set up the batabase.

        Args:
            app: our fastapi application we accept it to track event: 'startup',
             when it fires up we execute creation of our database


        Returns:
            None

        """

    @app.on_event("startup")
    def create_tables():
        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)


def create_app() -> None:
    """this is our application factory it just creates app and all dependencies for it  to return a set up application.

            Args:


            Returns:
                None

            """
    app = FastAPI()

    # database
    setup_database(app)

    # middleware
    origins = [
        "http://localhost:3000",
        "localhost:3000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # routers
    app.include_router(users_router)
    app.include_router(cvs_router)
    app.include_router(auth_router)

    return app
