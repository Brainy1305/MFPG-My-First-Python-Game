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
    #Реализации функций внесения и получения урона
    def take_damage(self, damage):
        self.hpmain -= damage
    def AttackHero(self, villian_1, villian_2, villian_3, mag):
        pressed = pygame.key.get_pressed()
        current_time = time.time()
        if pressed[pygame.K_SPACE] and current_time - self.last_attack_time >= self.attack_cooldown:
            pygame.mixer.music.load('Fight.mp3')
            pygame.mixer.music.play(0)                   
            if abs((self.x + self.length_sword) - villian_1.x1) <= 256: villian_1.take_damage(self.damagemain)
            if abs((self.x + self.length_sword) - villian_2.x2) <= 256: villian_2.take_damage(self.damagemain)
            if abs((self.x + self.length_sword) - villian_3.x3) <= 256: villian_3.take_damage(self.damagemain)
            if abs((self.x + self.length_sword) - villian_4.x4) <= 256: villian_4.take_damage(self.damagemain)
            if abs((self.x + self.length_sword) - mag.xmag) <= 256: mag.take_damage(self.damagemain)            
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

#Создание класса магических шаров            
class MagicShard:
    def __init__(self, xshard, yshard):
        ##Загрузка изображения магического шара
        self.shard_image = pygame.image.load('MagicShard.gif')
        self.shard_image = pygame.transform.scale(self.shard_image, (128, 128))
        #Создание свойств класса
        self.shard_x = xshard
        self.shard_y = yshard
        self.shard_damage = 1
        self.shard_speed = 20
        #Ограничение позиций магического шара по границам экрана
        if self.shard_x < 0: self.shard_x = 0
        elif self.shard_x > 1920 - 128: self.shard_x = 1920 - 128
        if self.shard_y < 0: self.shard_y = 0
        elif self.shard_y > 1080 - 128: self.shard_y = 1080 - 128
    #Реализация функции полёта
    def flying(self):
        self.shard_x -= self.shard_speed
    #Реализации функций нанесения урона
    def AttackShard(self, hero):
        current_time = time.time()
        if abs(hero.x - self.shard_x) <= 256 and hero.y == self.shard_y: hero.take_damage(self.shard_damage)

#Создание класса Маг
class Mag:
    def __init__(self):
        #Загрузка изображения мага
        self.mag_image = pygame.image.load('Mag.png')
        self.mag_image = pygame.transform.scale(self.mag_image, (256, 256))
        #Создание свойств класса
        self.xmag = 1575
        self.ymag = 716
        self.maghp = 80
        self.shoot_timer = 0
        self.shoot_delay = 5000
        #Ограничение позиций персонажа по границам экрана
        if self.xmag < 0: self.xmag = 0
        elif self.xmag > 1920 - 256: self.xmag = 1920 - 256
        if self.ymag < 0: self.ymag = 0
        elif self.ymag > 1080 - 256: self.ymag = 1080 - 256
    #Реализации функций получения урона
    def take_damage(self, damage):
        self.maghp -= damage
    #Реализации функции стрельбы
    def shoot(self):
        return MagicShard(self.xmag, self.ymag)
    #Реализации функции перезарядки навыка(cooldown)
    def update_timer(self, time):
        self.shoot_timer += time
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            return self.shoot()
        return None

#Создание класса Злодей        
class Villian_1:
    def __init__(self):
        #Загрузка изображения злодея
        self.viL1_image = pygame.image.load('ViL1.png')
        self.viL1_image = pygame.transform.scale(self.viL1_image, (256, 256))
        #Создание свойств класса
        self.hp1 = 15
        self.damage1 = 1
        self.speed1 = 15
        self.x1 = 1200
        self.y1 = 716
    #Реализация функции передвижения
    def move_1(self):
        if random.choice([True, False]): self.x1 += self.speed1
        else: self.x1 -= self.speed1
        #Ограничение позиций персонажа по границам экрана
        if self.x1 < 0: self.x1 = 0
        elif self.x1 > 1720 - 256:  self.x1 = 1720 - 256
        if self.y1 < 0: self.y1 = 0
        elif self.y1 > 1080 - 256: self.y1 = 1080 - 256
    #Реализации функций нанесения и получения урона 
    def take_damage(self, damage):
        self.hp1 -= damage
    def AttackVillian_1(self, hero):
        if abs(MainHero.x - self.x1) <= 256: hero.take_damage(self.damage1)

#Создание класса Злодей
class Villian_2:
    def __init__(self):
        #Загрузка изображения злодея
        self.viL2_image = pygame.image.load('ViL2.png')
        self.viL2_image = pygame.transform.scale(self.viL2_image, (256, 256))
        #Создание свойств класса
        self.hp2 = 50
        self.damage2 = 2
        self.speed2 = 15
        self.x2 = 1400
        self.y2 = 716
    #Реализация функции передвижения
    def move_2(self):
        if random.choice([True, False]): self.x2 += self.speed2
        else: self.x2 -= self.speed2
        #Ограничение позиций персонажа по границам экрана
        if self.x2 < 0: self.x2 = 0
        elif self.x2 > 1720 - 256:  self.x2 = 1720 - 256
        if self.y2 < 0: self.y2 = 0
        elif self.y2 > 1080 - 256: self.y2 = 1080 - 256
    #Реализации функций нанесения и получения урона
    def take_damage(self, damage):
        self.hp2 -= damage
    def AttackVillian_2(self, hero):
        if abs(MainHero.x - self.x2) <= 256: hero.take_damage(self.damage2)

#Создание класса Злодей         
class Villian_3:
    def __init__(self):
        #Загрузка изображения злодея
        self.viL2_image = pygame.image.load('ViL2.png')
        self.viL2_image = pygame.transform.scale(self.viL2_image, (256, 256))
        #Создание свойств класса
        self.hp3 = 52    #Пасхалка(хп 50 и 52)
        self.damage3 = 1 #Пасхалка(урон 1 и 2)
        self.speed3 = 20
        self.x3 = 1600
        self.y3 = 716
    #Реализация функции передвижения
    def move_3(self):
        if random.choice([True, False]): self.x3 += self.speed3
        else: self.x3 -= self.speed3
        #Ограничение позиций персонажа по границам экрана
        if self.x3 < 0: self.x3 = 0
        elif self.x3 > 1720 - 256:  self.x3 = 1720 - 256
        if self.y3 < 0: self.y3 = 0
        elif self.y3 > 1080 - 256: self.y3 = 1080 - 256
    #Реализации функций нанесения и получения урона
    def take_damage(self, damage):
        self.hp3 -= damage
    def AttackVillian_3(self, hero):
        if abs(MainHero.x - self.x3) <= 256: hero.take_damage(self.damage3)

#Создание класса Злодей
class Villian_4:
    def __init__(self):
        #Загрузка изображения злодея
        self.viL4_image = pygame.image.load('ViL4.png')
        self.viL4_image = pygame.transform.scale(self.viL4_image, (256, 256))
        #Создание свойств класса
        self.hp4 = 30
        self.damage4 = 1
        self.speed4 = 15
        self.x4 = 1100
        self.y4 = 716
    #Реализация функции передвижения
    def move_4(self):
        if random.choice([True, False]): self.x4 += self.speed4
        else: self.x4 -= self.speed4
        #Ограничение позиций персонажа по границам экрана
        if self.x4 < 0: self.x4 = 0
        elif self.x4 > 1720 - 256:  self.x4 = 1720 - 256
        if self.y4 < 0: self.y4 = 0
        elif self.y4 > 1080 - 256: self.y4 = 1080 - 256
    #Реализации функций нанесения и получения урона
    def take_damage(self, damage):
        self.hp4 -= damage
    def AttackVillian_4(self, hero):
        if abs(MainHero.x - self.x4) <= 256: hero.take_damage(self.damage4)

#Создание экземпляров классов         
MainHero = MainHero()
Hero = [MainHero]
villian_1 = Villian_1()
villian_2 = Villian_2()
villian_3 = Villian_3()
villian_4 = Villian_4()
mag = Mag()
Villian1 = [villian_1]
Villian2 = [villian_2]
Villian3 = [villian_3]
Villian4 = [villian_4]
Mag = [mag]
MagicShards = []
HealthBarHero = HealthBarHero(MainHero)
#Основной игровой цикл
clock = pygame.time.Clock()
last_time = pygame.time.get_ticks()
stop = False
while not stop:
    current_time = pygame.time.get_ticks()
    time_go = current_time - last_time
    last_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True  
    #Отображение фона
    screen.blit(forest_image, (0, 0))
    #Условие появления нового заряда у мага
    if mag.maghp > 0:
        new_shard = mag.update_timer(time_go)
        if new_shard: 
            MagicShards.append(new_shard)
    #Вызов функций магических шаров
    for shard in MagicShards:
        shard.flying()
        shard.AttackShard(MainHero)
        #Условие исчезновение мага и магических шаров
        if shard.shard_x < 0: MagicShards.remove(shard)
        if mag.maghp == 0: MagicShards.clear()
    #Вызов функций из класса Героя    
    for MainHero in Hero:
        MainHero.move_main()
        MainHero.Heal()
        HealthBarHero.UpdateBarHero()
        MainHero.AttackHero(villian_1, villian_2, villian_3, mag)
        #Условия завершения игры, когда Главный Герой погиб
        if MainHero.hpmain <= 0:
            Hero.remove(MainHero)
            pygame.mixer.music.load('GameOver.mp3')
            pygame.mixer.music.play(0)
    #Вызов функций из класса злодея    
    for villian_1 in Villian1:
        villian_1.move_1()
        villian_1.AttackVillian_1(MainHero)
        #Условие исчезновения злодея
        if villian_1.hp1 <= 0: 
            Villian1.remove(villian_1)
    #Вызов функций из класса злодея       
    for villian_2 in Villian2:
        villian_2.move_2()
        villian_2.AttackVillian_2(MainHero)
        #Условие исчезновения злодея
        if villian_2.hp2 <= 0: 
            Villian2.remove(villian_2)
    #Вызов функций из класса злодея     
    for villian_3 in Villian3:
        villian_3.move_3()
        villian_3.AttackVillian_3(MainHero)
        #Условие исчезновения злодея
        if villian_3.hp3 <= 0: 
            Villian3.remove(villian_3)
    #Вызов функций из класса злодея 
    for villian_4 in Villian4:
        villian_4.move_4()
        villian_4.AttackVillian_4(MainHero)
        #Условие исчезновения злодея
        if villian_4.hp4 <= 0: 
            Villian4.remove(villian_4)
    #Условие исчезновения мага 
    for mag in Mag:
        if mag.maghp <= 0: 
            Mag.remove(mag)
    #Отображение персонажей на экране
    for MainHero in Hero: screen.blit(MainHero.hero_image, (MainHero.x, MainHero.y))
    for mag in Mag: screen.blit(mag.mag_image, (mag.xmag, mag.ymag))
    for shard in MagicShards: screen.blit(shard.shard_image, (shard.shard_x, shard.shard_y))
    for villian_1 in Villian1: screen.blit(villian_1.viL1_image, (villian_1.x1, villian_1.y1))
    for villian_2 in Villian2: screen.blit(villian_2.viL2_image, (villian_2.x2, villian_2.y2))
    for villian_3 in Villian3: screen.blit(villian_3.viL2_image, (villian_3.x3, villian_3.y3))
    for villian_4 in Villian4: screen.blit(villian_4.viL4_image, (villian_4.x4, villian_4.y4))
    #Обновление экрана
    pygame.display.flip()
    #Создание задержки
    pygame.time.delay(100)   

#Завершение работы PyGame
pygame.quit()
