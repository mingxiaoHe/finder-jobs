#!/usr/bin/env python
# coding=utf-8

from sqlalchemy import String, Column, Integer, ForeignKey, Table, Date, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Job(Base):

    __tablename__ = "job"
    id = Column(Integer, primary_key=True)
    position_name = Column(String(64))
    company_short_name = Column(String(64))
    salary = Column(String(32))
    company_size = Column(String(32))
    position_id = Column(Integer, unique=True)
    finance_stage = Column(String(64))

    def __repr__(self):
        return "<公司名:%s>" % self.company_short_name

