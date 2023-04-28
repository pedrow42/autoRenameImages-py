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
            image_count = item[last_dash+1:].split('.')[0]
            if image_count.isdigit():
                image_count = int(image_count)+1
            else:
                return

            last_img_extension = images[-1].split('.')[-1]
            new_name = f'{current_name}-{str(image_count).zfill(2)}.{last_img_extension}'

            while True:
                try:
                    os.rename(os.path.join(
                        self.image_dir, images[-1]), os.path.join(self.image_dir, new_name))
                    break
                except:
                    break

        if len(images) >= 2:
            if self.new_name:
                time.sleep(.5)
                for i in range(len(images)):
                    img_extension = images[i].split('.')[-1]
                    new_name = f'{self.new_name}-{str(i + 1).zfill(2)}.{img_extension}'
                    while True:
                        try:
                            os.rename(os.path.join(self.image_dir, images[i]),
                                      os.path.join(self.image_dir, new_name))
                            break
                        except:
                            break

            else:
                time.sleep(.3)
                take_last_img(images[-2])
        else:
            return


def main():
    sg.theme('DarkBlue3')
    font = ('Helvetica', 12)

    layout = [
        [sg.Text('Quantas pastas você deseja monitorar?',
                 font=font, justification='left'),
         sg.Combo(['1', '2', '3', '4', '5'], key='folders_to_watch', enable_events=True, font=font)]
    ]

    window = sg.Window('Renomeador de Imagens', layout,
                       element_justification='c', margins=(80, 40))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'folders_to_watch':
            new_layout = [
                [sg.Text('Quantas pastas você deseja monitorar?',
                 font=font, justification='left'),
                 sg.Combo(['1', '2', '3', '4', '5'], key='folders_to_watch', default_value=values['folders_to_watch'], enable_events=True, font=font)]
            ]
            for i in range(int(values['folders_to_watch'])):
                new_layout.append(
                    [
                        [sg.Text(
                            f'Digite o caminho da {i+1}ª pasta selecionada: ', justification='left', font=font, pad=((0, 0), (20, 0))), sg.Input(key=f'image_dir{i}', pad=((0, 0), (20, 0)), font=font, size=(40, 1))],
                        [sg.Text('Aplicar único padrão de nomenclatura para todas as imagens na pasta?', font=font, justification='left'),
                         sg.Radio('Sim', f'rename{i}', key=f'sim-{i}', enable_events=True, font=font), sg.Radio('Não', f'rename{i}', key=f'nao-{i}', default=True, enable_events=True, font=font)],
                        [sg.Text('Digite o padrão de nomenclatura das imagens: ', font=font, key=f'label_default{i}', justification='left',
                                 visible=False), sg.Input(key=f'default_name{i}', visible=False)]
                    ]
                )
            new_layout.append([
                [sg.Button('Iniciar', font=('Helvetica', 14),
                           button_color=('black', 'yellow'), size=(16, 2), pad=((0, 0), (20, 0)))]
            ])

            new_window = sg.Window(
                'Renomeador de Imagens', new_layout, margins=(80, 40))
            window.close()
            window = new_window

        if event.startswith('sim'):
            selected_radio = event.split("-")[1]
            window[f'label_default{selected_radio}'].update(visible=True)
            window[f'default_name{selected_radio}'].update(visible=True)
        elif event.startswith('nao'):
            selected_radio = event.split("-")[1]
            window[f'label_default{selected_radio}'].update(visible=False)
            window[f'default_name{selected_radio}'].update(visible=False)

        if event == 'Iniciar':
            for i in range(int(values['folders_to_watch'])):
                folder_path = values[f'image_dir{i}']
                default_name = values[f'default_name{i}']

                if folder_path:
                    event_handler = RenameHandler(default_name, folder_path)
                    observer = Observer()
                    observer.schedule(
                        event_handler, folder_path, recursive=True)
                    observer.start()
                    if default_name:
                        event_handler.on_created(None)

            running_layout = [
                [sg.Text('Aplicativo em execução...',
                         font=('Helvetica', 18), pad=((0, 0), (20, 20)))],
                [sg.Text('Clique no botão abaixo para reiniciar ou no "x" para encerrar.', font=font, pad=(
                    (0, 0), (20, 20)))],
                [[sg.Button('Reiniciar', size=(16, 2), font=(
                    'Helvetica', 14))]]
            ]
            running_window = sg.Window(
                'Renomeador de Imagens', running_layout, margins=(80, 40), element_justification='c')
            window.close()
            window = running_window

        if event == 'Reiniciar':
            observer.stop()
            layout = [
                [sg.Text('Quantas pastas você deseja monitorar?',
                         font=font, justification='left'),
                 sg.Combo(['1', '2', '3', '4', '5'], key='folders_to_watch', enable_events=True, font=font)]
            ]
            window.close()
            window = sg.Window('Renomeador de Imagens',
                               layout, margins=(80, 40))


if __name__ == '__main__':
    main()
