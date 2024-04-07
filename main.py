import pygame
import sys
import random
import time
from pygame.locals import *
from pygame import mixer
import os

# Инициализация Pygame
pygame.init()

# Получаем путь к текущей директории
current_dir = os.path.dirname(__file__)

# музыка
pygame.mixer.init()
# Загрузка и воспроизведение музыкального файла из папки "music"
music_path = os.path.join(current_dir, 'musik', 'musik')
pygame.mixer.music.load(music_path)
pygame.mixer.music.play()

# Определение цветов
WHITE = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Настройки экрана
WIDTH, HEIGHT = 1024, 768
FPS = 60

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Вышинский жрёт бургеры под жоский фонк")

# Загрузка изображений
# Загрузка изображения фона
background_img = pygame.image.load(os.path.join(current_dir, "pictures", "fon.png"))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

basket_img = pygame.image.load(os.path.join(current_dir, "pictures", "basket.png"))

good_ball_img = pygame.image.load(os.path.join(current_dir, "pictures", "ball.png"))

bad_ball_img = pygame.image.load(os.path.join(current_dir, "pictures", "brokkoli.png"))

# Размеры и начальные координаты Вышинского
basket_width, basket_height = 100, 100
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 80

# Размеры и начальные координаты еды
ball_width, ball_height = 75, 75
ball_x = random.randint(0, WIDTH - ball_width)
ball_y = -ball_height

# Размеры и начальные координаты "плохих" шаров
bad_ball_width, bad_ball_height = 75, 75
bad_ball_x = random.randint(0, WIDTH - bad_ball_width)
bad_ball_y = -bad_ball_height

# Счет
score = 0
font = pygame.font.Font(None, 36)

# Основной игровой цикл
clock = pygame.time.Clock()

### ЛОГИЧЕСКИЙ БЛОК НЕ ТРОГАТЬ!!!

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Обработка управления корзиной
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= 8 + score/8
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += 8 + score/8

    # Скорость и направление движения шаров
    ball_speed = 5 + score/8
    bad_ball_speed = 5 + score/8

    # Обновление координат шаров
    ball_y += ball_speed
    bad_ball_y += bad_ball_speed

    # Проверка пойманного "хорошего" шара
    if (
        basket_x < ball_x + ball_width
        and basket_x + basket_width > ball_x
        and basket_y < ball_y + ball_height
        and basket_y + basket_height > ball_y
    ):
        score += 1
        ball_y = -ball_height
        ball_x = random.randint(0, WIDTH - ball_width)

    # Проверка пойманного "плохого" шара
    if (
        basket_x < bad_ball_x + bad_ball_width
        and basket_x + basket_width > bad_ball_x
        and basket_y < bad_ball_y + bad_ball_height
        and basket_y + basket_height > bad_ball_y
    ):
        score -= 1
        bad_ball_y = -bad_ball_height
        bad_ball_x = random.randint(0, WIDTH - bad_ball_width)

    # Проверка завершения игры
    if ball_y > HEIGHT:
        print("Игра окончена! Ваш счет:", score)
        time.sleep(0.1)

        # Экран окончания игры
        end_font = pygame.font.Font(None, 72)
        end_text = end_font.render("Игра окончена", True, RED)
        end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(end_text, end_rect)

        score_text = font.render("Ваш счет: " + str(score), True, RED)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(score_text, score_rect)

        pygame.display.flip()

        # Ожидание нажатия клавиши для выхода или перезапуска игры
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        # Нажатие Enter начинает новую игру
                        score = 0
                        ball_y = -ball_height
                        ball_x = random.randint(0, WIDTH - ball_width)
                        bad_ball_y = -bad_ball_height
                        bad_ball_x = random.randint(0, WIDTH - bad_ball_width)
                        waiting = False

            clock.tick(FPS)

    # Если "плохой" шар достиг нижней границы, переместите его в случайную позицию сверху
    if bad_ball_y > HEIGHT:
        bad_ball_y = -bad_ball_height
        bad_ball_x = random.randint(0, WIDTH - bad_ball_width)

    # Отрисовка на экране
    screen.blit(background_img, (0, 0))
    screen.blit(basket_img, (basket_x, basket_y))
    screen.blit(good_ball_img, (ball_x, ball_y))
    screen.blit(bad_ball_img, (bad_ball_x, bad_ball_y))

    # Отображение счета
    score_text = font.render("Счет: " + str(score), True, RED)
    screen.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()

    # Установка FPS
    clock.tick(FPS)
