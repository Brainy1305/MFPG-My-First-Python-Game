#Импортирование необходимой библиотеки
import pygame

#Импортирование параметров экрана
from Settings import *

#Инициализация модулей PyGame
pygame.mixer.init()
pygame.init()
#Создание игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
#Загрузка и отображение фона
village_image = pygame.image.load('Village.jpg').convert()
village_image = pygame.transform.scale(village_image, (WIDTH, HEIGHT))
screen.blit(village_image, (0, 0))

#Создание класса Главного Героя  
class MainHero:
    def __init__(self):
        #Загрузка изображения Героя
        self.hero_image = pygame.image.load('MainHero.png')
        self.hero_image = pygame.transform.scale(self.hero_image, (256, 256))
        #Создание свойств класса
        self.hpmain = 100
        self.hpmainmax = 100
        self.damagemain = 20
        self.speedmain = 15
        self.x = 1450
        self.y = 716
        self.jumping = False
        self.jump_height = 512
        self.jump_count = 1
        self.last_attack_time = 0
        self.attack_cooldown = 1
    #Реализация функции передвижения и прыжка
    def move_main(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.jumping = True
        if self.jumping:
            if self.jump_count >= -1:
                self.y -= (self.jump_count * abs(self.jump_height)) * 0.5
                self.jump_count -= 1
            else:
                self.jumping = False
                self.jump_count = 1
        if pressed[pygame.K_LEFT]: self.x -= self.speedmain
        if pressed[pygame.K_RIGHT]: self.x += self.speedmain
        #Ограничение позиций персонажа по границам экрана
        if self.x < 0: self.x = 0
        elif self.x > 1720 - 256: self.x = 1720 - 256
        if self.y < 0: self.y = 0
        elif self.y > 1080 - 256: self.y = 1080 - 256

#Создание класса Принцесса
class Princess:
    def __init__(self):
        #Загрузка изображения принцессы
        self.princess_image = pygame.image.load('Princess.png')
        self.princess_image = pygame.transform.scale(self.princess_image, (256, 256))
        #Создание свойств класса
        self.name = "Принцесса Афина"
        self.xPr = 1400
        self.yPr = 716
        self.speedPr = 10
        self.meet = False
    #Реализация функции воспроизведения реплики
    def talk2Pr(self):
        pygame.mixer.music.load('PrincessTalk2.wav')
        pygame.mixer.music.play(0)
        self.meet = True
    #Реализация функции передвижения
    def movePr(self):
        if self.xPr > 200: self.xPr -= self.speedPr
        #Ограничение позиций персонажа по границам экрана
        if self.xPr < 0: self.xPr = 0
        elif self.xPr > 1920 - 256: self.xPr = 1920 - 256
        if self.yPr < 0: self.yPr = 0
        elif self.yPr > 1080 - 256: self.yPr = 1080 - 256        

#Создание класса Король    
class King:
    def __init__(self):
        #Загрузка изображения короля
        self.king_image = pygame.image.load('KingTalk1.png')
        self.king_image = pygame.transform.scale(self.king_image, (256, 256))
        #Создание свойств класса
        self.name = "Король Ричард LII" #Пасхалка 52
        self.x2K = 100
        self.y2K = 716
        self.talk2 = False
        #Ограничение позиций персонажа по границам экрана
        if self.x2K < 0: self.x2K = 0
        elif self.x2K > 1920 - 256: self.x2K = 1920 - 256
        if self.y2K < 0: self.y2K = 0
        elif self.y2K > 1080 - 256: self.y2K = 1080 - 256
    #Реализация функции воспроизведения реплики
    def talk_2(self):
        pygame.mixer.music.load('KingTalk2.mp3')
        pygame.mixer.music.play(0)
        self.talk2 = True

#Создание экземпляров классов       
MainHero = MainHero()
Princess = Princess()
King = King()
#Основной игровой цикл
stop = False
while not stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
    #Отображение фона        
    screen.blit(village_image, (0, 0))
    #Вызов функций из классов
    MainHero.move_main()
    Princess.movePr()
    if MainHero.x >= Princess.xPr - 256 and not Princess.meet: Princess.talk2Pr()
    if King.x2K >= MainHero.x - 256 and not King.talk2: King.talk_2()
    #Отображение персонажей на экране
    screen.blit(MainHero.hero_image, (MainHero.x, MainHero.y))
    screen.blit(Princess.princess_image, (Princess.xPr, Princess.yPr))
    screen.blit(King.king_image, (King.x2K, King.y2K))
    #Обновление экрана
    pygame.display.flip()
    #Создание задержки
    pygame.time.delay(100)   

#Завершение работы PyGame
pygame.quit()
