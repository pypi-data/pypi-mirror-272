# 此文件用于定义各种常量。
from os.path import dirname

ASSESTS       = f"{dirname(__file__)}/assets/" # 存放图片背景音乐等素材的目录
LOCALE        = f"{dirname(__file__)}/locale/" # 存放翻译文件的路径
RED           = (255,  0,  0) # 红色RGB
WHITE         = (255,255,255) # 白色RGB
BACKGROUND    = f"{ASSESTS}bg.png" # 背景图
BGM           = f"{ASSESTS}bgmsc.ogg" # 背景音乐
FONT          = f"{ASSESTS}Simhei.ttf" # 字体
LETTERS       = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z") # 字母表
DELETE        = f"{ASSESTS}DELETE.png" # DELETE键
ENTER         = f"{ASSESTS}ENTER.png" # ENTER键
CHARGE        = f"{ASSESTS}charge.png" # 电量
GUN           = f"{ASSESTS}gun.png" # 枪（轮廓）
BLANKMUSIC    = f"{ASSESTS}blank.wav" # 射出空弹音效
LIVEDEALER    = f"{ASSESTS}livedealer.wav" # 大哥被打到时的音效
LIVEPLAYER    = f"{ASSESTS}liveplayer.wav" # 玩家被打到时的音效
BLANK         = f"{ASSESTS}blank.png" # 空弹
LIVEROUND     = f"{ASSESTS}liveround.png" # 实弹
SHOOTSELF     = f"{ASSESTS}dealershootself.png" # 大哥紫砂
SHOOTPLAYER   = f"{ASSESTS}dealershootplayer.png" # 大哥打玩家
SMOKE         = f"{ASSESTS}smoke.png"
HANDCUFF      = f"{ASSESTS}handcuff.png"
MAGNIFIER     = f"{ASSESTS}magnifier.png"
KNIFE         = f"{ASSESTS}knife.png"
PROPBOX       = f"{ASSESTS}propbox.png"
BEER          = f"{ASSESTS}beer.png"
PILL          = f"{ASSESTS}pill.png"
NONEPROP      = f"{ASSESTS}noneprop.png"
USESMOKE      = f"{ASSESTS}usesmoke.png"
USEKNIFE      = f"{ASSESTS}useknife.png"
USEHANDCUFF   = f"{ASSESTS}usehandcuff.png"
USEBEER       = f"{ASSESTS}usebeer.png"
USEMAGNIFIER  = f"{ASSESTS}usemagnifier.png"
DUSESMOKE     = f"{ASSESTS}dusesmoke.png"
DUSEKNIFE     = f"{ASSESTS}duseknife.png"
DUSEHANDCUFF  = f"{ASSESTS}dusehandcuff.png"
DUSEBEER      = f"{ASSESTS}dusebeer.png"
DUSEMAGNIFIER = f"{ASSESTS}dusemagnifier.png"
SEEBLANK      = f"{ASSESTS}seeblank.png"
SEELIVEROUND  = f"{ASSESTS}seeliveround.png"
BOOM          = f"{ASSESTS}boom.png"
HEALTH        = (2,4,6)
BULLETS = [ # 子弹（1代表实，0代表空）
        [
            [1,0,0],
            [1,1,0,0]
        ],
        [
            [1,0],
            [1,1,0,0,0],
            [1,1,1,0,0,0],
            [1,1,1,1,0,0,0,0]
        ],
        [
            [1,1,1,1,1,0,0,0],
            [1,1,1,1,0,0,0,0],
            [1,1,1,1,1,1,0,0],
            [1,1,1,1,0,0,0,0],
            [1,1,0,0,0,0,0,0]
        ]
    ]
LETTERSPATH = [ASSESTS + l + ".png" for l in LETTERS]