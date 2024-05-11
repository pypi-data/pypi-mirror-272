# 主程序
# 外部导入
from locale import getdefaultlocale as lcl,setlocale as stlcl,LC_ALL
from gettext import translation
from random import shuffle,random
from time import sleep
from os.path import dirname
from sys import path
#import treading
#treading.Tread() # TODO
path.append(dirname(__file__))
# 模块导入
from data import *
from sprites import Dealer,Player

stlcl(LC_ALL,"")
lang, _ = lcl()
trans = translation("trans",LOCALE,languages=[lang],fallback=True)
_ = trans.gettext

def printprop(prop):
    for p in prop:
        if p == "beer":
            print(_("啤酒"))
        elif p == "smoke":
            print(_("烟"))
        elif p == "handcuff":
            print(_("手铐"))
        elif p == "knife":
            print(_("小刀"))
        else:
            print(_("放大镜"))

# 以下是主程序
def run(CHEAT = False):
    try:
        playerknife = False
        dealerknife = False
        name = input(_("输入名字：")) # 输入名字
        for j in range(3): # 三个回合
            brk = False
            dealer = Dealer(HEALTH[j]) # 恶魔初始化
            player = Player(HEALTH[j],name) # 玩家初始化
            for i in range(len(BULLETS[j])): # 每一小轮
                if brk:
                    brk = False
                    break
                buckshot = BULLETS[j][i] # 初始化本轮子弹
                buckshotcount = [0,0] #子弹计数
                for k in buckshot: # 实弹
                    if k:buckshotcount[0]+=1
                for k in buckshot: # 空弹
                    if k == 0:buckshotcount[1]+=1
                shuffle(buckshot) # 打乱子弹顺序
                dealer.setbullet(buckshot)
                print(_(f"{buckshotcount[0]}发实弹,{buckshotcount[1]}发空弹")) # 打印子弹提示
                if j:
                    for k in range(HEALTH[j-1]):
                        rdm = random()
                        if rdm <= 0.2: # 啤酒
                            dealer.setprop("beer")
                        elif rdm <= 0.4: # 烟
                            dealer.setprop("smoke")
                        elif rdm <= 0.6: # 手铐
                            dealer.setprop("handcuff")
                        elif rdm <= 0.8: # 小刀
                            dealer.setprop("knife")
                        else:
                            dealer.setprop("magnifier")
                    for k in range(HEALTH[j-1]):
                        rdm = random()
                        if rdm <= 0.2: # 啤酒
                            player.setprop("beer")
                        elif rdm <= 0.4: # 烟
                            player.setprop("smoke")
                        elif rdm <= 0.6: # 手铐
                            player.setprop("handcuff")
                        elif rdm <= 0.8: # 小刀
                            player.setprop("knife")
                        else:
                            player.setprop("magnifier")
                print(_("恶魔的道具："))
                printprop(dealer.getprop())
                print(_("你的道具："))
                printprop(player.getprop())
                next = 0 # 下一轮
                brk = False
                ctn = False
                ctnl = False
                playercuff = False
                dealercuff = False
                for b in buckshot:
                    if CHEAT:
                        print("Bullets:",buckshot)
                    print(f"恶魔血量：{dealer.gethealth()} {name}的血量：{player.gethealth()}")
                    if next == 0:
                        if j:
                            while True:
                                useprop = player.useprop()
                                if useprop == 0: # TODO
                                    break
                                elif useprop == 1: # 啤酒
                                    print(_("正在使用：啤酒"))
                                    if b:
                                        print(_("下一发是：实弹"))
                                    else:
                                        print(_("下一发是：空弹"))
                                    ctnl = True
                                    break
                                elif useprop == 2: # 烟
                                    print(_("正在使用：烟"))
                                    player.smoke()
                                elif useprop == 3:
                                    print(_("正在使用：手铐"))
                                    dealercuff = True
                                elif useprop == 4:
                                    print(_("正在使用：小刀"))
                                    playerknife = True
                                else:
                                    print(_("正在使用：放大镜"))
                                    if buckshot[0]:
                                        print(_("下一发是：实弹"))
                                    else:
                                        print(_("下一发是：空弹"))
                            if ctnl:
                                ctnl = False
                                continue
                        if player.shoot(): # 想射#TODO
                            if b:
                                print(_("砰！！！"))
                                dealer.hurt() # 受伤
                                if playerknife:
                                    dealer.hurt() # 受伤
                            else:
                                print(_("咔......"))
                            if not dealercuff:next = 1
                            else:dealercuff = False
                        else:
                            if b:
                                print(_("砰！！！"))
                                player.hurt()
                                if playerknife:
                                    player.hurt()
                                if not dealercuff:next = 1
                                else:dealercuff = False
                            else:
                                print(_("咔......"))
                    else:
                        if j:
                            while True:
                                useprop = dealer.useprop()
                                if useprop == 0:
                                    break
                                elif useprop == 1: # 啤酒
                                    print(_("恶魔正在使用：啤酒"))
                                    if b:
                                        print(_("下一发是：实弹"))
                                    else:
                                        print(_("下一发是：空弹"))
                                    ctnl = True
                                    break
                                elif useprop == 2: # 烟
                                    print(_("恶魔正在使用：烟"))
                                    dealer.smoke()
                                elif useprop == 3:
                                    print(_("恶魔正在使用：手铐"))
                                    playercuff = True
                                elif useprop == 4:
                                    print(_("恶魔正在使用：小刀"))
                                    dealerknife = True
                                else:
                                    print(_("恶魔正在使用：放大镜")) # TODO
                                    print(_("恶魔:非常有趣。。。"))
                            if ctnl:
                                ctnl = False
                                continue
                        if dealerknife:
                            print(_("恶魔选择向你开枪！！！"))
                            if b:
                                print(_("砰！！！"))
                                player.hurt()
                                player.hurt()
                            else:
                                print(_("咔......"))
                            if not playercuff:next = 0
                            else:playercuff = False
                            dealerknife = False
                        else:
                            if dealer.shoot():
                                print(_("恶魔选择向你开枪！！！"))
                                if b:
                                    print(_("砰！！！"))
                                    player.hurt()
                                else:
                                    print(_("咔......"))
                                if not playercuff:next = 0
                                else:playercuff = False
                            else:
                                print(_("恶魔选择向自己开枪......"))
                                if b:
                                    print(_("砰！！！"))
                                    dealer.hurt()
                                    if not playercuff:next = 0
                                    else:playercuff = False
                                else:
                                    print(_("咔......"))
                    playerknife = False
                    sleep(1)
                    if dealer.gethealth() == 0:
                        print("恶魔死了！！！")
                        brk = True
                        break
                    if player.gethealth() == 0:
                        print(f"{name}死了！！！")
                        raise SystemExit
            del dealer
            del player
    except KeyboardInterrupt:pass