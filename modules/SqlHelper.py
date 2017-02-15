#!/usr/bin/env python
# coding=utf-8

from sqlalchemy.orm import sessionmaker
from conf.settings import ConnParams
from modules import models

class SqlHelper(object):

    def __init__(self):
        engine = models.create_engine(ConnParams, echo=True)
        models.Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
