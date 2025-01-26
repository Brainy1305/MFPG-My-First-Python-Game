#Импортирование необходимых библиотек
import pygame
import time

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
        self.hpmain = 75
        self.hpmainmax = 100
        self.damagemain = 20
        self.speedmain = 15
        self.x = 100
        self.y = 716
        self.jumping = False
        self.jump_height = 512
        self.jump_count = 1
        self.last_attack_time = 0
        self.attack_cooldown = 0.9
        self.healhp = 25
        self.Acount = 1
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
    #Реализации функций нанесения и получения урона
    def take_damage(self, damage):
        self.hpmain -= damage
        if self.hpmain < 0: self.hpmain = 0
    def AttackHero(self, stand):
        pressed = pygame.key.get_pressed()
        current_time = time.time()
        if pressed[pygame.K_SPACE] and current_time - self.last_attack_time >= self.attack_cooldown:
            pygame.mixer.music.load('Fight.mp3')
            pygame.mixer.music.play(0)            
            if abs(self.x - stand.xstand) <= 256: stand.take_damage(self.damagemain)
            self.last_attack_time = current_time
    #Реализация функции восполнения здоровья
    def Heal(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN] and self.Acount >= 1:
            self.hpmain += self.healhp
            self.Acount = 0    

#Создание класса шкалы здоровья у Главного Героя
class HealthBarHero:
    def __init__(self, hero):
        #Создание свойств класса
        self.MainHero = hero
        self.barhw = 100
        self.barhh = 10
    #Реализация функции обновления шкалы здоровья
    def UpdateBarHero(self):
        health_ratioh = self.MainHero.hpmain / self.MainHero.hpmainmax
        health_recth = pygame.Rect(self.MainHero.x + 130, self.MainHero.y + 20, self.barhw * health_ratioh, self.barhh)
        pygame.draw.rect(screen, (255, 0, 0), (self.MainHero.x + 130, self.MainHero.y + 20, self.barhw, self.barhh))
        pygame.draw.rect(screen, (0, 255, 0), health_recth)

#Создание класса Манекен
class Stand:
    def __init__(self):
        #Загрузка изображения манекена
        self.stand_image = pygame.image.load('Stand.png')
        self.stand_image = pygame.transform.scale(self.stand_image, (256, 256))
        #Создание свойств класса
        self.xstand = 1000
        self.ystand = 716
        #Ограничение позиций персонажа по границам экрана
        if self.xstand < 0: self.xstand = 0
        elif self.xstand > 1920 - 256: self.xstand = 1920 - 256
        if self.ystand < 0: self.ystand = 0
        elif self.ystand > 1080 - 256: self.ystand = 1080 - 256

#Создание класса Король        
class King:
    def __init__(self):
        #Загрузка изображения короля
        self.king_image = pygame.image.load('KingTalk1.png')
        self.king_image = pygame.transform.scale(self.king_image, (256, 256))
        #Создание свойств класса
        self.name = "Король Ричард LII" #Пасхалка 52
        self.x1K = 1450
        self.y1K = 716
        self.talk1 = False
        #Ограничение позиций персонажа по границам экрана
        if self.x1K < 0: self.x1K = 0
        elif self.x1K > 1920 - 256: self.x1K = 1920 - 256
        if self.y1K < 0: self.y1K = 0
        elif self.y1K > 1080 - 256: self.y1K = 1080 - 256
    #Реализация функции воспроизведения реплики
    def talk_1(self):
        pygame.mixer.music.load('KingTalk1.mp3')
        pygame.mixer.music.play(0)
        self.talk1 = True

#Создание экземпляров классов        
MainHero = MainHero()
King = King()
Stand = Stand()
HealthBarHero = HealthBarHero(MainHero)
#Основной игровой цикл
ED = False
clock = pygame.time.Clock()
last_time = pygame.time.get_ticks()
stop = False
while not stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
    #Отображение фона        
    screen.blit(village_image, (0, 0))
    #Вызов функций из классов
    MainHero.move_main()
    MainHero.AttackHero(Stand)
    MainHero.Heal()
    HealthBarHero.UpdateBarHero()    
    if MainHero.x >= King.x1K - 512 and not King.talk1: King.talk_1()
    if MainHero.x == MainHero.x and not ED:
        pygame.mixer.music.load('ED.mp3')
        pygame.mixer.music.play(0)
        ED = True
    #Отображение персонажей на экране
    screen.blit(MainHero.hero_image, (MainHero.x, MainHero.y))
    screen.blit(King.king_image, (King.x1K, King.y1K))
    screen.blit(Stand.stand_image, (Stand.xstand, Stand.ystand))
    #Обновление экрана
    pygame.display.flip()
    #Создание задержки
    pygame.time.delay(100)

#Завершение работы PyGame    
pygame.quit()
