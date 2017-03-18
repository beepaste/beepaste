import datetime # will be used to set default dates on models
from .meta import Base # we need to import our sqlalchemy metadata from which model classes will inherit
from sqlalchemy import (
    Column,
    Integer,
    Unicode,     # will provide Unicode field
    DateTime,    # time abstraction field
)

from passlib.apps import custom_app_context as beepastePWD

class Users(Base):
    __tablename__ = 'users'
    userID = Column(Integer, primary_key=True)
    username = Column(Unicode(255), nullable=False)
    password = Column(Unicode(255), nullable=False)
    email = Column(Unicode(63), nullable=False)
    resetToken = Column(Unicode(255), default=u'')
    status = Column(Unicode(3), default=u'00') # first digit is for verified account, 2nd is for waiting for reset password
    created = Column(DateTime, default=datetime.datetime.utcnow)

    def verifyPassword(self, password):
        return beepastePWD.verify(password, self.password)

    def setPassword(self, password):
        password_hash = beepastePWD.encrypt(password)
        self.password = password_hash
