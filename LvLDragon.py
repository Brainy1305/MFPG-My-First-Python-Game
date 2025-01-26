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
dragonhome_image = pygame.image.load('DragonHome.jpg').convert()
dragonhome_image = pygame.transform.scale(dragonhome_image, (WIDTH, HEIGHT))
screen.blit(dragonhome_image, (0, 0))

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
        elif self.x > 1720 - 256: self.x = 1720 - 256
        if self.y < 0: self.y = 0
        elif self.y > 1080 - 256: self.y = 1080 - 256
    #Реализации функций нанесения и получения урона
    def take_damage(self, damage):
        self.hpmain -= damage
    def AttackHero(self, dragon):
        pressed = pygame.key.get_pressed()
        current_time = time.time()
        if pressed[pygame.K_SPACE] and current_time - self.last_attack_time >= self.attack_cooldown:
            pygame.mixer.music.load('Fight.mp3')
            pygame.mixer.music.play(0)            
            if abs((self.x + self.length_sword) - dragon.xd) <= 256: dragon.take_damage(self.damagemain)
            self.last_attack_time = current_time
    #Реализация функции восполнения здоровья
    def Heal(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN] and self.Acount >= 1:
            self.hpmain += self.healhp
            self.Acount = 0    

#Создание класса Дракона
class Dragon:
    def __init__(self):
        #Загрузка изображения Дракона
        self.dragon_image = pygame.image.load('Dragon.png')
        self.dragon_image = pygame.transform.scale(self.dragon_image, (512, 512))
        #Создание свойств класса
        self.hpd = 500
        self.hpdmax = 500
        self.damaged = 1.5
        self.speedd = 30
        self.dragonheal = 0.1
        self.xd = 1720
        self.yd = 450
        #Ограничение позиций персонажа по границам экрана
        if self.xd < 0: self.xd = 0
        elif self.xd > 1720 - 512: self.xd = 1720 - 512
        if self.yd < 0: self.yd = 0
        elif self.yd > 1080 - 512: self.yd = 1080 - 512
    #Реализации функций нанесения и получения урона
    def take_damage(self, damage):
        self.hpd -= damage
        if self.hpd < 0: self.hpd = 0
    def AttackDragon(self, hero):
        current_time = time.time()
        if abs(MainHero.x - self.xd) <= 256: hero.take_damage(self.damaged)
    #Реализация функции восполнения здоровья
    def DragonHeal(self):
        if self.hpd > 0:
            self.hpd += self.dragonheal

#Создание класса Принцесса        
class Princess:
    def __init__(self):
        #Загрузка изображения принцессы
        self.princess_image = pygame.image.load('Princess.png')
        self.princess_image = pygame.transform.scale(self.princess_image, (256, 256))
        #Создание свойств класса
        self.name = "Принцесса Афина"
        self.xPr = 1720
        self.yPr = 716
        self.rescued = False
        #Ограничение позиций персонажа по границам экрана
        if self.xPr < 0: self.xPr = 0
        elif self.xPr > 1720 - 256: self.xPr = 1720 - 256
        if self.yPr < 0: self.yPr = 0
        elif self.yPr > 1080 - 256: self.yPr = 1080 - 256
    #Реализация функции воспроизведения реплики
    def talk1Pr(self):
        pygame.mixer.music.load('PrincessTalk1.wav')
        pygame.mixer.music.play(0)
        self.rescued = True

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

#Создание класса шкалы здоровья у Дракона
class HealthBarDragon:
    def __init__(self, dragon):
        #Создание свойств класса
        self.Dragon = dragon
        self.bardw = 500
        self.bardh = 100
    def UpdateBarDragon(self):
        #Реализация функции обновления шкалы здоровья
        health_ratiod = self.Dragon.hpd / self.Dragon.hpdmax
        health_rectd = pygame.Rect(1225, 100, self.bardw * health_ratiod, self.bardh)
        pygame.draw.rect(screen, (255, 0, 0), (1225, 100, self.bardw, self.bardh))
        pygame.draw.rect(screen, (0, 255, 0), health_rectd)

#Создание экземпляров классов                
MainHero = MainHero()
Hero = [MainHero]
Princess = Princess()
Pr = []
Dragon = Dragon()
Final = [Dragon]
HealthBarHero = HealthBarHero(MainHero)
HealthBarDragon = HealthBarDragon(Dragon)
#Основной игровой цикл
stop = False
while not stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
    #Отображение фона        
    screen.blit(dragonhome_image, (0, 0))
    #Вызов функций из класса Героя
    for MainHero in Hero:
        MainHero.move_main()
        MainHero.Heal()
        HealthBarHero.UpdateBarHero()
        MainHero.AttackHero(Dragon)
        #Условия завершения игры, когда Главный Герой погиб
        if MainHero.hpmain <= 0:
            Hero.remove(MainHero)
            pygame.mixer.music.load('GameOver.mp3')
            pygame.mixer.music.play(0)
    #Вызов функций из класса Дракона       
    for Dragon in Final:
        HealthBarDragon.UpdateBarDragon()
        Dragon.AttackDragon(MainHero)
        Dragon.DragonHeal()
        #Функция передвижения Дракона
        if random.choice([True, False]): Dragon.xd += Dragon.speedd
        else: Dragon.xd -= Dragon.speedd
        #Ограничение позиций персонажа по границам экрана
        if Dragon.xd < 0: Dragon.xd = 0
        elif Dragon.xd > 1720 - 512: Dragon.xd = 1720 - 512
        #Условие исчезновения Дракона и появления Принцессы Афины
        if Dragon.hpd <= 0:
            Final.remove(Dragon)
            Pr.append(Princess)
            Princess.talk1Pr()
    #Отображение персонажей на экране
    for MainHero in Hero: screen.blit(MainHero.hero_image, (MainHero.x, MainHero.y))
    for Dragon in Final: screen.blit(Dragon.dragon_image, (Dragon.xd, Dragon.yd))
    for Princess in Pr: screen.blit(Princess.princess_image, (Princess.xPr, Princess.yPr))
    #Обновление экрана
    pygame.display.flip()
    #Создание задержки
    pygame.time.delay(100)

#Завершение работы PyGame    
pygame.quit()
