import pandas as pd
from sqlmodel import SQLModel, Field, create_engine, Session,select
from datetime import datetime
from fastapi import FastAPI,Depends,HTTPException
from typing import Annotated

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: datetime
    value: int
    partner: str

    @classmethod
    def from_entry(cls, row):
        value = int(str(row["Összeg"]).replace("\xa0", ""))

        # pozitív értéket nem mentünk
        if value > 0:
            return None

        return cls(
            date=pd.to_datetime(row["Könyvelés dátuma"]).to_pydatetime(),
            value=value,
            partner=str(row["Partner név"])
        )


engine = create_engine("sqlite:///test2.db")

SQLModel.metadata.drop_all(bind=engine)
SQLModel.metadata.create_all(bind=engine)


with Session(engine) as db:
    df = pd.read_csv("adatok.csv", encoding="utf-16")
    inserted = 0
    skipped = 0
    for _, row in df.iterrows():
        tr = Transaction.from_entry(row)

        if tr is None:
            skipped += 1
            continue

        db.add(tr)
        inserted += 1

    db.commit()

print(f"Inserted: {inserted}, Skipped: {skipped}")


def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]


app = FastAPI()


@app.get("/")
def start():
    return "start"

@app.get("/transactions")
def read_transactions(db: SessionDep):
    return db.query(Transaction).all()

@app.get("/transactions/{transaction_id}")
def read_transaction(transaction_id: int,session: SessionDep) -> Transaction:
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@app.get("/transactions/by/{partner}")
def read_transactions_by_partner(
    partner: str,
    session: SessionDep
) -> list[Transaction]:
    statement = select(Transaction).where(Transaction.partner == partner)
    transactions = session.exec(statement).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this partner")

    return transactions


