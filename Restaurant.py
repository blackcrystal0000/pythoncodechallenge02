from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Create a base class for our models to inherit from.
Base = declarative_base()

# Define the `Restaurant` class, which represents a restaurant in our domain.
class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    reviews = relationship("Review", back_populates="restaurant")
    customers = relationship("Customer", secondary="reviews")

# Define the `Review` class, which represents a review of a restaurant left by a customer.
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)

    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship("Restaurant", back_populates="reviews")

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="reviews")

# Define the `Customer` class, which represents a customer in our domain.
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship("Review", back_populates="customer")