# 此文件用于声明类
import pygame
from data import *
from random import random

class Button:
    def __init__(self,x,y,image,mode = 0):
        self.image = image
        self.location = self.image.get_rect()
        if mode == 0:
            self.location.topleft = (x,y)
        else:
            self.location.center = (x,y)
            x = self.location.topleft[0]
            y = self.location.topleft[1]
        self.framelocation = pygame.Rect(x-5, y-5, self.image.get_width()+10, self.image.get_height()+10)
        self.clicked = False
    
    def run(self,screen):
        screen.blit(self.image,self.location)
        mouselocation = pygame.mouse.get_pos()
        if self.location.collidepoint(mouselocation):
            pygame.draw.rect(screen,RED,self.framelocation,5)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                return 1
            else:
                self.clicked = False
                return 0

class Dealer: # 恶魔
    def __init__(self,health,prop = []) -> None: # 初始化
        self.__tophealth = health
        self.__health = health
        self.__prop = prop
        self.__value = None
        self.__bullet = []

    def gethealth(self) -> int:
        return self.__health

    def smoke(self) -> None:
        if self.__health < self.__tophealth:
            self.__health += 1

    def setprop(self,prop) -> None: # 抽取道具
        self.__prop.append(prop)

    def getprop(self) -> list:
        return self.__prop

    def shoot(self) -> int: # 开枪
        if len(self.__bullet) == 1:return self.__bullet[0]
        del self.__bullet[0]
        if self.__value != None:
            self.__value = None
            return self.__value
        if random() >= 0.5:return 1 # 1：向玩家开枪，0：向自己开枪
        else:return 0

    def noprop(self,rm = True) -> None:
        if rm:
            self.__prop = []
        else:
            while True:
                if len(self.__prop) > 8:
                    self.__prop.pop()
                    continue
                break

    def useprop(self) -> int: # 使用道具
        '''
        args:None
        return:
        （1：使用道具
            （
            0：不用）
        ）
        '''
        if not self.__prop:
            return 0
        while True:
            rdm = random()
            if rdm <= 0.19: # 啤酒
                if "beer" in self.__prop and len(self.__bullet) != 1 and self.__value != 1:
                    del self.__prop[self.__prop.index("beer")]
                    return 1
            elif rdm <= 0.38: # 烟
                if "smoke" in self.__prop and self.__health < self.__tophealth:
                    del self.__prop[self.__prop.index("smoke")]
                    return 2
            elif rdm <= 0.57: # 手铐
                if "handcuff" in self.__prop and len(self.__bullet) != 1:
                    del self.__prop[self.__prop.index("handcuff")]
                    return 3
            elif rdm <= 0.76: # 小刀
                if "knife" in self.__prop and self.__value == 1:
                    del self.__prop[self.__prop.index("knife")]
                    return 4
            elif rdm <= 0.95: # 放大镜
                if "magnifier" in self.__prop and len(self.__bullet) != 1 and self.__value == None:
                    del self.__prop[self.__prop.index("magnifier")]
                    return 5
            else:
                return 0

    def memory(self,value):
        self.__value = value

    def setbullet(self,bullet):
        self.__bullet = bullet

    def hurt(self):
        self.__health -= 1
        print("恶魔:啊！！！")

class Player: # 人（玩家）
    def __init__(self,health,name,prop = []) -> None: # 初始化（设置血量）
        self.__tophealth = health
        self.__health = health
        self.__name = name
        self.__prop = prop
    
    def smoke(self) -> None:
        if self.__health < self.__tophealth:
            self.__health += 1

    def shoot(self) -> int: # 打出
        return int(input(f"{self.__name}想射："))

    def gethealth(self) -> int:
        return self.__health

    def getprop(self) -> list:
        return self.__prop

    def useprop(self): # 抽取道具
        while True:
            using = input(f"使用道具：")
            if using in self.__prop:
                del self.__prop[self.__prop.index(using)]
                return using
            elif using == 0:
                return 0
            else:
                print("没有此道具")

    def setprop(self,prop) -> None: # 抽取道具
        self.__prop.append(prop)

    def hurt(self) -> int: # 受伤
        self.__health -= 1
        print(f"{self.__name}：啊！！！")

    def setname(self,name):
        self.__name = name