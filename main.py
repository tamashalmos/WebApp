from typing import Union
from sqlmodel import Session
from fastapi import FastAPI, Depends,UploadFile,File
from engine import get_db, Hero
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
"""  
@app.post("/hero")
def create_hero(hero_name: str, hero_secret_name: str, hero_age: int, db: Session = Depends(get_db)) -> Hero:
    obj = Hero(
        name=hero_name,
        secret_name=hero_secret_name,
        age=hero_age,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/hero")
def get_hero(hero_id: int, db: Session = Depends(get_db)) -> Hero:
    return db.query(Hero).where(Hero.id == hero_id).first()

@app.get("/heroes")
def get_heroes(db: Session = Depends(get_db)) -> list[Hero]:
    return db.query(Hero).all()

@app.delete("/hero")
def delete_hero(hero_id: int, db: Session = Depends(get_db)):
    obj = db.query(Hero).where(Hero.id == hero_id).first()
    if obj:
        db.delete(obj)
        db.commit()
"""

@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):

    if file.filename.lower().endswith(".csv"):
        df = pd.read_csv(file.file)
    else:
        df = pd.read_excel(file.file)

    return df.to_dict(orient="records")
