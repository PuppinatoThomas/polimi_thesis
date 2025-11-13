from scripts.utils.constants import RANDOM_SEED
from scripts.utils.setup import setup
setup()

import os
import random
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


task_dir = os.path.join(dirty_dir, 'data_cleaning')

# if task directory does not exist, raise an exception
if not os.path.exists(datasets_dir):
    raise Exception("There is no 'task' directory to work with. Consider running 'python -m scripts.data_cleaning_dataset' before running this script.")

# make duplicates dirty shuffled folder
shuffled_dataset_dir = os.path.join(task_dir, 'dirty_duplicates_shuffled')

# make duplicates dirty shuffled if it does not exist
if not os.path.exists(shuffled_dataset_dir):
    os.makedirs(shuffled_dataset_dir)

dirty_datasets_dir = os.path.join(task_dir, 'dirty_duplicates')

# if dirty datasets directory does not exist, raise an exception
if not os.path.exists(datasets_dir):
    raise Exception("There is no 'dirty_duplicates' directory to work with. Consider running 'python -m scripts.data_deduplication_dataset' before running this script.")

for percentage in percentages:
    # Legge il dataset originale come stringa
    csv_file = f"data_cleaning_{int(percentage * 100)}.csv"
    file_path = os.path.join(dirty_datasets_dir, csv_file)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Divide il contenuto in righe
    rows = content.strip().split('\n')

    # Estrae l'intestazione e i dati
    header = rows[0]
    data = rows[1:]

    # Crea una lista di righe con gli indici originali
    indexed_data = [(i, row) for i, row in enumerate(data)]

    # Effettua lo shuffle casuale del dataset
    random.seed(RANDOM_SEED)
    shuffled_data = random.sample(indexed_data, len(indexed_data))

    # Crea una mappatura tra vecchi indici e nuovi indici
    old_to_new_index = {old_index: new_index for new_index, (old_index, _) in enumerate(shuffled_data)}

    # Funzione per aggiornare la colonna 'duplicate'
    def update_duplicates(row):
        parts = row.split(';')  # Supponendo che il delimitatore sia ';'
        duplicate_value = parts[-1]  # La colonna 'duplicate' è l'ultima
        if duplicate_value == '-1' or duplicate_value == "-1":  # Nessun duplicato
            return row
        else:
            indices = map(int, duplicate_value.split(','))
            updated_indices = [old_to_new_index[i] for i in indices]
            parts[-1] = ','.join(map(str, updated_indices))
            return ';'.join(parts)

    # Aggiorna i valori nella colonna 'duplicate'
    updated_data = [update_duplicates(row) for _, row in shuffled_data]

    # Ricostruisce il contenuto del file CSV
    shuffled_content = '\n'.join([header] + updated_data)

    # Salva il dataset aggiornato
    output_file = f"shuffled_dirty_dataset_{int(percentage * 100)}.csv"
    output_path = os.path.join(shuffled_dataset_dir, output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(shuffled_content)

    print(f"Dataset riorganizzato e salvato in {output_path}")

    # === Rimuovi la colonna 'duplicate' e salva il nuovo dataset ===
    # Determina l'indice della colonna 'duplicate'
    duplicate_index = header_parts.index("duplicate")

    # Rimuovi la colonna dall'intestazione
    new_header = ';'.join([col for i, col in enumerate(header_parts) if i != duplicate_index])

    # Funzione per rimuovere la colonna 'duplicate' dalle righe
    def remove_duplicate_column(row):
        parts = row.split(';')
        new_parts = [value for i, value in enumerate(parts) if i != duplicate_index]
        return ';'.join(new_parts)

    # Applica la funzione a tutte le righe
    new_data = [remove_duplicate_column(row) for row in updated_data]

    # Ricostruisce il contenuto del nuovo file CSV
    new_content = '\n'.join([new_header] + new_data)

    # Salva il nuovo dataset nel percorso specificato
    new_output_file = f"data_cleaning_{int(percentage * 100)}.csv"
    new_output_path = os.path.join(task_dir, new_output_file)
    with open(new_output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Dataset senza colonna 'duplicate' salvato in {new_output_path}")