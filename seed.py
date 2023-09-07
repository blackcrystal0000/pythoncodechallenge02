from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
from restaurant import Restaurant, Review, Customer
import random

fake = Faker()

# Create an engine and session for the database.
creator_engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=creator_engine)
session = Session()

# Use Faker to generate fake data for the restaurant, review and customer.
for i in range(10):
    restaurant = Restaurant(name=fake.company(),
                            price=random.randint(1, 4))
    session.add(restaurant)
    session.commit()

for i in range(10):
    customer = Customer(first_name=fake.first_name(),
                        last_name=fake.last_name())
    session.add(customer)
    session.commit()

for i in range(10):
    review = Review(star_rating=random.randint(1, 5),
                    restaurant_id=random.randint(1, 10),
                    customer_id=random.randint(1, 10))
    session.add(review)
    session.commit()