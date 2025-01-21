import os
import sys
from asyncio import Event
import pygame
import random


pygame.init()
# Настройки экрана
CELL_SIZE = 30  # Размер одной клетки в пикселях
GRID_SIZE = 30  # Размер поля
WIDTH, HEIGHT = CELL_SIZE * GRID_SIZE, CELL_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Змейка')
fps = 10
clock = pygame.time.Clock()

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


eaten = 1
length = 0


class Player(pygame.sprite.Sprite):  #создание змейки
    def __init__(self):
        super().__init__()
        self.head_image = load_image('snake_d.png')  # Начальное изображение
        self.tail_image = load_image('tail.png')
        self.head_rect = self.head_image.get_rect()
        self.tail_rect = self.tail_image.get_rect()
        self.head_rect.x = CELL_SIZE * 1  # Начальная позиция X
        self.head_rect.y = CELL_SIZE * 1  # Начальная позиция Y
        self.direction = (0, 1)  # Начальное направление (вниз)
        self.x = 0
        self.y = 0

    def update(self):  # Обновление позиции игрока в зависимости от направления
        global length
        if length == eaten or length == 0:
            self.x = self.head_rect.x
            self.y = self.head_rect.y
        elif length < eaten:
            pass
        self.head_rect.x += self.direction[0] * CELL_SIZE
        self.head_rect.y += self.direction[1] * CELL_SIZE
        self.tail_rect.x = self.x
        self.tail_rect.y = self.y
        if eaten > length:
            pass

    def turn(self, new_direction):  # Запрет поворота на 180 градусов
        if (self.direction[0] == -new_direction[0] and self.direction[1] == -new_direction[1]):
            self.rotate180 = True
            return
        self.rotate180 = False
        self.direction = new_direction


class Food(pygame.sprite.Sprite):  # Класс еды
    def __init__(self):
        super().__init__()
        self.image = load_image('apple.png', 1).convert_alpha()  # Изображение еды (convert_alpha должен
        self.image = pygame.transform.scale(self.image, (30, 30))              ## убирать белый фон, но не убирает)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        # Генерация случайной позиции для еды
        self.rect.x = random.randint(0, GRID_SIZE - 1) * CELL_SIZE
        self.rect.y = random.randint(0, GRID_SIZE - 1) * CELL_SIZE


def show_game_over():  # Функция для отображения сообщения о поражении
    font = pygame.font.SysFont(None, 55)
    text = font.render('Game Over', True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Ждем 2 секунды перед выходом

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (900, 900))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    start_screen()
    player = Player()  # Создаем игрока
    food = Food()  # Создаем еду
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.turn((0, -1))  # Поворот вверх
                    if not player.rotate180:  # условие на поворот назад
                        player.head_image = load_image('snake_u.png')
                elif event.key == pygame.K_DOWN:
                    player.turn((0, 1))  # Поворот вниз
                    if not player.rotate180:  # условие на поворот назад
                        player.head_image = load_image('snake_d.png')
                elif event.key == pygame.K_LEFT:
                    player.turn((-1, 0))  # Поворот влево
                    if not player.rotate180:  # условие на поворот назад
                        player.head_image = load_image('snake_l.png')
                elif event.key == pygame.K_RIGHT:
                    player.turn((1, 0))  # Поворот вправо
                    if not player.rotate180:  # условие на поворот назад
                        player.head_image = load_image('snake_r.png')
        player.update()  # Обновление позиции игрока
        if (player.head_rect.x < 0 or player.head_rect.x >= WIDTH or  # Проверка на столкновение с границами игрового поля
                player.head_rect.y < 0 or player.head_rect.y >= HEIGHT):
            show_game_over()
            running = False
        if player.head_rect.colliderect(food.rect):  # Проверка на столкновение с едой
            eaten += 1
            food.randomize_position()  # Перемещаем еду в новое место
        grass_image = load_image('grass.png', CELL_SIZE)  # Отрисовка фона из травы
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                screen.blit(grass_image, (col * CELL_SIZE, row * CELL_SIZE))
        screen.blit(player.head_image, player.head_rect)  # Отрисовка змеи
        screen.blit(player.tail_image, player.tail_rect)
        screen.blit(food.image, food.rect)  # Отрисовка еды
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    sys.exit()










