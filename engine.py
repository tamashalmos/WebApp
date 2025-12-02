from sqlmodel import create_engine, Session, Field, SQLModel

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


engine = create_engine("sqlite:///foo.db")

def get_db():
    with Session(engine) as c_session:
        yield c_session
