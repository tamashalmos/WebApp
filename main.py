from fastapi import FastAPI, HTTPException
from sqlmodel import select

from db import SessionDep
from models import Transaction

app = FastAPI()

@app.get("/")
def start():
    return "start"

@app.get("/transactions")
def read_transactions(session: SessionDep) -> list[Transaction]:
    statement = select(Transaction)
    return session.exec(statement).all()

@app.get("/transactions/{transaction_id}")
def read_transaction(transaction_id: int,session: SessionDep)  -> Transaction:
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