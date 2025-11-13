from scripts.utils.setup import setup
setup()

import os
from scripts.utils.path import get_directory_from_root

'''
Questo script genera un dataset uguale all'originale, ma shuffled.
Rimane la colonna 'duplicate' per tenere traccia di quale riga è duplicato di un'altra.
'''

percentages = [0.1, 0.3, 0.5]

datasets_dir = get_directory_from_root(__file__, 'datasets')  # datasets directory

# if datasets directory does not exist, raise an exception
if not os.path.exists(datasets_dir):
    raise Exception("There is no 'datasets' directory to work with. Consider running 'python -m scripts.get_clean_dataset' before running this script.")

dirty_dir = os.path.join(datasets_dir, 'dirty')

# if dirty directory does not exist, raise an exception
if not os.path.exists(datasets_dir):
    raise Exception("There is no 'dirty' directory to work with. Consider running 'python -m scripts.data_deduplication_dataset' before running this script.")


cleaning_dir = os.path.join(dirty_dir, 'data_cleaning')
profiling_dir = os.path.join(dirty_dir, 'data_profiling')

# if task directory does not exist, raise an exception
if not os.path.exists(datasets_dir):
    raise Exception("There is no 'task' directory to work with. Consider running 'python -m scripts.data_cleaning_dataset' before running this script.")

# make duplicates dirty shuffled folder
shuffled_dataset_dir = os.path.join(cleaning_dir, 'dirty_duplicates_shuffled')

# make duplicates dirty shuffled if it does not exist
if not os.path.exists(shuffled_dataset_dir):
    os.makedirs(shuffled_dataset_dir)

dirty_datasets_dir = os.path.join(cleaning_dir, 'dirty_duplicates')

# if dirty datasets directory does not exist, raise an exception
if not os.path.exists(datasets_dir):
    raise Exception("There is no 'dirty_duplicates' directory to work with. Consider running 'python -m scripts.data_deduplication_dataset' before running this script.")

import csv
import os

for percentage in percentages:
    # Legge il dataset originale
    csv_file = f"data_cleaning_{int(percentage * 100)}.csv"
    file_path = os.path.join(dirty_datasets_dir, csv_file)

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Estrai l'intestazione e normalizza i nomi delle colonne
    header = [col.strip() for col in rows[0]]

    # Determina l'indice della colonna 'duplicate'
    try:
        duplicate_index = header.index("duplicate")
    except ValueError:
        print(f"Colonna 'duplicate' non trovata nel file {file_path}")
        continue

    # Rimuovi la colonna dall'intestazione
    new_header = [col for i, col in enumerate(header) if i != duplicate_index]

    # Rimuovi la colonna 'duplicate' dai dati
    new_data = [
        [value for i, value in enumerate(row) if i != duplicate_index]
        for row in rows[1:]
    ]

    # Scrivi il nuovo dataset senza la colonna 'duplicate'
    new_content = [new_header] + new_data
    new_output_file = f"data_cleaning_{int(percentage * 100)}.csv"
    new_output_path = os.path.join(cleaning_dir, new_output_file)

    with open(new_output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_content)

    print(f"Dataset senza colonna 'duplicate' salvato in {new_output_path}")

    # Salva anche per il profiling
    new_output_file = f"data_profiling_{int(percentage * 100)}.csv"
    new_output_path = os.path.join(profiling_dir, new_output_file)

    with open(new_output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_content)

    print(f"Dataset senza colonna 'duplicate' salvato in {new_output_path}")