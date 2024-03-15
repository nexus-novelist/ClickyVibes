import os
import sys
import random
import threading

from pynput import mouse, keyboard
import pygame

if __name__ == '__main__':
    pygame.mixer.init()
    key_folder_path = sys.argv[1]
    key_volume = int(sys.argv[2])
    mouse_folder_path = sys.argv[3]
    mouse_volume = int(sys.argv[4])
    loaded_key_sounds = {}
    loaded_mouse_sounds = {}

    script_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(script_dir, 'logo.txt'), 'r') as logo:
        print(logo.read())

    for file in os.listdir(key_folder_path):
        if (file.endswith('.mp4') or file.endswith('.wav')) and not file.lower().startswith('full'):
            loaded_key_sounds.update({file: key_folder_path+'\\'+file})
    
    for file in os.listdir(mouse_folder_path):
        if (file.endswith('.mp4') or file.endswith('.wav')) and not file.lower().startswith('full'):
            loaded_mouse_sounds.update({file: mouse_folder_path+'\\'+file})

    def on_click(x, y, button, pressed):
        if pressed:
            if button == mouse.Button.left:
                button = 'left'
            elif button == mouse.Button.right:
                button = 'right'
            else:
                button = 'middle'
            if button+'.wav' in loaded_mouse_sounds:
                sound = pygame.mixer.Sound(loaded_mouse_sounds[button+'.wav'])
                sound.play()
                sound.set_volume(mouse_volume/100)
            else:
                sound = pygame.mixer.Sound(random.choice(list(loaded_mouse_sounds.items()))[1])
                sound.play()
                sound.set_volume(mouse_volume/100)

    def on_type(key):
        if getattr(key, 'char', 'none') != 'none':
            if key.char.lower()+'.wav' in loaded_key_sounds:
                sound = pygame.mixer.Sound(loaded_key_sounds[key.char.lower()+'.wav'])
                sound.play()
                sound.set_volume(key_volume/100)
            else:
                sound = pygame.mixer.Sound(random.choice(list(loaded_key_sounds.items()))[1])
                sound.play()
                sound.set_volume(key_volume/100)
        else:
            sound = pygame.mixer.Sound(random.choice(list(loaded_key_sounds.items()))[1])
            sound.play()
            sound.set_volume(key_volume/100)
    
    def start_keyboard_listener():
        with keyboard.Listener(on_press=on_type) as listener:
            listener.join()
    
    def start_mouse_listener():
        with mouse.Listener(on_click=on_click) as listener:
            try:
                listener.join()
            except Exception as e:
                print('{0} was clicked'.format(e.args[0]))

    mouse_listener = threading.Thread(target=start_mouse_listener)
    keyboard_listener = threading.Thread(target=start_keyboard_listener)

    mouse_listener.start()
    keyboard_listener.start()

    mouse_listener.join()
    keyboard_listener.join()