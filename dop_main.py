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
screen = pygame.display.set_mode(size)  # Создание окна
pygame.display.set_caption('Змейка')
snake_speed = 12
clock = pygame.time.Clock()
fps = 10


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
food_image = load_image('apple.png')
cell_image = load_image('grass.png')
# Изменение размера изображений до нужного размера
snake_head_u = pygame.transform.scale(snake_head_u, (cell_size, cell_size))
snake_head_d = pygame.transform.scale(snake_head_d, (cell_size, cell_size))
snake_head_r = pygame.transform.scale(snake_head_r, (cell_size, cell_size))
snake_head_l = pygame.transform.scale(snake_head_l, (cell_size, cell_size))
snake_body_image = pygame.transform.scale(snake_body_image, (cell_size, cell_size))
food_image = pygame.transform.scale(food_image, (cell_size, cell_size))
cell_image = pygame.transform.scale(cell_image, (cell_size, cell_size))
font_style = pygame.font.SysFont("bahnschrift", 25)  # Шрифт для отображения счета
score_font = pygame.font.SysFont("comicsansms", 35)  # Шрифт для отображения счета


def draw_grid():  # отрисовка поля травы
    for x in range(0, width, cell_size):
        for y in range(0, height, cell_size):
            screen.blit(cell_image, (x, y))


def our_snake(snake_block, snake_list, direction):  # рисование змейки
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
    value = score_font.render("Счет: " + str(score - 4), True, (0, 0, 0))
    screen.blit(value, [0, 0])


def message(msg, color):  # Вывод сообщений
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():  # стартовый экран (нужно сделать кнопки старт и выход )
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


food_count = 2
food_on_grid = 0
eaten = True
eaten2 = True
first_game = True

if __name__ == '__main__':
    def gameLoop():  # Основная функция игры
        global food_count, food_on_grid, eaten, eaten2
        start_screen()
        game_over = False
        game_close = False
        x1 = width // 2 // cell_size * cell_size  # Начальные координаты змейки (в центре экрана)
        y1 = height // 2 // cell_size * cell_size
        x1_change = cell_size  # Начальное изменение по X для движения вправо
        y1_change = 0
        direction = 'RIGHT'  # Начальное направление
        snake_List = []
        Length_of_snake = 5
        while not game_over:
            while game_close:
                fon = pygame.transform.scale(load_image('fon.jpg'), (600, 400))
                screen.blit(fon, (0, 0))
                message("Ты проиграл! ENTER - повтор, Q - выход", (255, 255, 0))
                your_score(Length_of_snake - 1)
                pygame.display.update()
                for event in pygame.event.get():  # проверка ан повтор игры или выход
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_RETURN:
                            food_on_grid = 0
                            eaten = True
                            eaten2 = True
                            game_over = True
                            game_close = False
                            gameLoop()
            for event in pygame.event.get():  # Проверка на выход
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:  # Проверка нажатия кнопок и направления
                    if event.key == pygame.K_LEFT and direction != 'RIGHT':
                        x1_change = -cell_size
                        y1_change = 0
                        direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        x1_change = cell_size
                        y1_change = 0
                        direction = 'RIGHT'
                    elif event.key == pygame.K_UP and direction != 'DOWN':
                        y1_change = -cell_size
                        x1_change = 0
                        direction = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        y1_change = cell_size
                        x1_change = 0
                        direction = 'DOWN'
            if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:  # Проверка на выход за рамки
                game_close = True
            x1 += x1_change  # Обновление координат головы змеи
            y1 += y1_change
            draw_grid()  # Рисуем поле
            if food_count == 1 and eaten:
                while food_count > food_on_grid:
                    foodx = round(random.randrange(0, width - cell_size) / cell_size) * cell_size
                    foody = round(random.randrange(0, height - cell_size) / cell_size) * cell_size
                    food_on_grid += 1
                    eaten = False
            if food_count == 2:
                while food_count > food_on_grid:
                    if eaten:
                        foodx = round(random.randrange(0, width - cell_size) / cell_size) * cell_size
                        foody = round(random.randrange(0, height - cell_size) / cell_size) * cell_size
                        food_on_grid += 1
                        eaten = False
                    if eaten2:
                        foodx2 = round(random.randrange(0, width - cell_size) / cell_size) * cell_size
                        foody2 = round(random.randrange(0, height - cell_size) / cell_size) * cell_size
                        food_on_grid += 1
                        eaten2 = False
            screen.blit(food_image, (foodx, foody))  # Рисуем еду
            if food_count == 2:
                screen.blit(food_image, (foodx2, foody2))  # Рисуем еду
            if x1 == foodx and y1 == foody:  # Проверка на поедание еды
                foodx = round(random.randrange(0, width - cell_size) / cell_size) * cell_size
                foody = round(random.randrange(0, height - cell_size) / cell_size) * cell_size
                Length_of_snake += 1
                food_on_grid -= 1
                eaten = True
            if x1 == foodx2 and y1 == foody2:  # Проверка на поедание еды
                foodx2 = round(random.randrange(0, width - cell_size) / cell_size) * cell_size
                foody2 = round(random.randrange(0, height - cell_size) / cell_size) * cell_size
                Length_of_snake += 1
                food_on_grid -= 1
                eaten2 = True
            # Обновление змейки
            snake_Head = [x1, y1]  # Обновляем координаты головы
            snake_List.insert(0, snake_Head)  # Добавляем голову в начало списка
            if len(snake_List) > Length_of_snake:  # Удаляем последний элемент хвост, если длина змеи больше необходимой
                del snake_List[-1]  # Удаляем последний элемент из конца списка
            for x in snake_List[1:]:  # Проверка на столкновение с телом змеи (без головы)
                if x == snake_Head:
                    game_close = True
            our_snake(cell_size, snake_List, direction)  # Передаем направление в функцию our_snake()
            your_score(Length_of_snake - 1)
            pygame.display.update()
            clock.tick(fps)


    gameLoop()
