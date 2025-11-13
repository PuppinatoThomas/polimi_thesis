from scripts.utils.setup import setup

setup()

import os
import pandas as pd
from scripts.utils.path import get_directory_from_root, get_directory_from_dir_name

evaluations_dir = get_directory_from_root(__file__, 'evaluations')  # responses directory

# if evaluations directory does not exist, create it
if not os.path.exists(evaluations_dir):
    raise Exception(
        "There is no 'evaluations' directory to work with. Consider running 'python -m scripts.evaluate_responses' before running this script.")

datasets = [d for d in os.listdir(evaluations_dir) if os.path.isdir(os.path.join(evaluations_dir, d))]
df_list = []

for dataset in datasets:

    dataset_dir = get_directory_from_dir_name(evaluations_dir, dataset)
    if not os.path.exists(dataset_dir):
        raise Exception(
            "There is no dataset directory to work with. Consider running 'python -m scripts.evaluate_responses' before running this script.")

    datasets_dir = get_directory_from_root(__file__, os.path.join("datasets", "dirty"))  # datasets directory
    if not os.path.exists(datasets_dir):
        raise Exception(
            "There is no 'datasets/dirty' directory to work with. Consider running 'python -m scripts.evaluate_responses' before running this script.")

    tasks = [t for t in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, t))]

    for task in tasks:

        task_dir = get_directory_from_dir_name(dataset_dir, task)
        if not os.path.exists(task_dir):
            raise Exception(
                "There is no task directory to work with. Consider running 'python -m scripts.evaluate_responses' before running this script.")

        prompts = [p for p in os.listdir(task_dir) if os.path.isdir(os.path.join(task_dir, p))]

        for prompt in prompts:

            prompt_dir = get_directory_from_dir_name(task_dir, prompt)
            if not os.path.exists(prompt_dir):
                raise Exception(
                    "There is no prompt directory to work with. Consider running 'python -m scripts.evaluate_responses' before running this script.")

            results_files = [r for r in os.listdir(prompt_dir) if os.path.isfile(os.path.join(prompt_dir, r))]

            for results_file in results_files:
                df_list.append(pd.read_csv(os.path.join(prompt_dir, results_file)))

df = pd.concat(df_list, ignore_index=True)

results_dir = get_directory_from_root(__file__, 'results')  # responses directory

# if results directory does not exist, create it
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

df.to_csv(os.path.join(results_dir, 'results.csv'), index=False)

print("Done!")