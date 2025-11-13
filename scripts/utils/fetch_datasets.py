import os
import re

from experiments.model.dataset import Dataset


def get_dirtiness_from_filename(filename):
  match = re.search(r'[a-z_]+(\d+)', filename)
  if match:
    return match.group(1)
  else:
    raise ValueError("There is no percentage in: " + filename)

def load_dirty_datasets(directory):
  """
  Loads all CSV files starting with "df_dirty_" into a list of DataFrames.

  Args:
    directory: The directory containing the CSV files.

  Returns:
    A list of DataFrames, each representing a loaded CSV file.
  """

  dirty_datasets = []
  for filename in os.listdir(directory):
    if filename.endswith(".csv"):
      filepath = os.path.join(directory, filename) #costruisce il percorso completo al file CSV combinando la directory directory con il nome del file filename.
      percentage = get_dirtiness_from_filename(filename)
      dataset = Dataset(
          dataset_id=os.path.splitext(filename)[0],
          content_string=read_csv_as_string(filepath),
          dirty_percentage=percentage
      )
      dirty_datasets.append(dataset)
  return dirty_datasets

def read_csv_as_string(filepath):
  # Legge il file CSV come stringa pura
  with open(filepath, "r", encoding="utf-8") as f:
    return f.read()