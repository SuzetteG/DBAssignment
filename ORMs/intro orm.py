from typing import Optional, List
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy import select 

engine = create_engine('mysql+mysqlconnector://root:Mina0630@localhost:3306/intro_orm')

class Base(DeclarativeBase):
    pass

user_pet = Table(
    "user_pet",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("pet_id", ForeignKey("pets.id"))
)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True)

# Many-to-many relationship
    pets: Mapped[List["Pet"]] = relationship(secondary=user_pet, back_populates="owners")

class Pet(Base):
    __tablename__ = "pets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    animal: Mapped[str] = mapped_column(String(100), nullable=False)
    
# Many-to-many relationship
    owners: Mapped[List["User"]] = relationship(secondary=user_pet, back_populates="pets")

# Create tables and session once
Base.metadata.create_all(engine)
print("Database and User/Pet tables created successfully.")
session = Session(engine)

bella = session.get(Pet, 1)
sunny = session.get(Pet, 2)

mina = session.get(User, 1)
hawke = session.get(User, 2)

#print(mina.pets)
#mina.pets.append(bella)
#mina.pets.append(sunny) 
#session.commit()
#print(f"Added pets Bella and Sunny to Mina.")

# Add Bella and Sunny for the correct user (e.g., Mina)
hawke = session.query(User).filter_by(name='Hawke').first()
if not hawke:
    hawke = User(name='Hawke', email='hawke@example.com')
    session.add(hawke)
    session.commit()
    print("New user Hawke added successfully.")

bella = Pet(name="Bella", animal="Cat")
sunny = Pet(name="Sunny", animal="Dog")
hawke.pets.append(bella)
hawke.pets.append(sunny)
session.add(bella)
session.add(sunny)
session.commit()
print("Added pets Bella and Sunny to Hawke.")

# Add Bella the Cat for Peter
#bella = Pet(name="Bella", animal="Cat")
#peter.pets.append(bella)
#session.add(bella)
#session.commit()
#print(f"Added pet Bella (Cat) for Peter.")

mina = User(name='Mina', email='mina@example.com')
hawke = User(name='Hawke', email='hawke@example.com')
session.add_all([mina, hawke])
session.commit()

sunny.owners.append(mina)
session.commit()
print("New users Mina and Hawke added successfully with pet Sunny.")

#Aries = Pet(name="Aries", animal="Dog")
#Luna = Pet(name="Luna", animal="Cat")

#session.add_all([mina, hawke, Aries, Luna])
#session.commit()
#print("New users Mina and Hawke, and pets Aries and Luna added successfully.")

