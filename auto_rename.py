import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class RenameHandler(FileSystemEventHandler):

    def __init__(self, new_name, image_dir):
        self.new_name = new_name
        self.image_dir = image_dir

    def on_created(self, event):
        print(self.new_name, self.image_dir)

        # Get a list of all the images in the directory
        images = os.listdir(self.image_dir)

        # Sort the list of images by creation time
        images.sort(key=lambda x: os.stat(os.path.join(self.image_dir, x)).st_ctime)

        # Iterate over the list of images and rename them
        for i, image in enumerate(images):
            image_name = os.path.basename(image)

            print(image_name)

            # Generate the new name for the image
            new_name = f'{self.new_name}-{str(i+1).zfill(2)}.jpg'

            # Rename the image
            os.rename(os.path.join(self.image_dir, image), os.path.join(self.image_dir, new_name))

def main():
    image_dir = input('Digite o caminho da pasta selecionada: ')
    new_name = input('Digite o padrão de nomes que as imagens devem ter (Exemplo: sco-01-pht): ')
    event_handler = RenameHandler(new_name, image_dir)
    observer = Observer()
    observer.schedule(event_handler, image_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

if __name__ == '__main__':
    main()
