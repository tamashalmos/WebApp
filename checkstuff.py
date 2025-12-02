import pandas as pd
from datetime import datetime
from sqlmodel import create_engine, Session, Field, SQLModel

class Transactions(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, unique=True)
    date : datetime
    value: int
    partner: str | None

    @classmethod
    def from_entry(cls, transaction_entry):
        return cls(
            date=transaction_entry["Könyvelés dátuma"],
            value=transaction_entry["Összeg"],
            partner=transaction_entry["Partner név"]
        )

engine = create_engine("sqlite:///test.db")

# SQLModel.metadata.drop_all(bind=engine)
# SQLModel.metadata.create_all(bind=engine)

db = Session(bind=engine)

# a = pd.read_excel("adatok_excel.xlsx")

# for index, row in a.iterrows():
#     c_tr = Transactions.from_entry(row)
#     db.add(c_tr)
# db.commit()

wolt = db.query(Transactions).where(Transactions.partner == "Wolt").all()
for data in wolt:
    print(data)
