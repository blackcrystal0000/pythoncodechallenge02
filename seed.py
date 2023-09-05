from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
from Restaurant import Restaurant, Review, Customer
import random

- Create an engine and session for the database.


creator_engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=creator_engine)
session = Session()