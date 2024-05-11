from locale import getdefaultlocale as lcl,setlocale as stlcl,LC_ALL
from gettext import translation
from random import shuffle
from time import sleep
import pygame
from copy import copy
from os.path import dirname
from sys import path
#import treading
#treading.Tread() # TODO
path.append(dirname(__file__))
# 模块导入
from data import *
from sprites import *

stlcl(LC_ALL,"")
lang, _ = lcl()
trans = translation("trans",LOCALE,languages=[lang],fallback=True)
_ = trans.gettext

def setprop(beset,value,prop):
    beset.setprop(value)
    prop.append(value)
    return prop

def makeprop(beset,value):
    prp = []
    for i in range(value):
        rdm = random()
        if rdm <= 0.2: # 啤酒
            prp = setprop(beset,"beer",prp)
        elif rdm <= 0.4: # 烟
            prp = setprop(beset,"smoke",prp)
        elif rdm <= 0.6: # 手铐
            prp = setprop(beset,"handcuff",prp)
        elif rdm <= 0.8: # 小刀
            prp = setprop(beset,"knife",prp)
        else:
            prp = setprop(beset,"magnifier",prp)
    return prp

def run(FPS = 15,CHEAT = False):
    try:
        pygame.init()
        # 以下是一些关于pygame的一些常量声明
        # 以下是初始化
        clock = pygame.time.Clock() # 初始化时钟
        screen = pygame.display.set_mode((1400,850)) # 屏幕（窗口）初始化
        pygame.display.set_caption("Bullet Roulette") # 设置标题
        text = pygame.font.Font(FONT,75) # 设定字体
        background    = pygame.image.load(BACKGROUND) # 加载背景图
        gunimage      = pygame.image.load(GUN) # 加载霰弹枪图片
        charge        = pygame.image.load(CHARGE) # 加载血量图片
        blank         = pygame.image.load(BLANK) # 加载空弹图片
        liveround     = pygame.image.load(LIVEROUND) # 加载实弹图片
        shootself     = pygame.image.load(SHOOTSELF) # 加载恶魔射击自己时的图片
        shootplayer   = pygame.image.load(SHOOTPLAYER) # 加载恶魔射击玩家时的图片
        smoke         = pygame.image.load(SMOKE) # 加载烟的图片
        magnifier     = pygame.image.load(MAGNIFIER) # 加载放大镜图片
        knife         = pygame.image.load(KNIFE) # 加载刀的图片
        handcuff      = pygame.image.load(HANDCUFF) # 加载手铐图片
        beer          = pygame.image.load(BEER) # 加载啤酒图片
        propbox       = pygame.image.load(PROPBOX) # 加载道具盒图片
        usesmoke      = pygame.image.load(USESMOKE) # 加载玩家使用烟时的图片
        usemagnifier  = pygame.image.load(USEMAGNIFIER) # 加载玩家使用放大镜时的图片
        usehandcuff   = pygame.image.load(USEHANDCUFF) # 加载玩家使用手铐时的图片
        usebeer       = pygame.image.load(USEBEER) # 加载玩家使用啤酒时的图片
        useknife      = pygame.image.load(USEKNIFE) # 加载玩家使用刀时的图片
        seeblank      = pygame.image.load(SEEBLANK) # 加载玩家使用放大镜看到空弹时的图片
        seeliveround  = pygame.image.load(SEELIVEROUND) # 加载玩家使用放大镜看到实弹时的图片
        dusesmoke     = pygame.image.load(DUSESMOKE) # 加载玩家使用烟时的图片
        dusemagnifier = pygame.image.load(DUSEMAGNIFIER) # 加载玩家使用放大镜时的图片
        dusehandcuff  = pygame.image.load(DUSEHANDCUFF) # 加载玩家使用手铐时的图片
        dusebeer      = pygame.image.load(DUSEBEER) # 加载玩家使用啤酒时的图片
        duseknife     = pygame.image.load(DUSEKNIFE) # 加载玩家使用刀时的图片
        nametext = text.render(_("输入名字："),True,WHITE) # 用字体生成文字
        playerlose = text.render(_("恶魔赢了！"),True,WHITE) # 用字体生成文字
        interestingtext = text.render(_("恶魔：非常有趣"),True,WHITE)
        shootdealer = Button(700,75,text.render(_("恶魔"),True,WHITE),1)
        dealerturntext = text.render(_("恶魔的回合"),True,WHITE)
        buckshottext = text.render(_("子弹："),True,WHITE)
        uselocation = usebeer.get_rect() # 获取使用道具的图片的位置
        seelocation = seeblank.get_rect()
        propboxlocation = propbox.get_rect()
        buckshotlocation = blank.get_rect() # 获取子弹显示位置
        shootlocation = shootself.get_rect() # 获取恶魔射击时的位置
        chargelocation = charge.get_rect() # 获取血量显示位置
        buckshottextlocation = buckshottext.get_rect()
        nametextlocation = nametext.get_rect()
        interestingtextlocation = interestingtext.get_rect()
        loseorwinlocation = playerlose.get_rect()
        seelocation.top = 0
        seelocation.centerx = 700
        uselocation.centerx = 700
        uselocation.bottom = 850 # 将使用道具的图片的位置的底边修改为700,850
        propboxbutton = Button(700,700,propbox,1)
        noneprop     = copy(knife)
        noneprop.set_alpha(0)
        proplocation = []
        propbuttons = []
        dproplocation = []
        for i in range(8):
            proplocation.append(pygame.Rect((100*(i+1)+200,425,50,100)))
        for i in range(8):
            propbuttons.append(Button(100*(i+1)+200,425,noneprop))
        for i in range(8):
            dproplocation.append(pygame.Rect((100*(i+1)+200,25,50,100)))
        gunimage.set_alpha(0) # 完全透明（此图是为了绘制边框）
        gun = Button(675,300,gunimage,1) # 加载按钮（Button类的定义在sprites.py)
        pygame.mixer.music.load(BGM) # 加载背景音乐（BGM）
        liveplayermusic = pygame.mixer.Sound(LIVEPLAYER) # 玩家被击中时的音效
        livedealermusic = pygame.mixer.Sound(LIVEDEALER) # 恶魔被击中时的音效
        blankmusic = pygame.mixer.Sound(BLANKMUSIC) # 空弹发射时的音效
        shootlocation.center = (700,300) # 设置恶魔射击时的位置
        interestingtextlocation.center = (700,600)
        loseorwinlocation.center = (700,425)
        propboxlocation.center = (700,700)
        nametextlocation.center = (700,100)
        buckshottextlocation.topleft = (100,75)
        dealerturntextlocation = copy(nametextlocation)
        dealerturntextlocation.topright = (1400,0)
        buttons = []
        name = ""
        for i in range(26):buttons.append(Button(50*(i+1),700,pygame.image.load(LETTERSPATH[i])))
        delete = Button(350,760,pygame.image.load(DELETE))
        enter = Button(800,760,pygame.image.load(ENTER))
        pygame.mixer.music.play(-1) # 循环播放音乐
        # 以下是一些控制变量
        first = True
        naming = True # 正在命名
        playerturn = False # 玩家回合
        dealerturn = False # 恶魔回合
        choosing = False # 玩家正在选择射击谁
        drawingbullets = False # 正在显示子弹和抽取道具
        selectingprop = True # 隶属于drawingbullets，正在选择道具（还没有点击道具盒）
        playercuff = False
        dealercuff = False
        playerknife = False
        dealerknife = False
        tmppropplayer = [] # 玩家当前将要抽取的道具
        propdealer = []
        propplayer = [None,None,None,None,None,None,None,None] # 玩家已经抽取的道具
        buckshot = [] # 当前小轮的子弹
        turn = [0,0] # 记录回合[大轮，小轮]
        dealer = Dealer(2) # 初始化Dealer类
        player = Player(2,name) # 初始化Player类
        count = 0
        while True: # 游戏主循环
            count += 1
            if CHEAT and count == FPS:
                count = 0
                print("Bullets:",buckshot)
            for event in pygame.event.get(): # 事件处理循环
                if event.type == pygame.QUIT: # QUIT处理
                    raise SystemExit # 退出(等同于exit())
            screen.blit(background,(0,0)) # 粘贴背景图片
            if player.gethealth() <= 0: # 玩家死亡
                screen.blit(playerlose,loseorwinlocation) # 打印玩家死亡提示
                pygame.display.update() # 更新画面
                sleep(2) # 停留2秒
                raise SystemExit # 退出
            if dealer.gethealth() <= 0: # 恶魔死亡
                turn[1] = 0 # 初始化小轮
                turn[0] += 1 # 大轮+1
                propplayer = [None,None,None,None,None,None,None,None]
                propdealer = []
                buckshot = [] # 初始化子弹
                screen.blit(playerwin,loseorwinlocation) # 打印恶魔死亡提示
                pygame.display.update() # 更新画面
                sleep(2) # 停留2秒
                if turn[0] == 3: # 超出3轮
                    raise SystemExit # 退出
                else:
                    dealer = Dealer(HEALTH[turn[0]]) # 初始化Dealer类
                    player = Player(HEALTH[turn[0]],name) # 初始化Player类
                    dealer.noprop()
            if not buckshot:
                buckshot = BULLETS[turn[0]][turn[1]]
                turn[1] += 1
                if turn[0]:
                    savepropdaler = copy(propdealer)
                    tmppropdealer = makeprop(dealer,HEALTH[turn[0] - 1])
                    propdealer = copy(savepropdaler)
                    propdealer.extend(tmppropdealer)
                    dealer.noprop(False)
                    propdealer = dealer.getprop()
                    tmppropplayer = makeprop(player,HEALTH[turn[0] - 1])
                if not naming:
                    playerturn = dealerturn = False
                    drawingbullets = True
            if naming:
                screen.blit(nametext,nametextlocation)
                for i in buttons: 
                    if i.run(screen):
                        name += (LETTERS[buttons.index(i)])
                if delete.run(screen):
                    name = name[:-1]
                if enter.run(screen):
                    naming = False
                    drawingbullets = True
                    shootyou = Button(700,700,text.render(name,False,WHITE),1)
                    playerwin = text.render(f"{name} 赢了！",False,WHITE)
                    player.setname(name)
                tmpnametext = text.render(name,False,WHITE)
                tmpnametextlocation = tmpnametext.get_rect()
                tmpnametextlocation.center = (700,400)
                screen.blit(tmpnametext,tmpnametextlocation)
            elif playerturn:
                for i in range(player.gethealth()):
                    chargelocation.bottomleft = (0,850-50*i)
                    screen.blit(charge,chargelocation)
                for i in range(dealer.gethealth()):
                    chargelocation.topleft = (0,0+50*i)
                    screen.blit(charge,chargelocation)
                for en,i in enumerate(propdealer):
                    screen.blit(eval(i),dproplocation[en])
                for en,i in enumerate(propplayer):
                    if i:
                        screen.blit(eval(i),proplocation[en])
                        if propbuttons[en].run(screen):
                            if i == "magnifier":screen.blit(usemagnifier,(600,620))
                            else:screen.blit(eval("use" + i),uselocation)
                            if i == "beer":
                                if buckshot[0]:
                                    screen.blit(liveround,(650,0))
                                else:
                                    screen.blit(blank,(650,0))
                                del buckshot[0]
                            elif i == "knife":
                                playerknife = True
                            elif i == "smoke":
                                player.smoke()
                            elif i == "handcuff":
                                dealercuff = True
                            else:
                                if buckshot[0]:
                                    screen.blit(seeliveround,seelocation)
                                else:
                                    screen.blit(seeblank,seelocation)
                            propplayer[en] = None
                            pygame.display.update()
                            sleep(2)
                if gun.run(screen):
                    playerturn = False
                    choosing = True
            elif dealerturn:
                screen.blit(dealerturntext,dealerturntextlocation)
                for i in range(player.gethealth()):
                    chargelocation.bottomleft = (0,850-50*i)
                    screen.blit(charge,chargelocation)
                for i in range(dealer.gethealth()):
                    chargelocation.topleft = (0,0+50*i)
                    screen.blit(charge,chargelocation)
                for en,i in enumerate(propdealer):
                    screen.blit(eval(i),dproplocation[en])
                for en,i in enumerate(propplayer):
                    if i:screen.blit(eval(i),proplocation[en])
                pygame.display.update()
                sleep(1)
                while True:
                    if not dealer.getprop():break
                    useprop = dealer.useprop()
                    if useprop == 0:
                        break
                    elif useprop == 1: # 啤酒
                        screen.blit(dusebeer,seelocation)
                        if buckshot[0]:
                            screen.blit(liveround,uselocation)
                        else:
                            screen.blit(blank,uselocation)
                        del buckshot[0]
                    elif useprop == 2: # 烟
                        screen.blit(dusesmoke,seelocation)
                        dealer.smoke()
                    elif useprop == 3:
                        screen.blit(dusehandcuff,seelocation)
                        playercuff = True
                    elif useprop == 4:
                        screen.blit(duseknife,seelocation)
                        dealerknife = True
                    else:
                        screen.blit(dusemagnifier,seelocation)
                        if buckshot[0]:
                            dealer.memory(1)
                        else:
                            dealer.memory(0)
                        screen.blit(interestingtext,interestingtextlocation)
                    propdealer = dealer.getprop()
                    pygame.display.update()
                    sleep(2)
                    screen.blit(background,(0,0))
                    screen.blit(dealerturntext,dealerturntextlocation)
                    for i in range(player.gethealth()):
                        chargelocation.bottomleft = (0,850-50*i)
                        screen.blit(charge,chargelocation)
                    for i in range(dealer.gethealth()):
                        chargelocation.topleft = (0,0+50*i)
                        screen.blit(charge,chargelocation)
                    for en,i in enumerate(propdealer):
                        screen.blit(eval(i),dproplocation[en])
                    for en,i in enumerate(propplayer):
                        if i:screen.blit(eval(i),proplocation[en])
                    pygame.display.update()
                    sleep(1)
                if buckshot:
                    if dealer.shoot() == 0:
                        screen.blit(shootself,shootlocation)
                        if buckshot[0]:
                            livedealermusic.play()
                            dealer.hurt()
                            if not playercuff:
                                dealerturn = False
                                playerturn = True
                            else:playercuff = False
                        else:
                            blankmusic.play()
                    else:
                        screen.blit(shootplayer,shootlocation)
                        if buckshot[0]:
                            liveplayermusic.play()
                            if dealerknife:
                                player.hurt()
                            player.hurt()
                        else:
                            blankmusic.play()
                        if not playercuff:
                            dealerturn = False
                            playerturn = True
                        else: playercuff = False
                    print("deling",buckshot)
                    del buckshot[0]
                    pygame.display.update()
                    sleep(2)
                else:pass
            elif choosing:
                for i in range(player.gethealth()):
                    chargelocation.bottomleft = (0,850-50*i)
                    screen.blit(charge,chargelocation)
                for i in range(dealer.gethealth()):
                    chargelocation.topleft = (0,0+50*i)
                    screen.blit(charge,chargelocation)
                if shootdealer.run(screen):
                    choosing = False
                    if dealercuff:
                        playerturn = True
                        dealercuff = False
                    else:
                        dealerturn = True
                    if buckshot[0] == 0:
                        blankmusic.play()
                    else:
                        livedealermusic.play()
                        dealer.hurt()
                        if playerknife:
                            dealer.hurt()
                    del buckshot[0]
                    playerknife = False
                    sleep(2)
                elif shootyou.run(screen):
                    choosing = False
                    if buckshot[0] == 0:
                        blankmusic.play()
                        playerturn = True
                    else:
                        liveplayermusic.play()
                        player.hurt()
                        if playerknife:
                            player.hurt()
                        if dealercuff:
                            playerturn = True
                            dealercuff = False
                        else:
                            dealerturn = True
                    del buckshot[0]
                    playerknife = False
                    sleep(2)
            elif drawingbullets:
                pygame.draw.rect(screen,RED,(0,0,1400,250))
                screen.blit(buckshottext,buckshottextlocation)
                for en,b in enumerate(buckshot):
                    buckshotlocation.topleft = (600+80 * en,75)
                    if b:
                        screen.blit(liveround,buckshotlocation)
                    else:
                        screen.blit(blank,buckshotlocation)
                for en,p in enumerate(propplayer):
                    if p:
                        screen.blit(eval(p),proplocation[en])
                if tmppropplayer:
                    screen.blit(propbox,propboxlocation)
                    first = False
                    if selectingprop:
                        if propboxbutton.run(screen):
                            selectingprop = False
                    else:
                        screen.blit(eval(tmppropplayer[0]),propboxlocation)
                        for en,p in enumerate(propbuttons):
                            if not propplayer[en] and p.run(screen):
                                selectingprop = True
                                propplayer[en] = tmppropplayer[0]
                                del tmppropplayer[0]
                else:
                    if first:
                        pygame.display.update()
                        sleep(2)
                    else:
                        first = True
                    drawingbullets = False
                    playerturn = True
                    shuffle(buckshot)
                    dealer.setbullet(copy(buckshot))
 #           else:
#                raise TypeError("Nothing is Running!!!")
            pygame.display.update()
            clock.tick(FPS)
    except KeyboardInterrupt:pass
    except SystemExit:pass
    pygame.quit()