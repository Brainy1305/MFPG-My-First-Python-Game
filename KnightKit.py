#Импортирование необходимых библиотек
import pygame
import random
import tkinter as tk
import time

#Импортирование параметров экрана
from Settings import *

#Реализация функции переключения уровней
def start_level(level):
    if level == 1:
        import Edutainment
    elif level == 2:
        import MainFights
    elif level == 3:
        import LvLGoblin
    elif level == 4:
        import LvLDragon
    elif level == 5:
        import End
    elif level == 6:
        import Credits

#Реализации функции создания меню с уровнями
def create_menu():
    root = tk.Tk()
    root.title("Меню уровней")

    #Настройка шрифта для текста
    label = tk.Label(root, text="Выберите уровень", font=(None, 74))
    label.pack(pady=20)
    #Создание кнопок
    buttons_frame = tk.Frame(root)
    buttons_frame.pack()
    #Реализация механики кнопок
    for i in range(1, 7):
        button = tk.Button(buttons_frame, text=f"Уровень {i}", font=(None, 24),
                           command=lambda i=i: start_level(i))
        button.grid(row=0, column=i-1, padx=10)

    root.mainloop()

#Вызов Меню с уровнями
if __name__ == "__main__":
    create_menu()
