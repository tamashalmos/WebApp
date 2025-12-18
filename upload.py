import pandas as pd
from sqlmodel import Session,create_engine,SQLModel
from models import Transaction

def transaction_from_entry(row):
    value = int(str(row["Összeg"]).replace("\xa0", ""))

    if value > 0:
        return None

    return Transaction(
        date=pd.to_datetime(row["Könyvelés dátuma"]).to_pydatetime(),
        value=value,
        partner=str(row["Partner név"])
    )


engine = create_engine("sqlite:///test2.db")

SQLModel.metadata.drop_all(bind=engine)
SQLModel.metadata.create_all(bind=engine)


with Session(engine) as session:
    df = pd.read_csv("adatok.csv", encoding="utf-16")

    for _, row in df.iterrows():
        tr = transaction_from_entry(row)
        if tr:
            session.add(tr)

    session.commit()
