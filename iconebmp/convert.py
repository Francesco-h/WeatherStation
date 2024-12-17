import os
from PIL import Image

def convert_images_in_folder(folder_path):
    # Estensioni di immagini supportate
    supported_extensions = (".png", ".jpg", ".jpeg", ".tiff",".gif")

    # Itera su tutti i file nella cartella
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_extensions):
            image_path = os.path.join(folder_path, filename)

            try:
                # Apri l'immagine e converti in monocromatico
                img = Image.open(image_path).convert("1")

                # Crea il nome del file con estensione .bmp
                new_filename = os.path.splitext(filename)[0] + ".bmp"
                new_image_path = os.path.join(folder_path, new_filename)

                # Salva l'immagine convertita in formato BMP
                img.save(new_image_path)
                print(f"Convertito: {filename} -> {new_filename}")

            except Exception as e:
                print(f"Errore durante la conversione di {filename}: {e}")

if __name__ == "__main__":
    folder_path = "./"  # Cambia con il percorso della tua cartella
    convert_images_in_folder(folder_path)

