This repository contains materials related to mmy research thesis project at Politecnico di Milano.

- **`checklists`**: Provides an English version of the blueprint spreadsheets used for evaluating LLM outputs.
- **`data`**: Includes hard-coded Python files containing information on the LLMs utilized, examined tasks, checklists, and additional relevant details.
- **`datasets`**: Contains multiple CSV files:
  - **`datasets/dirty`**: Stores CSV versions of dirty datasets that were prompted to LLMs.
  - **`datasets/help`**: Includes supplementary data used at specific points during the experiments (these files are likely not relevant for most users).
  - **Root `datasets` folder**: Contains `df_clean.csv`, the clean dataset from which all dirty datasets originate.
- **`evaluations`**: Consists of spreadsheets manually filled to assess LLM-generated outputs, categorized by task. Each LLM folder contains the various checklists that evaluate the task, one for each type of prompt.
- **`experiments`**: Include some hard-coded Python files, including various tested prompts.
- **`responses`**: Stores LLM-generated outputs in `.txt` format.
- **`results`**: Stores tables of results.
- **`scripts`**: Houses various Python scripts for dataset selection, preparation, and generation of multiple dirty dataset versions. The script names are self-explanatory regarding their respective purposes.
