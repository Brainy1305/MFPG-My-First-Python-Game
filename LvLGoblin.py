#Импортирование необходимых библиотек
import pygame
import random
import time

#Импортирование параметров экрана
from Settings import *

#Инициализация модулей PyGame
pygame.mixer.init()
pygame.init()
#Создание игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
#Загрузка и отображение фона
forest_image = pygame.image.load('Forest.jpg').convert()
forest_image = pygame.transform.scale(forest_image, (WIDTH, HEIGHT))
screen.blit(forest_image, (0, 0))

#Создание класса Главного Героя   
class MainHero:
    def __init__(self):
        #Загрузка изображения Героя
        self.hero_image = pygame.image.load('MainHero.png')
        self.hero_image = pygame.transform.scale(self.hero_image, (256, 256))
        #Создание свойств класса
        self.hpmain = 100
        self.hpmainmax = 100
        self.damagemain = 25
        self.length_sword = 64 
        self.speedmain = 20
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
        elif self.x > 1920 - 256: self.x = 1920 - 256
        if self.y < 0: self.y = 0
        elif self.y > 1080 - 256: self.y = 1080 - 256
    #Реализации функций нанесения и получения урона
    def take_damage(self, damage):
        self.hpmain -= damage
    def AttackHero(self, goblin):
        pressed = pygame.key.get_pressed()
        current_time = time.time()
        if pressed[pygame.K_SPACE] and current_time - self.last_attack_time >= self.attack_cooldown:
            pygame.mixer.music.load('Fight.mp3')
            pygame.mixer.music.play(0)            
            if abs((self.x + self.length_sword) - goblin.xg) <= 256: goblin.take_damage(self.damagemain)
            self.last_attack_time = current_time
    #Реализация функции восполнения здоровья
    def Heal(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN] and self.Acount >= 1:
            self.hpmain += self.healhp
            self.Acount = 0

#Создание класса Гоблин                   
class Goblin:
    def __init__(self):
        #Загрузка изображения Гоблина
        self.goblin_image = pygame.image.load('Goblin.png')
        self.goblin_image = pygame.transform.scale(self.goblin_image, (256, 256))
        #Создание свойств класса
        self.hpg = 500
        self.hpgmax = 500
        self.damageg = 1
        self.speedg = 30
        self.xg = 1720
        self.yg = 716
        #Ограничение позиций персонажа по границам экрана
        if self.xg < 0: self.xg = 0
        elif self.xg > 1920 - 256: self.xg = 1920 - 256
        if self.yg < 0: self.yg = 0
        elif self.yg > 1080 - 256: self.yg = 1080 - 256
    #Реализации функций нанесения и получения урона
    def take_damage(self, damage):
        self.hpg -= damage
        if self.hpg < 0: self.hpg = 0 
    def AttackGoblin(self, hero):
        current_time = time.time()
        if abs(MainHero.x - self.xg) <= 256: hero.take_damage(self.damageg)

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

#Создание класса шкалы здоровья у Гоблина
class HealthBarGoblin:
    def __init__(self, goblin):
        #Создание свойств класса
        self.Goblin = goblin
        self.bargw = 500
        self.bargh = 100
    #Реализация функции обновления шкалы здоровья
    def UpdateBarGoblin(self):
        health_ratiog = self.Goblin.hpg / self.Goblin.hpgmax
        health_rectg = pygame.Rect(1225, 100, self.bargw * health_ratiog, self.bargh)
        pygame.draw.rect(screen, (255, 0, 0), (1225, 100, self.bargw, self.bargh))
        pygame.draw.rect(screen, (0, 255, 0), health_rectg)

#Создание экземпляров классов                
MainHero = MainHero()
Hero = [MainHero]
Goblin = Goblin()
GK = [Goblin]
HealthBarHero = HealthBarHero(MainHero)
HealthBarGoblin = HealthBarGoblin(Goblin)
#Основной игровой цикл
stop = False
while not stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
    #Отображение фона     
    screen.blit(forest_image, (0, 0))
    #Вызов функций из класса Героя
    for MainHero in Hero:
        MainHero.move_main()
        MainHero.Heal()
        HealthBarHero.UpdateBarHero()
        MainHero.AttackHero(Goblin)
        #Условия завершения игры, когда Главный Герой погиб
        if MainHero.hpmain == 0:
            Hero.remove(MainHero)
            pygame.mixer.music.load('GameOver.mp3')
            pygame.mixer.music.play(0) 
    #Вызов функций из класса Гоблина       
    for Goblin in GK:
        HealthBarGoblin.UpdateBarGoblin()
        Goblin.AttackGoblin(MainHero)
        #Функция передвижения Гоблина
        if random.choice([True, False]): Goblin.xg += Goblin.speedg
        else: Goblin.xg -= Goblin.speedg
        #Ограничение позиций персонажа по границам экрана
        if Goblin.xg < 0: Goblin.xg = 0
        elif Goblin.xg > 1720 - 256: Goblin.xg = 1720 - 256
        #Условие исчезновения Гоблина
        if Goblin.hpg == 0: GK.remove(Goblin)
    #Отображение персонажей на экране
    for MainHero in Hero: screen.blit(MainHero.hero_image, (MainHero.x, MainHero.y))
    for Goblin in GK: screen.blit(Goblin.goblin_image, (Goblin.xg, Goblin.yg))
    #Обновление экрана
    pygame.display.flip()
    #Создание задержки
    pygame.time.delay(100)

#Завершение работы PyGame    
pygame.quit()
