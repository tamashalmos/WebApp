import pandas as pd
from sqlmodel import Session
from db import engine
from importer import transaction_from_entry

with Session(engine) as session:
    df = pd.read_csv("adatok.csv", encoding="utf-16")

    for _, row in df.iterrows():
        tr = transaction_from_entry(row)
        if tr:
            session.add(tr)

    session.commit()
