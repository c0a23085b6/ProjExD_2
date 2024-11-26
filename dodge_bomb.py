import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

"""
引数で与えられたRectが画面内に収まっているかどうかを判定する関数
引数：こうかとんRect or 爆弾Rect
戻り値：True(画面内に収まっている) or False(画面外に出ている)
"""

def check_bound(rct):
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def game_over(screen):
    """
    ゲームオーバー画面を表示する。
    画面をブラックアウトし、「Game Over」を表示し、
    泣いているこうかとん画像を貼り付ける。

    Args:
        screen (pg.Surface): ゲーム画面Surface。
        kk_rct (pg.Rect): こうかとんの位置情報Rect。
    """
    # 半透明の黒い背景を作成
    black_screen = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))  # RGBA: 半透明
    black_screen.set_alpha(200)  # 透過度を設定
    screen.blit(black_screen, (0, 0)) # ブラックアウト画面の描画

    # 「Game Over」の文字を作成
    font = pg.font.Font(None, 80)  # フォントサイズ80
    text = font.render("Game Over", True, (255, 255, 255))  # 白文字
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 25 ))  # 画面中央に配置

    # 泣いているこうかとん画像の描画
    kk_crying_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_crying_rct = kk_crying_img.get_rect()
    kk_crying_rct.center = WIDTH // 2 + 200, HEIGHT // 2 + 2
    screen.blit(kk_crying_img, kk_crying_rct)
    kk_crying_rct.center = WIDTH // 2 - 200, HEIGHT // 2 
    screen.blit(kk_crying_img, kk_crying_rct)

    # 画面を更新して5秒間停止
    pg.display.update()
    time.sleep(5)
    return


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #爆弾用の空surface
    pg.draw.circle(bb_img, (255, 0, 0), (10,10), 10) #爆弾円を描く
    bb_img.set_colorkey(0, 0)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            break #爆弾に当たったらゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        
        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外に出ないようにする
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx, vy) #爆弾を動かす
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1 #左右の壁に当たったら逆方向に動かす
        if not tate:
            vy *= -1 #上下の壁に当たったら逆方向に動かす
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
