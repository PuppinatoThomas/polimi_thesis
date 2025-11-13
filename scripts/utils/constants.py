# number of rows to sample from the dataset
ROWS_TO_SAMPLE = 100
# fixing seed for reproducibility
RANDOM_SEED = 42
# fixing seed for reproducibility AIRLINE DATASET
RANDOM_SEED_AIR = 31
# number of successful tries per each evaluation
NUM_SUCCESSFUL_TRIES = 3
# dirtiness percentages
PERCENTAGES = [10, 30, 50]

LLM_INPUT_COSTS = {
    "GPT": 0.0000025,
    "Gemini": 0.00000125,
    "Claude": 0.000003
}

LLM_OUTPUT_COSTS = {
    "GPT": 0.00001,
    "Gemini": 0.000005,
    "Claude": 0.000015
}