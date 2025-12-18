from sqlmodel import create_engine, Session
from fastapi import Depends
from typing import Annotated

engine = create_engine("sqlite:///test2.db")

def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
