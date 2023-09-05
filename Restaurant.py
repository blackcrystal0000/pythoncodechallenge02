from sqlalchemy.ext.declarative import declarative_base

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
