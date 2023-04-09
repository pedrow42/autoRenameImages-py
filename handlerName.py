import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class RenameHandler(FileSystemEventHandler):

    def __init__(self, new_name, image_dir):
        self.new_name = new_name
        self.image_dir = image_dir

    def on_created(self, event):
        images = os.listdir(self.image_dir)

        images.sort(key=lambda x: os.stat(os.path.join(self.image_dir, x)).st_ctime)
        last_img_name, last_img_extension = os.path.splitext(images[-1])

        def take_last_img(item):
            img_name, img_extension = os.path.splitext(item)
            new_image = item.replace(img_extension, "")
            
            pos = new_image.rfind('-')
            part1 = ''
            part2 = ''
            if pos != -1:
                part1, part2 = new_image[:pos], new_image[pos+1:]
                part1 = part1.strip()
                part2 = part2.strip()
            
            new_name = f'{part1}-{str(int(part2) + 1).zfill(2)}{last_img_extension}'
            os.rename(os.path.join(self.image_dir, images[-1]), os.path.join(self.image_dir, new_name))

        if len(images) >= 2:
            if self.new_name:
                n=0
                for i, image in enumerate(images):
                    img_name, img_extension = os.path.splitext(image)
                    new_name = f'{self.new_name}-{str(i + 1).zfill(2)}{img_extension}'
                    n+=1
                    os.rename(os.path.join(self.image_dir, image), os.path.join(self.image_dir, new_name))
                event_handler = RenameHandler(self.new_name, self.image_dir)
                observer = Observer()
                observer.schedule(event_handler, self.image_dir, recursive=True)
                observer.start()
            else:
                time.sleep(.5) 
                take_last_img(images[-2])
        else:
            return
            

def main():
    folders_to_watch = None
    while not isinstance(folders_to_watch, int) or folders_to_watch <= 0:
        folders_to_watch = input('Quantas pastas você deseja monitorar? (Digite um número): ')
        try:
            folders_to_watch = int(folders_to_watch)
            if folders_to_watch <= 0:
                print('Digite um número maior que zero!')
        except:
            print('Digite um número válido!')

    c = 0
    while c < int(folders_to_watch):
        c+=1
        image_dir = input('Digite o caminho da pasta selecionada: ')
        question = input('Você deseja que todas as imagens da pasta sejam renomeadas seguindo um mesmo padrão? (S/N): ')
        new_name = ''
        if question.lower() == 's':
            new_name = input('Digite o padrão de nomes que as imagens devem ter (Exemplo: sco-01-pht): ')
            event_handler = RenameHandler(new_name, image_dir)
            event_handler.on_created(None)
        else:
            event_handler = RenameHandler(new_name, image_dir)
            observer = Observer()
            observer.schedule(event_handler, image_dir, recursive=True)
            observer.start()

    while True:
        reload = input('Digite "r" para reiniciar o programa ou "e" para encerrá-lo: ')
        if reload.lower() == 'r':
            new_name = ''
            observer.stop()
            main()
        else:
            exit()


if __name__ == '__main__':
    main()
