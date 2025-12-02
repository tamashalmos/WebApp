from engine import Hero, engine
from sqlmodel import SQLModel, Session

SQLModel.metadata.drop_all(bind=engine)
SQLModel.metadata.create_all(engine)

db = Session(engine)

db.add(Hero(name="Tomasz", secret_name="Tomszoyer", age=20))
db.add(Hero(name="Adam", secret_name="Papoca", age=33))
db.add(Hero(name="Domi", secret_name="SzamiMami", age=34))
db.add(Hero(name="Daci", secret_name="DaciPapa", age=30))
db.add(Hero(name="Adel", secret_name="Adus", age=30))

db.commit()