import os


def _get_project_root(current_file_name, project_name='polimi-thesis'):
    # Ottieni la directory corrente del file passato
    script_dir = os.path.dirname(os.path.abspath(current_file_name))

    # Continua a risalire fino a trovare la directory 'polimi-thesis'
    while os.path.basename(script_dir) != project_name:
        parent_dir = os.path.dirname(script_dir)  # Vai alla directory genitore
        if parent_dir == script_dir:
            # Se siamo tornati alla radice del filesystem senza trovare la cartella, esci
            raise FileNotFoundError(f"Directory '{project_name}' not found.")
        script_dir = parent_dir

    return script_dir

def get_directory_from_root(current_file_name, dir_name):
    return os.path.join(_get_project_root(current_file_name), dir_name)  # datasets directory

def get_directory_from_dir_name(current_directory, dir_name):
    return os.path.join(current_directory, dir_name)
