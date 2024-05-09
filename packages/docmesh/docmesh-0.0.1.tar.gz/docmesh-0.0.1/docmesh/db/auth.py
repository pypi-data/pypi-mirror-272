import os
import uuid

from typing import Optional

from sqlalchemy import create_engine, select, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session

if (url := os.getenv("MYSQL_URL")) is None:
    raise ValueError("You have to set mysql database url using environment `MYSQL_URL`.")
else:
    engine = create_engine(url)


class Base(DeclarativeBase):
    ...


class Auth(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True)
    entity_name = Column(String(64), unique=True)
    access_token = Column(String(32))


def _create_table():
    Base.metadata.create_all(engine)


def add_auth_for_entity(entity_name: str) -> str:
    _create_table()

    access_token = uuid.uuid4().hex
    with Session(engine) as session:
        session.add(Auth(entity_name=entity_name, access_token=access_token))
        session.commit()

    return access_token


def get_auth_from_entity(entity_name: str) -> Optional[str]:
    with Session(engine) as session:
        stmt = select(Auth.access_token).where(Auth.entity_name == entity_name)
        access_token = session.scalar(stmt)

    return access_token


def get_entity_from_auth(access_token: str) -> Optional[str]:
    with Session(engine) as session:
        stmt = select(Auth.entity_name).where(Auth.access_token == access_token)
        entity_name = session.scalar(stmt)

    return entity_name
