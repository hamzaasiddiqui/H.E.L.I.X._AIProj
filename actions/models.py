# coding: utf-8
from sqlalchemy import BigInteger, Column, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Device(Base):
    __tablename__ = 'Device'

    d_id = Column(BigInteger, primary_key=True)
    d_type = Column(String, nullable=False)
    d_value = Column(BigInteger, server_default=text("0"))


class User(Base):
    __tablename__ = 'User'

    u_id = Column(BigInteger, primary_key=True)
    u_name = Column(String(50), nullable=False)
