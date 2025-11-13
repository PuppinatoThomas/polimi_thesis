from scripts.utils.path import get_directory_from_root

import subprocess
import os

def markdown_to_pdf(source_dir: str, target_dir: str):
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, relative_path)

        os.makedirs(target_path, exist_ok=True)

        for file in files:
            if file.endswith(".md"):
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_path, file.replace(".md", ".pdf"))

                # Usa Pandoc per la conversione
                subprocess.run([
                    "pandoc", source_file, "-o", target_file,
                    #"--pdf-engine=xelatex",
                    "-V", "geometry:margin=0.5in"
                ])

                print(f"File {file} convertito in PDF: {target_file}")

# Directory sorgente e di destinazione
source_directory = get_directory_from_root(__file__, "markdowns")
target_directory = get_directory_from_root(__file__, "pdfs")

# Crea la cartella "pdfs", se non esiste
os.makedirs(target_directory, exist_ok=True)

# Esegui la conversione (specifica il path del font se necessario)
markdown_to_pdf(source_directory, target_directory)

print(f"Conversione completata! I documenti si trovano nella cartella '{target_directory}'.")