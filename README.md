# Exploring LLMs for Tabular Data Preparation

This repository contains materials related to our research thesis project at Politecnico di Milano.

## 📂 Folder Structure

- **`checklists`**: Provides an English version of the blueprint spreadsheets used for evaluating LLM outputs.
- **`data`**: Includes hard-coded Python files containing information on the LLMs utilized, examined tasks, checklists, and additional relevant details.
- **`datasets`**: Contains multiple CSV files:
  - **`datasets/dirty`**: Stores CSV versions of dirty datasets that were prompted to LLMs.
  - **`datasets/help`**: Includes supplementary data used at specific points during the experiments (these files are likely not relevant for most users).
  - **Root `datasets` folder**: Contains `df_clean.csv`, the clean dataset from which all dirty datasets originate.
- **`evaluations`**: Consists of spreadsheets manually filled to assess LLM-generated outputs, categorized by task and dataset dirtiness. Each LLM folder contains an Excel checklist and the evaluated output in a `.txt` file.
- **`experiments`**: Features a prototype of an automated LLM output evaluation pipeline. Although ultimately discarded, the reasons behind this decision are documented in our thesis. We hope future researchers can refine and implement this approach. 🚀
- **`markdowns`**: Contains the markdown versions of the collected LLM outputs.
- **`pdfs`**: Provides the PDF versions of the markdown LLM outputs.
- **`responses`**: Stores LLM-generated outputs in `.txt` format.
- **`scripts`**: Houses various Python scripts for dataset selection, preparation, and generation of multiple dirty dataset versions. The script names are self-explanatory regarding their respective purposes. 🛠️
- **`user_study_results`**: Contains a PDF detailing the results of a User Study conducted and extensively discussed in our thesis.

## 👥 Authors

- [__Matteo Spreafico__](https://github.com/MattBlue00)
- [__Ludovica Tassini__](https://github.com/LudoTassini)

## 📜 Abstract

The increasing adoption of Large Language Models (LLMs) has transformed Artificial Intelligence (AI), demonstrating strong abilities in language understanding, problem-solving, and automation. However, their potential application in structured data environments, particularly in Tabular Data Preparation, remains underexplored. Data Preparation—including Data Profiling, Cleaning, and Transformation—is crucial but often labor-intensive in data-driven workflows. This thesis examines whether LLMs can support users in automating these tasks and compares their utility to traditional Data Preparation tools.

To this end, we conduct a systematic evaluation of both general-purpose LLMs (GPT-4, Claude, Gemini, Llama) and fine-tuned tabular LLMs (TableGPT2, TableLLM). Our experimental framework evaluates their performance on structured datasets with varying complexity and noise, assessing their ability to handle tasks such as Data Profiling and Cleaning. To ensure rigorous evaluation, we propose a novel methodology based on a custom Quality Model (QM), which leverages structured checklists and quantitative metrics to assess key Data Quality dimensions. This assessment enables the evaluation of LLM output quality. The model includes well-established dimensions like Completeness and Accuracy, along with new ones such as Prescriptivity, Readiness, and Specificity. A user study further validates our framework and explores practitioners’ expectations for LLM-assisted Data Preparation.

Results show notable differences between general-purpose and tabular LLMs, revealing their respective strengths and limitations. While LLMs offer potential for automating aspects of Data Preparation, their effectiveness depends on the task and dataset.

By examining LLM support in diverse Tabular Data Preparation tasks, this thesis contributes to AI-assisted data management research. Our findings provide a foundation for future research on evaluating and improving LLMs’ handling of tabular data and offer guidance for professionals seeking innovative ways to streamline Data Preparation.

## 📑 Executive Summary

Currently under review (expected publication: **April 2025**).

## 📖 Thesis

Currently under review (expected publication: **April 2025**).
