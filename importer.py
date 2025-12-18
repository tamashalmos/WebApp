import pandas as pd
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
