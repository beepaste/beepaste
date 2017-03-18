import datetime # will be used to set default dates on models
from .meta import Base # we need to import our sqlalchemy metadata from which model classes will inherit
from sqlalchemy import (
    Column,
    Integer,
    Unicode,     # will provide Unicode field
    UnicodeText, # will provide Unicode text field
    DateTime,    # time abstraction field
    Boolean,     # for expiration check
)

class API(Base):
    __tablename__ = 'api'
    apiID = Column(Integer, primary_key=True)
    ownerName = Column(Unicode(255), nullable=False)
    owenerEmail = Column(Unicode(63), nullable=False)
    apikey = Column(Unicode(255), nullable=False)
    status = Column(Unicode(2), default=u'0') # is api active or not!
    created = Column(DateTime, default=datetime.datetime.utcnow)

    def verifyApi(self, apikey):
        if apikey == self.apikey:
            return True
        return False
