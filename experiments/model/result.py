import pandas as pd


class Result:

    def __init__(self, dataset_id, task_name, prompt_id, llm_name, accuracy, acc_reason, completeness, compl_reason):
        self.llm_name = llm_name
        self.dataset_id = dataset_id
        self.task_name = task_name
        self.prompt_id = prompt_id
        self.llm_name = llm_name
        self.accuracy = accuracy
        self.acc_reason = acc_reason
        self.completeness = completeness
        self.compl_reason = compl_reason

    def _to_dict(self):
        return {
            'dataset_id': self.dataset_id,
            'task_name': self.task_name,
            'prompt_id': self.prompt_id,
            'llm_name': self.llm_name,
            'accuracy': self.accuracy,
            'acc_reason': self.acc_reason,
            'completeness': self.completeness,
            'compl_reason': self.compl_reason
        }

    def _to_df(self):
        return pd.DataFrame([self._to_dict()])

    def to_csv(self, file_path):
        self._to_df().to_csv(file_path, index=False)

class DataCleaningResult(Result):

    def __init__(self, dataset_id, task_name, prompt_id, llm_name, accuracy, acc_reason, completeness, compl_reason):
        super().__init__(dataset_id, task_name, prompt_id, llm_name, accuracy, acc_reason, completeness, compl_reason)

class DataProfilingResult(Result):

    def __init__(self, dataset_id, task_name, prompt_id, llm_name, accuracy, acc_reason, completeness, compl_reason):
        super().__init__(dataset_id, task_name, prompt_id, llm_name, accuracy, acc_reason, completeness, compl_reason)