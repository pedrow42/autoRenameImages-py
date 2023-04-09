import os
import keyboard
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RenameHandler(FileSystemEventHandler):

    def __init__(self, new_name, image_dir):
        self.new_name = new_name
        self.image_dir = image_dir

    def on_created(self, event):
        images = os.listdir(self.image_dir)

        images.sort(key=lambda x: os.stat(os.path.join(self.image_dir, x)).st_ctime)
        n = 0    
        for i, image in enumerate(images):
            new_name = f'{self.new_name}-{str(i + 1).zfill(2)}.jpg'
            print('len: '+str(len(images)))
            n+=1

            os.rename(os.path.join(self.image_dir, image), os.path.join(self.image_dir, new_name))
        print(n)

def main():
    image_dir = input('Digite o caminho da pasta selecionada: ')
    new_name = input('Digite o padrão de nomes que as imagens devem ter (Exemplo: sco-01-pht): ')
    event_handler = RenameHandler(new_name, image_dir)
    observer = Observer()
    observer.schedule(event_handler, image_dir, recursive=True)
    observer.start()

    def restart_observer():
        observer.stop()
        observer.join()
        main()

    print('Pressione "r" para reiniciar o programa')
    keyboard.add_hotkey('r', restart_observer)
    keyboard.wait()


if __name__ == '__main__':
    main()
