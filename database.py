from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/deepstream_db"


engine = create_engine(
    DATABASE_URL,
    echo=False
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Test database connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        print("DeepStream PostgreSQL database connected successfully!")
        print("Database test result:", result.fetchone())

except Exception as e:
    print("Database connection failed:")
    print(e)