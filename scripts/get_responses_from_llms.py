
from experiments.model.dataset import Dataset
from experiments.model.prompt import QuestionPrompt
from scripts.utils.setup import setup

setup()#setup(dotenv=True)

import os


from data.llms import llms
from data.tasks import tasks
from scripts.utils.fetch_datasets import load_dirty_datasets, read_csv_as_string
from scripts.utils.path import get_directory_from_root, get_directory_from_dir_name

# Load the datasets
datasets_dir = get_directory_from_root(__file__, os.path.join("datasets", "dirty"))  # datasets directory

responses_dir = get_directory_from_root(__file__, 'responses')  # responses directory
# if responses directory does not exist, create it
if not os.path.exists(responses_dir):
    os.makedirs(responses_dir)

for task in tasks:

    print("Starting task " + task.name)

    task_dir = os.path.join(datasets_dir, task.name)
    if not os.path.exists(task_dir):
        os.makedirs(task_dir)

    if task.name == "dependency_discovery" :
        datasets = [
            Dataset(
               "dependency_discovery_dataset",
                content_string=read_csv_as_string(
                    #os.path.join(get_directory_from_root(__file__, "datasets"), "df_clean.csv")),
                    os.path.join(str(task_dir), "dependency_discovery.csv")),
                dirty_percentage=0
            )
        ]

    elif task.name == "data_wrangling" :
        datasets = [
            Dataset(
                "data_wrangling_dataset",
                content_string=read_csv_as_string(
                    os.path.join(str(task_dir), "data_wrangling.csv")),
                dirty_percentage=0
            )
        ]

    else: datasets = load_dirty_datasets(task_dir)

    task_dir = os.path.join(responses_dir, task.name)


    for dataset in datasets:

        print("Starting dataset " + str(dataset.id))

        dataset_dir = get_directory_from_dir_name(task_dir, dataset.id)
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        for prompt in task.prompts:

            if prompt.id !=20: # FIXME select the specific prompt
                continue
            if task.name!= "dependency_discovery":
                continue
            #if dataset.dirty_percentage != "50":
            #    continue

            print("Starting prompt " + str(prompt.id))

            prompt_dir = get_directory_from_dir_name(dataset_dir, str(prompt.id))
            if not os.path.exists(prompt_dir):
                os.makedirs(prompt_dir)

            prompt_copy = prompt.copy()
            prompt_copy.user_message = prompt_copy.user_message.replace("{{csv_text}}", dataset.content_string)
            print(prompt_copy.user_message)
          ###  with concurrent.futures.ThreadPoolExecutor() as executor:
           ##     futures = {}
            #
             #   print("Asking LLMs...")
             #   for llm in llms:
             #       futures[executor.submit(llm.get_response, prompt_copy)] = llm.name
             #
              #  responses = []
              #
              #  for future in concurrent.futures.as_completed(futures):
               #     llm_name = futures[future]
               #     try:
               #         response = future.result()
                #        responses.append((llm_name, response))
                #    except Exception as e:
                #        print(f"Error while asking {llm_name} for a response: {e}")

            responses = []
            print("Asking LLMs...")
            for llm in llms:
                llm_name = llm.name
                next_prompt_id = prompt.id
                if prompt.id == 9:
                    if dataset.dirty_percentage == 0:
                        answer_dir = get_directory_from_dir_name(responses_dir, get_directory_from_dir_name(task.name, get_directory_from_dir_name(task.name + '_dataset' , get_directory_from_dir_name(str(8), llm_name + '.txt'))))
                    else:
                        answer_dir = get_directory_from_dir_name(responses_dir, get_directory_from_dir_name(task.name, get_directory_from_dir_name(task.name + '_' + dataset.dirty_percentage, get_directory_from_dir_name(str(8), llm_name + '.txt')))) # 8 è l'id del prompt che ha fornito la knowledge
                    answer= read_csv_as_string(answer_dir)
                    prompt_copy.user_message = prompt_copy.user_message.replace("{{answer_text}}", answer)


                chat=llm.create_model(prompt_copy)

                try:
                    response = llm.get_response(chat, prompt_copy)
                    while True:
                        responses.append((llm_name, response))
                        print(response)

                        command= input("User:")

                        if command.strip().lower() != "exit":
                           # responses.append((llm_name, command))
                            next_prompt_id += 1
                            for p in task.prompts:
                                if p.id == next_prompt_id:
                                    print(p.user_message)
                                    responses.append((llm_name, p.user_message))
                                    response = llm.get_response(chat, QuestionPrompt(1, p.user_message))


                        else:
                            break

                except Exception as e:
                    print(f"Error while asking {llm_name} for a response: {e}")

            print("All LLMs answered")

            file_path = os.path.join(prompt_dir, f"{llm_name}.txt") # Create a clean filename
            with open(file_path, 'w', encoding="utf-8") as f:
                for llm_name, response in responses:
                    f.write(response +  '\n')

            print("Finished prompt " + str(prompt_copy.id))

        print("Finished dataset " + str(dataset.id))

    print("Finished task " + task.name)