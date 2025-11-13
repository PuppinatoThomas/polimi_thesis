from scripts.utils.setup import setup
setup()

import os
import subprocess
import tempfile
import zipfile
import pandas as pd

from scripts.utils.constants import ROWS_TO_SAMPLE, RANDOM_SEED
from scripts.utils.path import get_directory_from_root
from scripts.utils.data_enrichment import generate_random_address

# Kaggle API command
command = "kaggle datasets download -d ahmedshahriarsakib/usa-real-estate-dataset"

# Download dataset in a temporary directory
with tempfile.TemporaryDirectory() as temp_dir:

    download_command = f"{command} -p {temp_dir}"

    try:
        print("Downloading Dataset from Kaggle...")
        subprocess.run(download_command, check=True, shell=True)

    except subprocess.CalledProcessError as e:
        print(f"Error while downloading from Kaggle: {e}")

    with zipfile.ZipFile(os.path.join(temp_dir, 'usa-real-estate-dataset.zip'), 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    print("Extracting Dataset...")

    df = pd.read_csv(os.path.join(temp_dir, 'realtor-data.zip.csv'))

    print("Preparing Dataset...")

    # Drop incomplete rows
    df_cleaned = df.dropna()

    # Reset the index after dropping rows
    df_cleaned = df_cleaned.reset_index(drop=True)

    # Sample a small subset of the cleaned dataset
    df_sampled = df_cleaned.sample(n=ROWS_TO_SAMPLE, random_state=RANDOM_SEED)

    # Reassign indices
    df_sampled = df_sampled.reset_index(drop=True)

    # Add meaningful data to 'street' column
    df_sampled['street'] = df_sampled.apply(lambda row: generate_random_address(), axis=1)

    # Convert columns to integers
    df_sampled['bed'] = df_sampled['bed'].astype(int, errors='ignore')
    df_sampled['bath'] = df_sampled['bath'].astype(int, errors='ignore')
    df_sampled['zip_code'] = df_sampled['zip_code'].astype(int, errors='ignore')
    df_sampled['house_size'] = df_sampled['house_size'].astype(int, errors='ignore')
    df_sampled['brokered_by'] = df_sampled['brokered_by'].astype(int, errors='ignore')
    df_sampled['price'] = df_sampled['price'].astype(int, errors='ignore')

    datasets_dir = get_directory_from_root(__file__, 'datasets')  # datasets directory

    # if datasets directory does not exist, create it
    if not os.path.exists(datasets_dir):
        os.makedirs(datasets_dir)

    # complete CSV path
    csv_file_path = os.path.join(datasets_dir, 'df_clean.csv')

    # write the CSV file into the desired folder
    df_sampled.to_csv(csv_file_path, index=False)

    print(f"Dataset successfully saved in: {csv_file_path}")