import pygame as pg
from PIL import Image
import numpy as np
import random
import sys

sys.setrecursionlimit(1000000000)
sys.set_int_max_str_digits(1000000000)

def base_converter(num, new_base):
    a = num // new_base
    b = num % new_base
    if a >= new_base:
        a = base_converter(a, new_base)
    return [a, b]


def flatten(messy_array):
    new = messy_array.replace('[', '')
    new = new.replace(']', '')
    new = '[' + new + ']'
    return eval(new)


def index_to_image(index, colour_type):
    if colour_type == 'b&w':
        # slicing removes '0b' from the front of the string
        index_base_2 = bin(index)[2:]
        zero_padding = '0' * (image_pixel_count - len(index_base_2))
        index_base_2 = zero_padding + index_base_2

        array = np.array(list(index_base_2), dtype=np.uint8)
        array = np.where(array < 0.5, 0, 255)
        array = np.tile(array, (3, 1)).T
    
    elif colour_type == 'grey':
        index_base_256 = flatten(str(base_converter(index, new_base=256)))
        zero_padding = [0] * (image_pixel_count - len(index_base_256))
        index_base_256 = zero_padding + index_base_256

        array = np.array(index_base_256, dtype=np.uint8)
        array = np.tile(array, (3, 1)).T
    
    elif colour_type == 'full':
        index_base_256 = flatten(str(base_converter(index, new_base=256)))
        zero_padding = [0] * (image_pixel_count * 3 - len(index_base_256))
        index_base_256 = zero_padding + index_base_256

        array = np.array(index_base_256, dtype=np.uint8)
    
    array = np.reshape(array, (image_width, image_height, 3))
    image = pg.surfarray.make_surface(array)

    return image


valid = False
while not valid:
    print('[1] black and white')
    print('[2] greyscale')
    print('[3] full colour')
    colour_type = input('Enter a number from above: ')

    if not colour_type in ['1', '2', '3']:
        print('That was not a valid option')

    elif colour_type == '1':
        colour_type = 'b&w'
        valid = True
    
    elif colour_type == '2':
        colour_type = 'grey'
        valid = True
    
    elif colour_type == '3':
        colour_type = 'full'
        valid = True

valid = False
while not valid:
    try:
        image_size = input('Enter the width/height of the image (will be square): ')
        
        if '.' in image_size:
            raise ValueError
        else:
            image_size = int(image_size)
        
        image_width = image_size
        image_height = image_size

        valid = True
    
    except ValueError:
        print('That was not a valid number')

try:
    image_pixel_count = image_width * image_height
    if colour_type == 'b&w':
        total_images = 2 ** image_pixel_count
    elif colour_type == 'grey':
        total_images = 256 ** image_pixel_count
    elif colour_type == 'full':
        total_images = 16777216 ** image_pixel_count

    print(f'Total possible images: {total_images:,}')
except ValueError:
    print('Total possible images too large to compute')

valid = False
while not valid:
    image_index = input('Enter an image location between 0 and the number above: ')
    try:
        if '.' in image_index:
            raise ValueError
        
        image_index = int(image_index)

        if image_index < 0 or image_index >= total_images:
            raise ValueError
        
        valid = True
    except ValueError:
        print('That was not a valid number. Enter a number between the range 0 and the total number of possible images')

pg.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
screen_width, screen_height = screen.get_size()
clock = pg.time.Clock()
font_size = 35
font = pg.font.SysFont('menlo', font_size)
text_width, text_height = font.size('a')
max_characters = screen_width // text_width

held_down = False
image = index_to_image(image_index, colour_type)
index_history = [image_index]
history_index = 0

viewing_index = False

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                held_down = True
            
            if event.key == pg.K_SLASH:
                viewing_index = not viewing_index
            
            if event.key == pg.K_COMMA:
                font_size -= 1
                font = pg.font.SysFont('menlo', font_size)
                text_width, text_height = font.size('a')
                max_characters = screen_width // text_width
            
            if event.key == pg.K_PERIOD:
                font_size += 1
                font = pg.font.SysFont('menlo', font_size)
                text_width, text_height = font.size('a')
                max_characters = screen_width // text_width
            
            if event.key == pg.K_LEFT:
                history_index -= 1
                if history_index < 0:
                    history_index = 0
            
            if event.key == pg.K_RIGHT:
                history_index += 1
                if history_index >= len(index_history):
                    history_index = len(index_history) - 1
        
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                held_down = False
    
    if held_down:
        index_history.append(random.randint(0, total_images))
        history_index = len(index_history) - 1
    
    image_index = index_history[history_index]
    image = index_to_image(image_index, colour_type)
    
    image = pg.transform.scale(image, (screen_width, screen_height))
    screen.blit(image, (0, 0))

    if viewing_index:
        for colour in [[0,0,0], [255,255,255]]:
            # add a newline character after every n characters. n is the max_characters allowed on one line
            image_index_str = '\n'.join([f'{image_index:,}'[i:i+max_characters] for i in range(0, len(f'{image_index:,}'), max_characters)])
            index_render = font.render(image_index_str, True, colour)
            index_render_rect = index_render.get_rect(midtop=(screen_width/2, 12))
            screen.blit(index_render, index_render_rect)
    
    clock.tick(5)
    pg.display.flip()