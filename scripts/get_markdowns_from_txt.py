import os

from scripts.utils.path import get_directory_from_root


def convert_txt_to_markdown(source_dir: str, target_dir: str):
    """
    Converte tutti i file .txt in una directory sorgente (inclusi quelli nelle sottocartelle)
    in file Markdown e li salva in una directory di destinazione mantenendo la struttura.
    """
    # Itera attraverso i file e le cartelle nella directory sorgente
    for root, dirs, files in os.walk(source_dir):
        # Determina il percorso relativo rispetto alla directory sorgente
        relative_path = os.path.relpath(root, source_dir)
        # Determina il percorso equivalente nella directory di destinazione
        target_path = os.path.join(target_dir, relative_path)

        # Crea la directory di destinazione se non esiste
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        for file in files:
            if file.endswith(".txt"):  # Processa solo i file .txt
                # Percorso completo del file sorgente
                source_file = os.path.join(root, file)
                # Percorso completo del file di destinazione con estensione .md
                target_file = os.path.join(target_path, file.replace(".txt", ".md"))

                # Leggi il contenuto del file sorgente
                with open(source_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Scrivi il contenuto convertito nel file di destinazione
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(content)


# Directory sorgente e di destinazione
source_directory = get_directory_from_root(__file__, "responses")
target_directory = get_directory_from_root(__file__, "markdowns")

# Crea la cartella "markdowns", se non esiste
os.makedirs(target_directory, exist_ok=True)

# Esegui la conversione
convert_txt_to_markdown(source_directory, target_directory)

print(f"Conversione completata! I file Markdown si trovano nella cartella '{target_directory}'.")