import pandas as pd
from datetime import datetime
from sqlmodel import create_engine, Session, Field, SQLModel, select
from sqlalchemy import func


class Transactions(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, unique=True)
    date: datetime
    value: int
    partner: str | None

    @classmethod
    def from_entry(cls, transaction_entry):
        raw_value = str(transaction_entry["Összeg"]).replace("\xa0", "")
        return cls(
            date=transaction_entry["Könyvelés dátuma"],
            value=int(raw_value),
            partner=str(transaction_entry["Partner név"])
        )


# --- DATABASE ---
engine = create_engine("sqlite:///test.db")

# MINDEN INDULÁSKOR RESETELJÜK A TÁBLÁKAT
SQLModel.metadata.drop_all(bind=engine)
SQLModel.metadata.create_all(bind=engine)

db = Session(bind=engine)


# --- EXCEL BEOLVASÁS ---
a = pd.read_excel("adatok_excel.xlsx")

for index, row in a.iterrows():
    c_tr = Transactions.from_entry(row)
    db.add(c_tr)

db.commit()


# --- WOLT ÉRTÉKEK ÖSSZEGZÉSE (DB OLDALON) ---
result = db.exec(
    select(func.sum(Transactions.value)).where(Transactions.partner.ilike("%Wolt%"))
).all()

raw = result[0] if result else None

if isinstance(raw, (tuple, list)):
    total = raw[0]
else:
    total = raw

total = int(total) if total is not None else 0

print("Wolt összeg:", total)
