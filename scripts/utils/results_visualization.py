import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def get_results(experiments):
    df_results = pd.DataFrame(columns=['Dataset', 'Task Name', 'Prompt', 'LLM', 'Accuracy', 'Completeness', 'Consistency', 'Relevance', 'Fluency', 'Overall Score'])
    for experiment in experiments:
      llm_results = experiment.results
      for llm_result in llm_results:
        row = {
          'Dataset': llm_result.dataset_id,
          'Task Name': llm_result.task_name,
          'Prompt': llm_result.id,
          'LLM': llm_result.llm_name,
          'Accuracy': llm_result.accuracy,
          'Completeness': llm_result.completeness,
          'Consistency': llm_result.consistency,
          'Relevance': llm_result.relevance,
          'Fluency': llm_result.fluency,
          'Overall Score': llm_result.overall_score
        }
        df_results.loc[len(df_results)] = row

    return df_results

def plot_results(df_results):

  # @title LLM vs Accuracy
  figsize = (12, 1.2 * len(df_results['LLM'].unique()))
  plt.figure(figsize=figsize)
  sns.violinplot(df_results, x='Accuracy', y='LLM', inner='stick', palette='Dark2', hue='LLM', legend=False)
  sns.despine(top=True, right=True, bottom=True, left=True)

  # @title Prompt vs Accuracy
  figsize = (12, 1.2 * len(df_results['Prompt'].unique()))
  plt.figure(figsize=figsize)
  sns.violinplot(df_results, x='Accuracy', y='Prompt', inner='stick', palette='Dark2', hue='Prompt', legend=False)
  sns.despine(top=True, right=True, bottom=True, left=True)

  # @title Accuracy vs Completeness
  df_results.plot(kind='scatter', x='Accuracy', y='Completeness', s=32, alpha=.8)
  plt.gca().spines[['top', 'right', ]].set_visible(False)