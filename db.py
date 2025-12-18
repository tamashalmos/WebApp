from sqlmodel import create_engine, Session
from fastapi import Depends
from typing import Annotated, Generator

engine = create_engine("sqlite:///test.db")

def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
