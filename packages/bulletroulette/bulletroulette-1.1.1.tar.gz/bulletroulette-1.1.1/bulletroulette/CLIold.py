# 外部导入
cannotuseGUI = False
from random import shuffle
from time import sleep
from os import chdir,path
from traceback import print_exc
from copy import copy
# 模块导入
from data import *
from sprites import *
# 以下是主程序
chdir(path.dirname(__file__))
health = (2,4,6)
buckshots = [ # 子弹（1代表实，0代表空）
        [
            [1,0,0],
            [1,1,0,0]
        ],
        [
            [1,0],
            [1,1,0,0,0],
            [1,1,1,1,0,0]
        ],
        [
            [1,1,1,1,1,0,0,0],
            [1,1,1,1,0,0,0,0],
            [1,1,1,0],
            [1,1,1,1,0,0,0,0]
        ]
    ]
def run(CHEAT = False):
    try:
        name = input("你的名字：") # 输入名字
        for j in range(3): # 三个回合
            dealer = Dealer(health[j]) # 恶魔初始化
            player = Player(health[j],name) # 玩家初始化
            for i in range(len(buckshots[j])): # 每一小轮
                buckshot = buckshots[j][i] # 初始化本轮子弹
                buckshotcount = [0,0] #子弹计数
                for k in buckshot: # 实弹
                    if k:buckshotcount[0]+=1
                for k in buckshot: # 空弹
                    if k == 0:buckshotcount[1]+=1
                next = 0 # 下一轮
                shuffle(buckshot) # 打乱子弹顺序
                dealer.setbullet(copy(buckshot))
                print(f"{buckshotcount[0]}发实弹，{buckshotcount[1]}发空弹") # 打印子弹提示
                for i in range(len(buckshot)): #
                    if CHEAT:
                        print("Bullets:",buckshot[i:])
                    print(f"恶魔血量:{dealer.gethealth()} {name}的血量:{player.gethealth()}")
                    if next == 0:
                        if player.shoot():
                            if buckshot[i]:
                                print("砰！！！")
                                dealer.hurt() # 受伤
                            else:
                                print("咔......")
                            next = 1
                        else:
                            if buckshot[i]:
                                print("砰！！！")
                                player.hurt()
                                next = 1
                            else:
                                print("咔......")
                    else:
                        if dealer.shoot():
                            print(f"恶魔选择向{name}开枪！！！")
                            if buckshot[i]:
                                print("砰！！！")
                                player.hurt()
                            else:
                                print("咔......")
                            next = 0
                        else:
                            print("恶魔选择向自己开枪......")
                            if buckshot[i]:
                                print("砰！！！")
                                dealer.hurt()
                                next = 0
                            else:
                                print("咔......")
                    if dealer.gethealth() == 0:
                        print("恶魔死了！！！")
                        break
                    if player.gethealth() == 0:
                        print(f"{name}死了！")
                        raise SystemExit
                    sleep(1.5)
            del dealer
            del player
    except KeyboardInterrupt:print("\n检测到^C")
    except SystemExit:pass
    except:
        print("抱歉，我们检测到了一个错误，这可能不是您造成的，但您无法继续进行游戏了")
        print("错误信息：")
        print_exc()
    print("游戏结束!")
    print("感谢您的游玩!")
    pygame.quit()