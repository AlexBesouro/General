from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Format of a connection string to pass to sqlalchemy
SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname:port/<database_name>"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:besouro@localhost:5432/fastapi_example"

# engine to connect to DB

# Creating the SQLAlchemy engine to connect to the PostgreSQL database, engine- its the starting point for any SQLAlchemy application
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine,  # sessionmaker factory for creating new Session objects
                            autoflush=False,  # bind=engine binds the session to the engine created above
                            expire_on_commit=False)  # prevent attributes from being expired after commit


def get_db():
    with SessionLocal() as session:
        yield session
