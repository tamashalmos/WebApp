import pandas as pd
from sqlmodel import SQLModel,Field
from datetime import datetime


class Transactions(SQLModel,table=True):
    id: int = Field(default=None,primary_key=True)
    date: datetime
    value: int 
    partner: str | None



read_excel = pd.read_excel("adatok_excel.xlsx")


print(read_excel)