import os 


def line():
    print(f'\33[1m\33[32m {"_" * (os.get_terminal_size().columns - 8)}')
    reset()


def reset():
    print("\033[0m")
    
    
def debug_(*args):
    line()
    for i in args:
        print(f"\033[35m\33[1m\033[3m {i}")
    line()


def subtract_perecnt(number: int, percent: int):
    return round(number - ((number * percent) / 100), 2)





"""
\033[0-7m — это различные эффекты, такие как подчеркивание, мигание, жирность и так далее;
\033[30-37m — коды, определяющие цвет текста (
    черный, красный, зелёный, жёлтый, синий, фиолетовый, сине-голубой, серый);
\033[40-47m — коды, определяющие цвет фона.


Цвет       Текст     Фон
------------------------
Чёрный	    30	     40
Красный	    31	     41
Зелёный	    32	     42
Жёлтый	    33	     43
Синий	    34	     44
Фиолетовый	35	     45
Бирюзовый	36	     46
Белый	    37	     47


Эффекты

Код    Значение
-------------------------------------
0      Сброс к начальным значениям
1      Жирный
2      Блёклый
3      Курсив
4      Подчёркнутый
5      Редкое мигание
6      Частое мигание
7      Смена цвета фона с цветом текста


"""