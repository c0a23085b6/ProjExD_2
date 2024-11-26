import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650  # ウィンドウの幅と高さ
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}  # キー入力に対する移動量の辞書

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # カレントディレクトリの移動

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:  # 画面内かどうかを判定
    """
    引数：こうかとん または 爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True  # 画面内かどうかの初期値
    if obj_rct.left < 0 or WIDTH < obj_rct.right:  # 画面外に出たら  
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  # 画面外に出たら
        tate = False
    return yoko, tate  # 画面内かどうかを返す

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


def  create_bomb_images_and_accs() -> tuple[list[pg.Surface], list[int]]:  
    """
    爆弾の拡大サーフェスと加速度のリストを返す
    """
    bb_imgs = []  
    bb_accs = [a for a in range(1, 11)]  # 加速度リスト（1から10まで）
    
    for r in range(1, 11):  # 1から10までの拡大率でサーフェスを生成
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)  # 透過度を設定
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 円を描画
        bb_imgs.append(bb_img)  # サーフェスをリストに追加
    
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")  # ウィンドウタイトル
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ゲーム画面の生成
    bg_img = pg.image.load("fig/pg_bg.jpg")  # 背景画像のロード
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # こうかとんの画像をロード
    kk_rct = kk_img.get_rect()  # こうかとんのRectを取得
    kk_rct.center = 300, 200   # こうかとんの初期位置
    
    # 爆弾の拡大サーフェスと加速度を生成
    bb_imgs, bb_accs = create_bomb_images_and_accs()
    
    bb_rct = bb_imgs[0].get_rect()  # 爆弾のRectを取得
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 爆弾の初期位置
    
    vx, vy = +5, -5
    gob_img = pg.Surface((1100, 650))  # ゲームオーバー画面のサーフェス
    gob_img.set_alpha(128)  # 透過度を設定
    pg.draw.rect(gob_img, (0, 0, 0), pg.Rect(0, 0, 800, 1600))  # 黒い四角形を描画
    fonto = pg.font.Font(None, 80)  # フォントの設定
    txt = fonto.render("GameOver", True, (255, 255, 255))  # テキストの設定
    cry_kk_img = pg.image.load("fig/8.png")  # 泣いているこうかとんの画像

    clock = pg.time.Clock()  # クロックオブジェクトの生成
    tmr = 0  # タイマーの初期化

    while True:  # ゲームループ
        for event in pg.event.get():  # イベント処理
            if event.type == pg.QUIT:   # ウィンドウの閉じるボタンが押されたら
                return  # ゲーム終了

        screen.blit(bg_img, [0, 0])  # 背景画像の描画

        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が重なっていたら
            game_over(screen)
            break

        # tmrに応じて爆弾のサイズと加速度を選択
        idx = min(tmr // 500, 9)  # 500フレームごとに段階を上げる（最大9段階）
        bb_img = bb_imgs[idx]  # 爆弾のサイズ変更
        avx = vx * bb_accs[idx]  # 爆弾の加速度変更
        avy = vy * bb_accs[idx]  # 爆弾の加速度変更

        key_lst = pg.key.get_pressed()  # キー入力のリストを取得
        sum_mv = [0, 0]  # こうかとんの移動量の初期化
        for key, tpl in DELTA.items():  # DELTAのキーと値を取り出す
            if key_lst[key]:  # キーが押されていたら
                sum_mv[0] += tpl[0]  # 横移動量を加算
                sum_mv[1] += tpl[1]  # 縦移動量を加算
        kk_rct.move_ip(sum_mv)  # こうかとんのRectを移動
        if check_bound(kk_rct) != (True, True):  # 画面外に出たら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 移動を戻す
        screen.blit(kk_img, kk_rct)  # こうかとんの画像を描画

        bb_rct.move_ip(avx, avy)  # 爆弾のRectを移動
        yoko, tate = check_bound(bb_rct)  # 画面内かどうかを判定
        if not yoko:  # 横方向に画面外に出たら
            vx *= -1  # 逆方向に移動
        if not tate:  # 縦方向に画面外に出たら
            vy *= -1  # 逆方向に移動
        screen.blit(bb_img, bb_rct)  # 爆弾の画像を
        pg.display.update()  # 画面を更新
        tmr += 1  # タイマーをカウント
        clock.tick(50)  # フレームレートを設定

if __name__ == "__main__":  # このファイルが直接実行されたら
    pg.init()    # Pygameの初期化
    main()     # メイン関数の実行
    pg.quit()  # Pygameの終了
    sys.exit()  # システム終了