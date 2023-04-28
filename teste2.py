import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import PySimpleGUI as sg


class RenameHandler(FileSystemEventHandler):
    def __init__(self, new_name, image_dir):
        self.new_name = new_name
        self.image_dir = image_dir

    def on_created(self, event):
        images = os.listdir(self.image_dir)
        images.sort(key=lambda x: os.stat(
            os.path.join(self.image_dir, x)).st_ctime)

        def take_last_img(item):
            last_dash = item.rfind('-')
            current_name = item[:last_dash]
            image_count = int(item[last_dash+1:].split('.')[0])+1
            last_img_extension = images[-1].split('.')[-1]
            new_name = f'{current_name}-{str(image_count)}.{last_img_extension}'

            while True:
                try:
                    os.rename(os.path.join(
                        self.image_dir, images[-1]), os.path.join(self.image_dir, new_name))
                    break
                except:
                    time.sleep(.3)
                    continue

        if len(images) >= 2:
            if self.new_name:
                n = 0
                for i, image in enumerate(images):
                    img_extension = os.path.splitext(image)[1]
                    new_name = f'{self.new_name}-{str(i + 1).zfill(2)}{img_extension}'
                    n += 1
                    os.rename(os.path.join(self.image_dir, image),
                              os.path.join(self.image_dir, new_name))
            else:
                take_last_img(images[-2])
        else:
            return


def main():
    sg.theme('DarkBlue3')
    font = ('Arial', 12)

    layout = [
        [sg.Text('Quantas pastas você deseja monitorar?',
                 font=font, justification='left')],
        [sg.Combo(['1', '2', '3', '4', '5'], key='folders_to_watch',
                  enable_events=True, font=font)],
        [sg.Button('Sair', font=font, button_color=('white', 'firebrick3'))]
    ]

    window = sg.Window('Monitor de Pastas', layout,
                       element_justification='c', margins=(20, 20))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        elif event == 'folders_to_watch':
            folder_count = int(values['folders_to_watch'])
            folder_inputs = []
            for i in range(folder_count):
                folder_inputs.append([sg.Text(f'Pasta {i+1}: ', font=font), sg.Input(
                    key=f'folder_{i}', font=font), sg.FolderBrowse(font=font)])
                folder_inputs.append([sg.Text(
                    f'Prefixo de nome da imagem para pasta {i+1}: ', font=font), sg.Input(key=f'prefix_{i}', font=font)])
                folder_inputs.append([sg.Checkbox(
                    'Aplicar padrão de nomenclatura padrão para todas as imagens na pasta?', default=True, key=f'rename_{i}', font=font)])
                folder_inputs.append([sg.Text('Padrão de nomenclatura:', font=font, key=f'label_default_{i}', visible=True),
                                      sg.Input(key=f'default_name_{i}', visible=True, font=font)])
                folder_inputs.append([sg.HorizontalSeparator()])
            folder_inputs.append(
                [sg.Button('Iniciar', font=font, button_color=('white', 'forestgreen'))])

            new_layout = [
                [sg.Column(folder_inputs, scrollable=True,
                           vertical_scroll_only=True)]
            ]

            new_window = sg.Window(
                'Monitor de Pastas', new_layout, element_justification='c', margins=(20, 20))
            window.close()
            window = new_window

        if event.startswith('rename'):
            selected_checkbox = event.split("_")[1]
            window[f'default_name_{selected_checkbox}'].update(
                visible=values[event])
            window[f'label_default_{selected_checkbox}'].update(
                visible=values[event])

        if event == 'Iniciar':
            folder_count = int(values['folders_to_watch'])
            for i in range(folder_count):
                folder_path = values[f'folder_{i}']
                default_name = values[f'default_name_{i}'] if values[f'rename_{i}'] else None

                if folder_path:
                    event_handler = RenameHandler(default_name, folder_path)
                    observer = Observer()
                    observer.schedule(
                        event_handler, folder_path, recursive=True)
                    observer.start()

            running_layout = [
                [sg.Text('Aplicativo em execução...',
                         font=font, pad=((0, 0), (20, 20)))],
                [sg.Text('Clique no botão abaixo para reiniciar ou no "X" para fechar.',
                         font=font, pad=((0, 0), (20, 0)))],
                [sg.Button('Reiniciar', font=font,
                           button_color=('white', 'darkorange'))]
            ]
            running_window = sg.Window(
                'Em execução', running_layout, element_justification='c', margins=(20, 20))


if __name__ == '__main__':
    main()
