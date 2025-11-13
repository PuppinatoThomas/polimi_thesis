import random
from scripts.utils.constants import RANDOM_SEED

def generate_random_indices(df, percentage):
  random.seed(RANDOM_SEED)
  return random.sample(df.index.tolist(), int(percentage * len(df)))