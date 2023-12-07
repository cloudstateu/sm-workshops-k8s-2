import random
from datetime import datetime
import time
import logging
import os
import pymongo

logging.basicConfig(level=logging.INFO)

FIRST_NAMES = ['John', 'Jane', 'Michael', 'Emily', 'Robert', 'Linda']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Davis']
EMAIL_DOMAINS = ['example.com', 'sample.net', 'demo.org']
CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia']
PROFESSIONS = ['Engineer', 'Doctor', 'Lawyer', 'Teacher', 'Architect', 'Developer']
WEBSITES = ['exampleShop.com', 'newsSite.net', 'socialPlatform.org']
ACTIVITIES = ['visited website', 'made a purchase', 'commented on a post', 'liked a product']

def generate_address():
    street = f"{random.choice(LAST_NAMES)} St."
    house_number = random.randint(1, 100)
    postal_code = f"{random.randint(10000, 99999)}"
    city = random.choice(CITIES)
    
    return f"{street} {house_number}, {postal_code}, {city}"

def generate_user():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(EMAIL_DOMAINS)}"
    birth_date = f"{random.randint(1950, 2005)}-{random.randint(1, 12)}-{random.randint(1, 28)}"
    profession = random.choice(PROFESSIONS)
    address = generate_address()
    city = address.split(',')[-1].strip()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'birth_date': birth_date,
        'profession': profession,
        'address': address,
        'city': city,
        'timestamp': timestamp
    }
    
    return user

def simulate_user_activity(user):
    website = random.choice(WEBSITES)
    activity = random.choice(ACTIVITIES)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    activity_log = {
        'user_email': user['email'],
        'website': website,
        'activity': activity,
        'timestamp': timestamp
    }
    
    return activity_log

def main():
    while True:
        user_data = generate_user()
        activity_data = simulate_user_activity(user_data)
        
        logging.info(f"User Data: {user_data}")
        logging.info(f"User Activity: {activity_data}")
        
        CONN_STR = os.getenv('CONNECTION_STRING')
        client = pymongo.MongoClient(CONN_STR)
        database = client[os.getenv('COSMOS_DATABASE_NAME')]
        user_collection = database[os.getenv('USER_COLLECTION_NAME')]
        activity_collection = database[os.getenv('ACTIVITY_COLLECTION_NAME')]

        user_collection.insert_one(user_data)
        activity_collection.insert_one(activity_data)

        
        time.sleep(30)

if __name__ == "__main__":
    main()
