import numpy as np

from scripts.utils.data_pollution import inject_duplicates, make_single_value_outlier_detection_dirty, \
    make_single_value_data_standardization_dirty, make_single_value_data_imputation_dirty
from scripts.utils.setup import setup
setup()

import os
import pandas as pd
from scripts.utils.constants import PERCENTAGES, RANDOM_SEED
from scripts.utils.path import get_directory_from_root

# paths
datasets_dir = get_directory_from_root(__file__, 'datasets')
clean_dataset_path = os.path.join(datasets_dir, 'df_clean.csv')

# read clean dataset
df = pd.read_csv(clean_dataset_path)

# directories
dirty_datasets_dir = os.path.join(datasets_dir, 'dirty')
os.makedirs(dirty_datasets_dir, exist_ok=True)

data_cleaning_dir = os.path.join(dirty_datasets_dir, 'data_cleaning')
os.makedirs(data_cleaning_dir, exist_ok=True)

data_cleaning_no_dirty_duplicates_dir = os.path.join(data_cleaning_dir, 'no_dirty_duplicates')
os.makedirs(data_cleaning_no_dirty_duplicates_dir, exist_ok=True)

# create dirty datasets
for perc in PERCENTAGES:
    # copy the original dataset
    df_modified = df.copy()

    duplicated_df = inject_duplicates(df_modified, perc / 100)

    # Aggiunge una nuova colonna 'old_index' che contiene gli indici originali
    duplicated_df['old_index'] = duplicated_df.index

    # Effettua lo shuffle casuale del dataset
    shuffled_df = duplicated_df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)

    # Creiamo una mappatura tra vecchi indici e nuovi indici
    old_to_new_index = {row['old_index']: new_index for new_index, row in shuffled_df.iterrows()}

    # Funzione per aggiornare la colonna 'duplicate' utilizzando 'old_index'
    def update_duplicates(value):
        if value == -1 or value == "-1":  # Nessun duplicato
            return -1
        else:
            # Traduci i vecchi indici in nuovi indici
            indices = map(int, str(value).split(','))
            updated_indices = [old_to_new_index[idx] for idx in indices]
            return ','.join(map(str, updated_indices))

    # Applica la funzione alla colonna 'duplicate'
    shuffled_df['duplicate'] = shuffled_df['duplicate'].apply(update_duplicates)

    # Rimuove la colonna temporanea 'old_index'
    shuffled_df.drop(columns=['old_index'], inplace=True)

    # Identifica le righe con duplicati negativi (-1)
    negative_duplicates = shuffled_df[shuffled_df['duplicate'] == -1]

    # Numero di righe da rimuovere
    num_to_remove = perc

    # Seleziona casualmente le righe da rimuovere
    rows_to_remove = negative_duplicates.sample(n=num_to_remove, random_state=RANDOM_SEED).index

    # Ordina gli indici delle righe da rimuovere per garantire un aggiornamento sequenziale
    rows_to_remove = sorted(rows_to_remove)

    # Elimina le righe selezionate dal dataframe
    shuffled_df.drop(index=rows_to_remove, inplace=True)


    # Funzione per aggiornare i valori della colonna 'duplicate'
    def update_duplicate_values(value, removed_idxs):
        if pd.isna(value) or value in [-1, "-1"]:
            return -1  # Nessun duplicato, restituisce -1
        try:
            # Trasforma il valore in una lista di indici
            indices = list(map(int, str(value).split(',')))
            updated_indices = []
            for idx in indices:
                # Se l'indice è stato rimosso, scartalo
                if idx in removed_idxs:
                    continue
                # Calcola il decremento del valore in base a quante righe precedenti sono state rimosse
                decrement = sum(1 for removed_idx in removed_idxs if removed_idx < idx)
                updated_indices.append(idx - decrement)
            # Se non rimangono indici validi, restituisci -1
            if not updated_indices:
                return -1
            return ','.join(map(str, updated_indices))
        except:
            raise ("Error while updating duplicate values: " + str(value))


    # Aggiorna i valori della colonna 'duplicate' dopo la rimozione delle righe
    removed_indices = list(rows_to_remove)
    shuffled_df['duplicate'] = shuffled_df['duplicate'].apply(lambda x: update_duplicate_values(x, removed_indices))

    col_map = {
        0: "brokered_by",
        1: "status",
        2: "price",
        3: "bed",
        4: "bath",
        5: "acre_lot",
        6: "street",
        7: "city",
        8: "state",
        9: "zip_code",
        10: "house_size",
        11: "prev_sold_date"
    }

    # Imposta il seed per la riproducibilità
    np.random.seed(RANDOM_SEED)

    # Determina il numero di celle totali richiesto
    values_per_column = perc  # Numero di valori da selezionare per ogni colonna
    total_cells = values_per_column * (shuffled_df.shape[1] - 1)  # Escludi la colonna 'duplicate'

    # Genera maschera (righe e colonne)
    rows = []
    cols = []
    for col_index in range(shuffled_df.shape[1] - 1):  # Escludi la colonna 'duplicate'
        col_rows = np.random.choice(shuffled_df.shape[0], values_per_column, replace=False).tolist()
        rows.extend(col_rows)
        cols.extend([col_index] * values_per_column)

    # Combina righe e colonne in una lista di tuple (maschera)
    mask = list(zip(rows, cols))

    # Definizione dei tipi di sporcature
    noise_types = ['outlier_detection', 'data_standardization', 'data_imputation']

    # Colonne applicabili per ciascun tipo di sporcatura
    outlier_columns = {2, 3, 4, 5, 10}
    standardization_columns = {1, 2, 3, 4, 6, 8, 10, 11}

    # Inizializza la struttura per memorizzare le sporcature
    grouped_masks = {noise_type: [] for noise_type in noise_types}

    # Filtra la maschera per colonna e assegna equamente le celle a ogni tipo di sporcatura
    for col_index in range(shuffled_df.shape[1] - 1):  # Escludi la colonna 'duplicate'
        # Celle della colonna corrente
        col_cells = [cell for cell in mask if cell[1] == col_index]

        # Determina i tipi applicabili per la colonna
        applicable_noise_types = []
        if col_index in outlier_columns:
            applicable_noise_types.append('outlier_detection')
        if col_index in standardization_columns:
            applicable_noise_types.append('data_standardization')
        applicable_noise_types.append('data_imputation')  # Sempre applicabile

        # Determina il numero di celle per ciascun tipo
        cells_per_type = len(col_cells) // len(applicable_noise_types)
        remainder = len(col_cells) % len(applicable_noise_types)

        # Distribuisci equamente le celle tra i tipi applicabili
        start_idx = 0
        for i, noise_type in enumerate(applicable_noise_types):
            end_idx = start_idx + cells_per_type + (1 if i < remainder else 0)  # Gestisce i residui
            grouped_masks[noise_type].extend(col_cells[start_idx:end_idx])
            start_idx = end_idx

    # Stampa di controllo per verificare la distribuzione
    for noise_type, cells in grouped_masks.items():
        print(f"{noise_type}: {len(cells)} cells")

    dirty_df = shuffled_df.copy()

    # Applica le sporcature
    for noise_type, cell_group in grouped_masks.items():
        for row, col in cell_group:
            if noise_type == 'outlier_detection':
                dirty_df.iat[row, col] = make_single_value_outlier_detection_dirty(shuffled_df.iat[row, col],
                                                                                   col_map[col], shuffled_df)
            elif noise_type == 'data_standardization':
                dirty_df.iat[row, col] = make_single_value_data_standardization_dirty(shuffled_df.iat[row, col],
                                                                                      col_map[col])
            elif noise_type == 'data_imputation':
                dirty_df.iat[row, col] = make_single_value_data_imputation_dirty(col_map[col])
            else:
                raise ValueError('Unknown noise type.')

    # save to CSV
    cleaning_path = os.path.join(data_cleaning_no_dirty_duplicates_dir, f'data_cleaning_{str(perc)}.csv')
    dirty_df.to_csv(cleaning_path, index=False)

    print(f"Data Cleaning {perc}% dataset was created.")