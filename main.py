import pygame as pg
from PIL import Image
import numpy as np

def random_image():
    if colour_type == 'b&w':
        array = np.random.randint(0, 2, size=image_width*image_height)
        array = np.where(array < 0.5, 0, 255)
        array = np.tile(array, (3, 1)).T

    elif colour_type == 'grey':
        array = np.random.randint(0, 255, size=image_width*image_height)
        array = np.tile(array, (3, 1)).T
    
    elif colour_type == 'full':
        array = np.random.randint(0, 255, size=image_width*image_height*3)

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

pg.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
screen_width, screen_height = screen.get_size()
clock = pg.time.Clock()

held_down = False
image = random_image()
image_history = [image]
image_index = 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                held_down = True
            
            if event.key == pg.K_LEFT:
                image_index -= 1
                if image_index < 0:
                    image_index = 0
            
            if event.key == pg.K_RIGHT:
                image_index += 1
                if image_index >= len(image_history):
                    image_index = len(image_history) - 1
        
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                held_down = False
    
    if held_down:
        image_history.append(random_image())
        image_index = len(image_history) - 1
    
    image = image_history[image_index]
    
    image = pg.transform.scale(image, (screen_width, screen_height))
    screen.blit(image, (0, 0))
    
    clock.tick(10)
    pg.display.flip()