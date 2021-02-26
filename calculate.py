"""
Калькулятор. Сохраняет и выводит историю вычислений, а так же промежуточный результат.
Поддерживает ввод с клавиатуры.

class ButFront настраивает внешний вид кнопок.

class ButBack содержит атрибуты, определяющие функционал кнопок.

class Calculate использует class ButFront для создания кнопок, и атрибуты класса ButBack в качестве команд для копок.
"""
from tkinter import *
import time

# Базовые настройки
font, pady = ('Helvetica', 32, 'bold'), 0


class ButFront(Button):
    def __init__(self, parent=None, **options):
        Button.__init__(self, parent, **options)
        self.config(font=('Helvetica', 15))
        self.config(width=6, height=2, bd=2, relief=GROOVE)
        self.defaultBackground = self['background']
        self.activeBackground = self['activebackground']
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        #self['background'] = self['activebackground']
        event.widget.config(bg=self.activeBackground)

    def on_leave(self, event):
        #self['background'] = self.defaultBackground
        event.widget.config(bg=self.defaultBackground)

    def on_press(self):
        """
        Функция on_press имитирует эффект нажатия кнопки.
        Применяется при вводе с клавиатуры.
        """
        self.config(relief=SUNKEN, bg=self.activeBackground)
        self.update()       # Без update не работает
        time.sleep(0.1)
        self.config(relief=GROOVE, bg=self.defaultBackground)


class ButBack():
    def zero(self):  ButBack.number(self, '0')
    def one(self):   ButBack.number(self, '1')
    def two(self):   ButBack.number(self, '2')
    def three(self): ButBack.number(self, '3')
    def four(self):  ButBack.number(self, '4')
    def five(self):  ButBack.number(self, '5')
    def six(self):   ButBack.number(self, '6')
    def seven(self): ButBack.number(self, '7')
    def eight(self): ButBack.number(self, '8')
    def nine(self):  ButBack.number(self, '9')
    def dot(self):
        if self.numberCurrent:
            try:
                if '.' not in self.numberCurrent:        # не добавляем точку, еси она уже есть
                    if self.numberCurrent == '0':        # исключает баг после сброса CE
                        ButBack.number(self, '0.')
                    else:
                        ButBack.number(self, '.')
            except TypeError:                         # Если исключение, то скорее всего, мы имеем дело с результатом
                ButBack.number(self, '0.')            # который нужно сбросить. Это же делает и number, но тода
        else:                                         # будет вывод вместо '0.', '.'
            ButBack.number(self, '0.')
    def number(self, num):
        if not self.numberAll:                      # Сбрасываем хронологию. Например после =
            self.labelChrony.config(text='')
        try:
            if self.numberAll[-1] not in ['+', '-', '*', '/']:      # Удаляем временные значения
                self.numberAll = self.numberAll[:-1]
                self.numberAllShort = self.numberAllShort[:-1]
                self.labelChrony.config(text=' '.join(str(i) for i in self.numberAll))
        except IndexError: pass
        if self.numberCurrent != '0':            # Исключаем значения '01'
            try:
                self.numberCurrent += str(num)
            except TypeError:
                self.numberCurrent = str()          # Исключение служит, что бы сбросить значения
                self.numberCurrent += str(num)      # например после =
        else:
            self.numberCurrent = str()
            self.numberCurrent += str(num)
        self.labelResult.config(text=self.numberCurrent, font=font, pady=pady)

    def plus(self):     ButBack.chronology(self, action='+')
    def minus(self):    ButBack.chronology(self, action='-')
    def multiply(self): ButBack.chronology(self, action='*')
    def devision(self): ButBack.chronology(self, action='/')
    def chronology(self, action):
        try:
            if self.numberAll[-1] in ['+', '-', '*', '/'] and not self.numberCurrent:       # если меняем знак
                self.numberAll = self.numberAll[:-1]                                        # после + нажимаем -
                self.numberAll.append(action)
                self.numberAllShort = self.numberAllShort[:-1]
                self.numberAllShort.append(action)
        except IndexError: pass
        if self.numberCurrent:      # добавляем и сбрасываем текущее значение
            current = ButBack.rounding(self, float(self.numberCurrent))
            if current >= 0:
                self.numberAll.append(current)
            else:
                self.numberAll.append('(' + str(current) + ')')
            self.numberAllShort.append(ButBack.rounding(self, float(self.numberCurrent)))
            self.numberCurrent = str()
        # Cчитаем промежуточный результат. Текущий результат всегда будет равен self.numberAllShort[0]
        if len(self.numberAllShort) > 2:
            try:
                self.numberAllShort = [eval(' '.join(str(i) for i in self.numberAllShort))]
            except ZeroDivisionError:
                self.labelResult.config(text='Деление на ноль невозможно', font=('Helvetica', 16), pady=14)
                ButBack.drop(self)
                return
        try:                             # добавляем арифметический знак
            if self.numberAll[-1] not in ['+', '-', '*', '/']:
                self.numberAll.append(action)
                self.numberAllShort.append(action)
            self.result = ButBack.rounding(self, self.numberAllShort[0])
            self.labelResult.config(text=self.result, font=font, pady=pady)
            self.labelChrony.config(text=' '.join(str(i) for i in self.numberAll))
        except IndexError: pass

    def sqr(self):
        factor1 = "float(self.numberCurrent) ** 2"
        factor2 = "float(self.result) ** 2"
        ButBack.sqrAll(self, factor1, factor2, text='sqr(')
    def sqrRoot(self):
        factor1 = "float(self.numberCurrent) ** 0.5"
        factor2 = "float(self.result) ** 0.5"
        ButBack.sqrAll(self, factor1, factor2, text='√(')
    def oneDevisionX(self):
        factor1 = "1 / float(self.numberCurrent)"
        factor2 = "1 / float(self.result)"
        ButBack.sqrAll(self, factor1, factor2, text='1/(')
    def sqrAll(self, factor1, factor2, text):
        if self.numberCurrent:
            try:
                self.result = ButBack.rounding(self, eval(factor1))
                if self.result == None:     # обработка исключения округления, строка 241
                    ButBack.drop(self)
                    return
            except ZeroDivisionError:
                self.labelResult.config(text='Деление на ноль невозможно', font=('Helvetica', 16), pady=14)
                ButBack.drop(self)
                return
            self.numberAll.append(text + str(self.numberCurrent) + ')')
            self.numberAllShort.append(self.result)
            self.numberCurrent = str()
        else:
            try:
                if self.numberAll[-1] not in ['+', '-', '*', '/']:
                    self.numberAll.pop()
                    self.numberAllShort.pop()
                self.numberAll.append(text + str(self.result) + ')')
                try:
                    self.result = ButBack.rounding(self, eval(factor2))
                except ZeroDivisionError:
                    self.labelResult.config(text='Деление на ноль невозможно', font=('Helvetica', 16), pady=14)
                    ButBack.drop(self)
                    return
                self.numberAllShort.append(self.result)
            except IndexError: pass
        self.labelResult.config(text=self.result, font=font, pady=pady)
        self.labelChrony.config(text=' '.join(str(i) for i in self.numberAll))

    def posNeg(self):
        if self.numberCurrent:
            self.numberCurrent = str(eval('-' + str(self.numberCurrent)))
            self.labelResult.config(text=self.numberCurrent, font=font, pady=pady)
        else:
            try:
                if self.numberAll[-1] not in ['+', '-', '*', '/']:
                    self.numberAll.pop()
                    self.numberAllShort.pop()
                self.result = eval('-' + str(self.result))
                self.numberAll.append('(' + str(self.result) + ')')
                self.numberAllShort.append(self.result)
                self.labelResult.config(text=self.result, font=font, pady=pady)
                self.labelChrony.config(text=' '.join(str(i) for i in self.numberAll))
            except IndexError: pass

    def returnBack(self):
        try:
            if self.numberCurrent:
                self.numberCurrent = self.numberCurrent[:-1]
                if self.numberCurrent:
                    self.labelResult.config(text=self.numberCurrent, font=font, pady=pady)
                else:
                    self.result = 0
                    self.numberCurrent = str()
                    self.labelResult.config(text=self.result, font=font, pady=pady)
        except TypeError: pass

    def drop(self):
        self.result = 0
        self.numberAll = list()
        self.numberAllShort = list()
        self.numberCurrent = str()

    def cancel(self):
        ButBack.drop(self)
        self.labelResult.config(text=self.result, font=font, pady=pady)
        self.labelChrony.config(text='')

    def ce(self):
        self.numberCurrent = '0'
        try:
            if self.numberAll[-1] not in ['+', '-', '*', '/']:
                self.numberAll = self.numberAll[:-1]
                self.numberAllShort = self.numberAllShort[:-1]
        except IndexError: pass
        self.labelResult.config(text=self.numberCurrent, font=font, pady=pady)
        self.labelChrony.config(text=' '.join(str(i) for i in self.numberAll))

    def percent(self):
        if self.numberCurrent and self.result:
            self.numberCurrent = ButBack.rounding(self, self.result * float(self.numberCurrent) / 100, 0)
            self.labelResult.config(text=self.numberCurrent, font=font, pady=pady)
            self.labelChrony.config(text=' '.join(str(i) for i in self.numberAll))

    def res(self):
        if self.numberCurrent:
            self.numberAll.extend([ButBack.rounding(self, float(self.numberCurrent)), '='])
            self.numberAllShort.append(ButBack.rounding(self, float(self.numberCurrent)))
        else:
            try:
                if type(self.numberAllShort[-1]) in (int, float):
                    self.numberAll.append('=')
                else:
                    self.numberAll.extend([self.result, '='])
                    self.numberAllShort.append(self.result)
            except IndexError: pass
        try:
            self.result = ButBack.rounding(self, (float(eval(' '.join(str(i) for i in self.numberAllShort)))))
        except ZeroDivisionError: # сбиваются настройки font и pady, из за чего, во всех labelRes дублируются настройки
            self.labelResult.config(text='Деление на ноль невозможно', font=('Helvetica', 16), pady=14)
            ButBack.drop(self)
            return
        except SyntaxError: pass
        self.labelChrony.config(text=' '.join(str(i) for i in self.numberAll))
        self.labelResult.config(text=self.result, font=font, pady=pady)
        res = self.result       # сохраняем переменную для продолжения
        ButBack.drop(self)
        self.numberCurrent = res

    def rounding(self, res, attribute=1):     # Округляем результат
        if not str(abs(res)).isdigit() and not str(res).endswith('.0'):     # abs решает проблему отрицательных чисел
            try:
                if attribute: self.result = float(res)
                else:         self.numberCurrent = float(res)
            except:
                self.labelResult.config(text='Слишком сложно, даже для меня :)', font=('Helvetica', 13), pady=15)
                ButBack.drop(self)
                return None
        else:
            if attribute: self.result = int(res)
            else:         self.numberCurrent = int(res)
        return self.result if attribute else self.numberCurrent


class Calculate(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.master.title('Калькулятор')
        self.result = 0                      # результат
        self.numberAll = list()              # для хронологии
        self.numberAllShort = list()         # для вычислений
        self.numberCurrent = str()           # текущее значение
        self.labelChrony = Label(parent, height=3, font=('Helvetica'), anchor=SE)        # хронология
        self.labelChrony.pack(expand=True, fill=BOTH)
        self.labelResult = Label(parent, text=0, font=font, pady=pady, anchor=NE)        # результат
        self.labelResult.pack(expand=True, fill=BOTH)

        val = [['%', ButBack.percent],        ['CE', ButBack.ce],   ['C', ButBack.cancel],  ['⌫', ButBack.returnBack],
               ['¹/ₓ', ButBack.oneDevisionX],  ['x²', ButBack.sqr], ['√', ButBack.sqrRoot], ['÷', ButBack.devision],
               [7, ButBack.seven],            [8, ButBack.eight],   [9, ButBack.nine],      ['×', ButBack.multiply],
               [4, ButBack.four],             [5, ButBack.five],    [6, ButBack.six],       ['−', ButBack.minus],
               [1, ButBack.one],              [2, ButBack.two],     [3, ButBack.three],     ['+', ButBack.plus],
               ['+/-', ButBack.posNeg],       [0, ButBack.zero],    [',', ButBack.dot],     ['=', ButBack.res]]

        self.butlist = {}
        while val:
            frameButton = Frame(parent)
            frameButton.pack(expand=True, fill=BOTH)
            valSlice, val = val[:4], val[4:]
            for sign in valSlice:
                x = sign[1]
                if type(sign[0]) == int or sign[0] == '+/-' or sign[0] == ',':
                    but = ButFront(frameButton, text=sign[0], command=lambda x=x: x(self),
                                                 bg='#F5F5F5', activebackground='#D3D3D3')
                elif sign[0] == '=':
                    but = ButFront(frameButton, text=sign[0], command=lambda x=x: x(self),
                                                 bg='#87CEFA', activebackground='#1E90FF')
                else:
                    but = ButFront(frameButton, text=sign[0], command=lambda x=x: x(self),
                                                 bg='#DCDCDC', activebackground='#D3D3D3')
                but.pack(side=LEFT, expand=True, fill=BOTH)
                self.butlist.update({sign[1]: but})
        self.bind('<KeyPress>', self.press)
        self.focus()

    def press(self, event):
        keymap = {
            '0': ButBack.zero,
            '1': ButBack.one,
            '2': ButBack.two,
            '3': ButBack.three,
            '4': ButBack.four,
            '5': ButBack.five,
            '6': ButBack.six,
            '7': ButBack.seven,
            '8': ButBack.eight,
            '9': ButBack.nine,
            '+': ButBack.plus,
            '-': ButBack.minus,
            '*': ButBack.multiply,
            '/': ButBack.devision,
            '=': ButBack.res,
            '%': ButBack.percent,
            '@': ButBack.sqrRoot,
            ',': ButBack.dot,
            '.': ButBack.dot
        }
        keycode = {
            13: ButBack.res,           # Enter
            8:  ButBack.returnBack,    # BackSpace
            27: ButBack.cancel,        # ESC
            46: ButBack.ce,            # DEL
            82: ButBack.oneDevisionX,  # r, R, к, К
            81: ButBack.sqr            # q, Q, й, Й
        }
        if event.char in keymap:
            keymap[event.char](self)
            but = self.butlist[keymap[event.char]]
            but.on_press()
        if event.keycode in keycode:
            keycode[event.keycode](self)
            but = self.butlist[keycode[event.keycode]]
            but.on_press()



if __name__ == '__main__':
    test = Calculate()
    test.pack()
    mainloop()
