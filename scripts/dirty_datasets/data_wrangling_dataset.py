from scripts.utils.setup import setup
setup()

import os
import pandas as pd
from scripts.utils.path import get_directory_from_root
import random

# paths
datasets_dir = get_directory_from_root(__file__, 'datasets')
clean_dataset_path = os.path.join(datasets_dir, 'df_clean.csv')

# read clean dataset
df = pd.read_csv(clean_dataset_path)

# merge columns
df['address'] = df['street'] + ', ' + df['city'] + ', ' + df['state']
df.drop(columns=['street', 'city', 'state'], inplace=True)

# create new columns
names = [
    "James", "Betty", "Jack", "Jason", "Matthew", "Taylor", "Katherine", "Helen",
    "Joe", "Oliver", "Susan", "Anthony", "Emma", "Sophia", "Mason", "Ella",
    "Ethan", "Ava", "Daniel", "Charlotte", "Lucas", "Amelia", "Liam", "Isabella",
    "Noah", "Grace", "Alexander", "Chloe", "Benjamin", "Emily"
]

surnames = [
    "Smith", "Black", "Hudson", "Brown", "Miller", "Jones", "Johnson", "Davis",
    "Garcia", "Williams", "Anderson", "Moore", "Jackson", "Wilson", "Thompson",
    "Harris", "Martin", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall",
    "Allen", "Young", "King", "Scott", "Green", "Adams", "Baker"
]

df['broker_first_name'] = [random.choice(names) for _ in range(len(df))]
df['broker_surname'] = [random.choice(surnames) for _ in range(len(df))]

# add useless columns
df['currency'] = '$'

# splitting prev_sold_date column
df['prev_sold_date'] = pd.to_datetime(df['prev_sold_date'])
df['prev_sold_day'] = df['prev_sold_date'].dt.day
df['prev_sold_month'] = df['prev_sold_date'].dt.month
df['prev_sold_year'] = df['prev_sold_date'].dt.year

# dropping 'prev_sold_date'
df.drop(columns=['prev_sold_date'], inplace=True)

# ordering of the columns
df = df[['brokered_by', 'broker_first_name', 'broker_surname', 'status', 'price', 'currency', 'bed', 'bath', 'acre_lot',
         'address', 'zip_code', 'house_size', 'prev_sold_month', 'prev_sold_day', 'prev_sold_year']]

# directories
dirty_datasets_dir = os.path.join(datasets_dir, 'dirty')
os.makedirs(dirty_datasets_dir, exist_ok=True)

data_wrangling_dir = os.path.join(dirty_datasets_dir, 'data_wrangling')
os.makedirs(data_wrangling_dir, exist_ok=True)

# save to CSV
wrangling_path = os.path.join(data_wrangling_dir, f'data_wrangling.csv')
df.to_csv(wrangling_path, index=False)

print(f"Data Wrangling dataset was created.")