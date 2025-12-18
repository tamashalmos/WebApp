from sqlmodel import SQLModel, Field
from datetime import date
import pandas as pd

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: date
    value: int
    partner: str

    @classmethod
    def from_entry(cls, row):
        value = int(str(row["Összeg"]).replace("\xa0", ""))

        # pozitív értéket nem mentünk
        if value > 0:
            return None

        return cls(
            date=pd.to_datetime(row["Könyvelés dátuma"]).date(),
            value=value,
            partner=str(row["Partner név"])
        )