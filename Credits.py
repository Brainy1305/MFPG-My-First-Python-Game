#Импортирование необходимых библиотек
import pygame
import sys

#Импортирование параметров экрана
from Settings import *

#Инициализация модулей PyGame
pygame.mixer.init()
pygame.init()
#Загрузка и воспроизведение звука
pygame.mixer.music.load('gameSong.mp3')
pygame.mixer.music.play(0)
#Создание игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
#Загрузка и отображение фона
credits_image = pygame.image.load('Flash.png').convert()
credits_image = pygame.transform.scale(credits_image, (WIDTH, HEIGHT))
screen.blit(credits_image, (0, 0))
#Настройка шрифта для текста
font = pygame.font.Font(None, 74)
#Создание текста для отображения на экране
text1 = font.render('Разработал игру, создал модели, написал текст' , True, (255, 255, 255)) 
text2 = font.render('ученик 10"Ж" класса Школы ГБОУ 1636 Ника', True, (255, 255, 255))
text3 = font.render('Чистяков Даниил Альбертович', True, (255, 255, 255))
text4 = font.render('Спасибо за то, что сыграли в мою игру!', True, (255, 255, 255))
#Основной игровой цикл
stop = False
while not stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
    #Отображение фона
    screen.blit(credits_image, (0, 0))
    #Отображение текста
    screen.blit(text1, (400, 125))
    screen.blit(text2, (425, 175))
    screen.blit(text3, (600, 225))
    screen.blit(text4, (470, 900))
    #Обновление экрана
    pygame.display.flip()

#Завершение работы PyGame
pygame.quit()
#Выход из программы
sys.exit()
