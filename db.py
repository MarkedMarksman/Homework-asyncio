import config
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine

PG_DSN = config.PG_DSN

engine = create_async_engine(PG_DSN)

Base = declarative_base()

class Characters(Base):
    __tablename__ = 'characters'
    
    id = sq.Column(sq.Integer, primary_key=True)
    birth_year = sq.Column(sq.String)
    eye_color = sq.Column(sq.String)
    films = sq.Column(sq.String)
    gender = sq.Column(sq.String)
    hair_color = sq.Column(sq.String)
    height = sq.Column(sq.String)
    homeworld = sq.Column(sq.String)
    mass = sq.Column(sq.String)
    name = sq.Column(sq.String)
    skin_color = sq.Column(sq.String)
    species = sq.Column(sq.String)
    starships = sq.Column(sq.String)
    vehicles = sq.Column(sq.String)
