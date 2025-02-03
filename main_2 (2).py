import os
import sys
import pygame
import random

# Инициализация Pygame
pygame.init()
# Настройки экрана
cell_size = 20  # Размер одной клетки в пикселях
width = 600
height = 400
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()
fps = 8

def load_image(name, colorkey=None):  # Загрузка изображений
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

snake_head_u = load_image('snake_u.png')  # Удобная загрузка изображений
snake_head_d = load_image('snake_d.png')
snake_head_r = load_image('snake_r.png')
snake_head_l = load_image('snake_l.png')
snake_body_image = load_image('tail.png')
snake_body_image2 = load_image('tail2.png')
food_image = load_image('apple.png')
cell_image = load_image('grass.png')
# Изменение размера изображений до нужного размера
snake_head_u = pygame.transform.scale(snake_head_u, (cell_size, cell_size))
snake_head_d = pygame.transform.scale(snake_head_d, (cell_size, cell_size))
snake_head_r = pygame.transform.scale(snake_head_r, (cell_size, cell_size))
snake_head_l = pygame.transform.scale(snake_head_l, (cell_size, cell_size))
snake_body_image = pygame.transform.scale(snake_body_image, (cell_size, cell_size))
snake_body_image2 = pygame.transform.scale(snake_body_image2, (cell_size, cell_size))
food_image = pygame.transform.scale(food_image, (cell_size, cell_size))
cell_image = pygame.transform.scale(cell_image, (cell_size, cell_size))
font_style = pygame.font.SysFont("bahnschrift", 25)  # Шрифт для отображения счета
score_font = pygame.font.SysFont("comicsansms", 35)  # Шрифт для отображения счета

def draw_grid():  # отрисовка поля травы
    for x in range(0, width, cell_size):
        for y in range(0, height, cell_size):
            screen.blit(cell_image, (x, y))

def our_snake(snake_body_image, snake_list, direction):  # рисование змейки
    head_image = {  # Отображение головы в зависимости от направления
        'UP': snake_head_u,
        'DOWN': snake_head_d,
        'RIGHT': snake_head_r,
        'LEFT': snake_head_l
    }[direction]
    for x in snake_list[1:]:  # Отображение тела
        screen.blit(snake_body_image, (x[0], x[1]))
    screen.blit(head_image, (snake_list[0][0], snake_list[0][1]))  # Отображение головы

def your_score(score):  # Вывод счёта
    value = score_font.render("Счет: " + str(score), True, (0, 0, 0))
    screen.blit(value, [0, 0])

def message(msg, color):  # Вывод сообщений
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():  # стартовый экран (нужно сделать кнопки старт и выход)
    fon = pygame.transform.scale(load_image('fon.jpg'), (600, 400))
    screen.blit(fon, (0, 0))
    message("                      Старт!", (255, 255, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    def gameLoop():  # Основная функция игры
        start_screen()  # Предполагается наличие функции start_screen()
        game_over = False
        game_close = False
        x1 = width // 2 // cell_size * cell_size  # змейка 1
        y1 = height // 2 // cell_size * cell_size
        x1_change = cell_size
        y1_change = 0
        direction1 = 'RIGHT'
        snake_List1 = []
        Length_of_snake1 = 1
        x2 = width // 4 // cell_size * cell_size  # змейка 2
        y2 = height // 4 // cell_size * cell_size
        x2_change = cell_size
        y2_change = 0
        direction2 = 'RIGHT'
        snake_List2 = []
        Length_of_snake2 = 1
        # Генерация еды в случайной позиции
        foodx = round(random.randrange(0, width - cell_size) / cell_size) * cell_size
        foody = round(random.randrange(0, height - cell_size) / cell_size) * cell_size
        while not game_over:
            while game_close:
                fon = pygame.transform.scale(load_image('fon.jpg'), (600, 400))  # Предполагается наличие функции load_image()
                screen.blit(fon, (0, 0))
                message("Ты проиграл! R - повтор, Q - выход", (255, 255, 0))
                your_score(max(Length_of_snake1 - 1, Length_of_snake2 - 1))  # максимальный счёт
                pygame.display.update()
                for event in pygame.event.get():  # проверка ан повтор игры или выход
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_r:
                            game_over = True
                            game_close = False
                            gameLoop()
            for event in pygame.event.get():  # Проверка на выход
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:  # Управление первой змейкой
                    if event.key == pygame.K_LEFT and direction1 != 'RIGHT':
                        x1_change = -cell_size
                        y1_change = 0
                        direction1 = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction1 != 'LEFT':
                        x1_change = cell_size
                        y1_change = 0
                        direction1 = 'RIGHT'
                    elif event.key == pygame.K_UP and direction1 != 'DOWN':
                        y1_change = -cell_size
                        x1_change = 0
                        direction1 = 'UP'
                    elif event.key == pygame.K_DOWN and direction1 != 'UP':
                        y1_change = cell_size
                        x1_change = 0
                        direction1 = 'DOWN'
                    if event.key == pygame.K_a and direction2 != 'RIGHT':  # Управление второй змейкой
                        x2_change = -cell_size
                        y2_change = 0
                        direction2 = 'LEFT'
                    elif event.key == pygame.K_d and direction2 != 'LEFT':
                        x2_change = cell_size
                        y2_change = 0
                        direction2 = 'RIGHT'
                    elif event.key == pygame.K_w and direction2 != 'DOWN':
                        y2_change = -cell_size
                        x2_change = 0
                        direction2 = 'UP'
                    elif event.key == pygame.K_s and direction2 != 'UP':
                        y2_change = cell_size
                        x2_change = 0
                        direction2 = 'DOWN'
            if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:  # Проверка на выход за рамки для змейки 1
                game_close = True
            x1 += x1_change  # Обновление координат головы змейки 1
            y1 += y1_change
            if x2 >= width or x2 < 0 or y2 >= height or y2 < 0:  # Проверка на выход за рамки для змейки 2
                game_close = True
            x2 += x2_change  # Обновление координат головы змейки 2
            y2 += y2_change
            draw_grid()  # Рисуем поле
            screen.blit(food_image, (foodx, foody))  # Рисуем еду
            if x1 == foodx and y1 == foody:  # Проверка на поедание еды первой змейкой
                foodx = round(random.randrange(0, width - cell_size) / cell_size) * cell_size
                foody = round(random.randrange(0, height - cell_size) / cell_size) * cell_size
                Length_of_snake1 += 1
            if x2 == foodx and y2 == foody:  # Проверка на поедание еды второй змейкой
                foodx = round(random.randrange(0, width - cell_size) / cell_size) * cell_size
                foody = round(random.randrange(0, height - cell_size) / cell_size) * cell_size
                Length_of_snake2 += 1
            # Обновление змейки 1
            snake_Head1 = [x1, y1]  # Обновляем координаты головы
            snake_List1.insert(0, snake_Head1)  # Добавляем голову в начало списка
            if len(snake_List1) > Length_of_snake1:  # Удаляем последний хвост, если длина змеи больше необходимой
                del snake_List1[-1]  # Удаляем последний элемент из конца списка
            for x in snake_List1[1:]:  # Проверка на столкновение с телом змеи (без головы)
                if x == snake_Head1:
                    game_close = True
            our_snake(snake_body_image, snake_List1, direction1)
            # Обновление змейки 2
            snake_Head2 = [x2, y2]  # Обновляем координаты головы
            snake_List2.insert(0, snake_Head2)  # Добавляем голову в начало списка
            if len(snake_List2) > Length_of_snake2:  # Удаляем последний хвост, если длина змеи больше необходимой
                del snake_List2[-1]  # Удаляем последний элемент из конца списка
            for x in snake_List2[1:]:  # Проверка на столкновение с телом змеи (без головы)
                if x == snake_Head2:
                    game_close = True
            our_snake(snake_body_image2, snake_List2, direction2)
            your_score(max(Length_of_snake1 - 1, Length_of_snake2 - 1)) # Вызов функции счета
            pygame.display.update()
            clock.tick(fps)

if __name__ == '__main__':
    gameLoop()
