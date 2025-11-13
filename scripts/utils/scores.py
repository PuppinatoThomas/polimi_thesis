import pprint
from typing import Dict, List

from typing import List, Dict


def get_mean_and_variance(scores_dict_list: List[Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    mean_dict: Dict[str, float] = {}
    variance_dict: Dict[str, float] = {}

    # mean
    for scores_dict in scores_dict_list:
        for key in scores_dict.keys():
            mean_dict[key] = mean_dict.get(key, 0) + scores_dict[key]

    for key in mean_dict.keys():
        mean_dict[key] = mean_dict[key] / len(scores_dict_list)

    # variance
    for scores_dict in scores_dict_list:
        for key in scores_dict.keys():
            variance_dict[key] = variance_dict.get(key, 0) + (scores_dict[key] - mean_dict[key]) ** 2

    for key in variance_dict.keys():
        variance_dict[key] = variance_dict[key] / len(scores_dict_list)

    result_dict = {key: {'Mean': mean_dict[key], 'Variance': variance_dict[key]} for key in mean_dict.keys()}
    return result_dict

def print_sorted_scores(scores) -> None:
    _sort_file_names(scores)
    pprint.pprint(scores)

def _sort_file_names(scores):
    for dataset_dict in scores.values():
        for task_dict in dataset_dict.values():
            for prompt_dict, response_dict in task_dict.items():
                sorted_files = dict(sorted(response_dict.items(), key=lambda item: item[0].lower()))
                task_dict[prompt_dict] = sorted_files