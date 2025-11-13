from scripts.utils.setup import setup
setup()

import pandas as pd
import os

from scripts.utils.data_pollution import make_dirty, shuffle_dataset
from scripts.utils.path import get_directory_from_root

percentages = [0.1, 0.3, 0.5]

datasets_dir = get_directory_from_root(__file__, 'datasets')  # datasets directory

# if datasets directory does not exist, raise an exception
if not os.path.exists(datasets_dir):
    raise Exception("There is no 'datasets' directory to work with. Consider running 'python -m scripts.get_clean_dataset' before running this script.")

df_clean = pd.read_csv(datasets_dir + '/df_clean.csv')

help_dir = os.path.join(datasets_dir, 'help')
dirty_dir = os.path.join(datasets_dir, 'dirty')

# make help datasets folder if it does not exist
if not os.path.exists(help_dir):
    os.makedirs(help_dir)

# make dirty datasets folder if it does not exist
if not os.path.exists(dirty_dir):
    os.makedirs(dirty_dir)

for percentage in percentages:
    df_dirty = shuffle_dataset(make_dirty(df_clean.copy(), percentage, help_dir), percentage, help_dir)
    csv_file_path = os.path.join(dirty_dir, 'df_dirty_' + str(int(percentage * 100)) + '.csv')
    df_dirty.to_csv(csv_file_path, index=False)
    print("Dirty dataset (" + str(int(percentage * 100)) + "%) successfully saved in: " + csv_file_path)