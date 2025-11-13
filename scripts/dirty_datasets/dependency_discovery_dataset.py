from scripts.utils.constants import RANDOM_SEED
from scripts.utils.setup import setup
setup()

import os
import pandas as pd
import numpy as np
from scripts.utils.path import get_directory_from_root
from datetime import timedelta
# paths
datasets_dir = get_directory_from_root(__file__, 'datasets')
clean_dataset_path = os.path.join(datasets_dir, 'df_clean.csv')

np.random.seed(RANDOM_SEED)

# read clean dataset
df = pd.read_csv(clean_dataset_path)



# Definizione delle città target con stati e zip code corrispondenti (ottengo (state,city)->zip_code, zip_code->state, zip_code->city)
target_cities = [
    ("Houston", "Texas", 77030),
    ("Orlando", "Florida", 32828),
    ("Los Angeles", "California", 90064),
    ("San Diego", "California", 92101),
    ("Nashville", "Indiana", 47448),
    ("Nashville", "Tennessee", 37201),
]

# Ripetizione ciclica delle città target per bilanciare il dataset
n = len(df)
repeated_cities = (target_cities * (n // len(target_cities) + 1))[:n]

# Aggiornamento delle colonne city, state e zip_code
df['city'], df['state'], df['zip_code'] = zip(*repeated_cities)

df['prev_sold_date']=pd.to_datetime(df['prev_sold_date'])

#Eliminazione colonne con un numero di valori distinti troppo basso
df = df.drop(['status', 'bed', 'bath'], axis=1)

columns = ['brokered_by', 'prev_sold_date']
for col in columns:
    # Trova i duplicati (mantieni il primo come valido)
    duplicates = df[df[col].duplicated(keep='first')]

    # Trova i numeri già esistenti nella colonna
    existing_numbers = set(df[col])

    # Limiti per i numeri casuali
    min_val = df[col].min()
    max_val = df[col].max()
    # Sostituisci i duplicati con numeri casuali non presenti
    new_values = []
    for i in range(len(duplicates)):
        while True:
            if col == 'brokered_by':
                random_value = np.random.randint(min_val, max_val)
            else:
                delta_days = (max_val - min_val).days
                random_days = np.random.randint(0, delta_days)
                random_value = min_val + timedelta(days=random_days)
            if random_value not in existing_numbers:
                break
        new_values.append(random_value)
        existing_numbers.add(random_value)

    # Aggiorna il DataFrame
    df.loc[duplicates.index, col] = new_values

target_price=[
    (111000, 12, 3321),
    (111000, 12, 5551),
    (125600, 12, 3321),
    (111000, 53, 3321)
]
repeated_prices = (target_price * (n // len(target_price) + 1))[:n]


# Define a single x and y coefficient for all cities
coefficients = {
    "x": 0.0001,
    "y": 0.1
}

# Randomly select 10% of rows to remain unchanged

unchanged_indices = np.random.choice(df.index, size=int(0.1 * n), replace=False)

# Create new columns for acre_lot and house_size with conditions
acre_lot = []
house_size = []
price=[]
replacement_counter = 0

for idx, row in df.iterrows():
    if idx in unchanged_indices:
        # Prendi la tupla corrispondente, scorrendo ciclicamente
        val = repeated_prices[replacement_counter % len(repeated_prices)]

        # Sostituisci con i valori della tupla
        price.append(val[0])
        acre_lot.append(val[1])
        house_size.append(int(val[2]))

        # Incrementa il contatore per passare alla prossima tupla
        replacement_counter += 1
    else:
        acre_lot.append(row['price'] * coefficients['x'])
        house_size.append(int(row['price'] * coefficients['y']))
        price.append(row['price'])
# Update the dataframe
df['acre_lot'] = acre_lot
df['house_size'] = house_size
df['price']=price

# Shuffle del dataset
df_shuffled = df.sample(frac=1, random_state=RANDOM_SEED+1).reset_index(drop=True)

# directories
dirty_datasets_dir = os.path.join(datasets_dir, 'dirty')
os.makedirs(dirty_datasets_dir, exist_ok=True)

depepdency_discovery_dir = os.path.join(dirty_datasets_dir, 'dependency_discovery')
os.makedirs(depepdency_discovery_dir, exist_ok=True)

# save to CSV
depepndency_discovery_path = os.path.join(depepdency_discovery_dir, f'dependency_discovery.csv')
df_shuffled.to_csv(depepndency_discovery_path, index=False)


print(f"Dependency discovery dataset was created.")