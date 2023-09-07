from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Create a base class for our models to inherit from.
Base = declarative_base()

# Define the association table for the many-to-many relationship between Customer and Restaurant.
customer_restaurant_association_table = Table(
    'customer_restaurant_association',
    Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('restaurant_id', Integer, ForeignKey('restaurants.id'))
)

# Define the `Restaurant` class, which represents a restaurant in our domain.
class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    # Define the relationship with reviews.
    reviews = relationship("Review", back_populates="restaurant")

    # Define the many-to-many relationship with customers using the association table.
    customers = relationship("Customer", secondary=customer_restaurant_association_table, back_populates="restaurants")

# Define the `Review` class, which represents a review of a restaurant left by a customer.
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)

    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship("Restaurant", back_populates="reviews")

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="reviews")

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

# Define the `Customer` class, which represents a customer in our domain.
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    # Define the relationship with reviews.
    reviews = relationship("Review", back_populates="customer")
    restaurants = relationship("Restaurant", secondary=customer_restaurant_association_table, back_populates="customers")

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        if self.reviews:
            max_rating = 0
            favorite = None
            for restaurant in self.restaurants:
                rating = restaurant.average_rating()
                if rating > max_rating:
                    max_rating = rating
                    favorite = restaurant
            return favorite
        else:
            return None

    def add_review(self, restaurant, rating):
        review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        self.reviews.append(review)
        restaurant.reviews.append(review)

    def delete_reviews(self, restaurant):
        self.reviews = [review for review in self.reviews if review.restaurant != restaurant]
        restaurant.reviews = [review for review in restaurant.reviews if review.customer != self]

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

    def __repr__(self):
        return f"<Customer id={self.id} name='{self.full_name()}'>"
