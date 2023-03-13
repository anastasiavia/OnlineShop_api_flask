from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class AddressSchema(Base):
    __tablename__ = "address"
    idaddress = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    house_number = Column(Integer, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserSchema(Base):
    __tablename__ = 'user'
    iduser = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    address_id = Column(Integer, ForeignKey("address.idaddress"))
    is_admin = Column(Boolean, default=False)

    addressUser = relationship(AddressSchema, backref='user', lazy="joined", foreign_keys=[address_id])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ItemSchema(Base):
    __tablename__ = "item"
    iditem = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    status = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class OrderSchema(Base):
    __tablename__ = "order"

    idorder = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=True)
    orderDate = Column(DateTime, nullable=False)
    status = Column(String(255), nullable=False)
    payment_method = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("user.iduser"))
    item_id = Column(Integer, ForeignKey("item.iditem"))

    item_order = relationship(ItemSchema, backref='order', lazy="joined", foreign_keys=[item_id])
    user_order = relationship(UserSchema, backref='order', lazy="joined", foreign_keys=[user_id])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
