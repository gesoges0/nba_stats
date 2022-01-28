import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

working_dir = Path('X:\\Adobe\\PremierePro\\images\\player_images_20220128')


def imscatter(x, y, image_paths, labels=None, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    x, y = np.atleast_1d(x, y)
    artists = []
    for x_, y_, img_path, label_ in zip(x, y, image_paths, labels):  # 画像の配列 imgsを作って, ここを zip(x, y, imgs)にすれば行けそう
        plt_img = plt.imread(str(img_path))
        im = OffsetImage(plt_img, zoom=zoom)
        ab = AnnotationBbox(im, (x_, y_), xycoords="data", frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists


if __name__ == '__main__':
    # tsvを読み込む
    # player_id, minutes, net_rtg
    tsv_path = 'result_2022_01_28.tsv'
    df = pd.read_csv(tsv_path, sep='\t', header=None, names=('player_id', 'player_name', 'minutes', 'net_rtg', 'img_url'))
    # player_ids, player_names, minutess, net_rtgs = df[['player_id', 'player_name', 'minutes', 'net_rtg']]
    player_ids = df['player_id']
    player_names = df['player_name']
    minutes = df['minutes']
    net_rtg = df['net_rtg']

    # 画像を読み込む
    vfunc = np.vectorize(lambda x: working_dir / f'{x}.png' if (working_dir / f'{x}.png').exists() else 0)
    player_imgs = vfunc(player_ids)

    # 画像が無いデータを消す
    minutes = minutes[np.where(player_imgs != 0, True, False)]
    net_rtg = net_rtg[np.where(player_imgs != 0, True, False)]
    player_names = player_names[np.where(player_imgs != 0, True, False)]
    player_imgs = player_imgs[np.where(player_imgs != 0, True, False)]

    # 座標の絞り込み
    # X軸は 500 < minutes < 1750
    # Y軸は-20 < net_rtg < + 20
    flags = (800 < minutes) & (minutes < 1750) & (-20 < net_rtg) & (net_rtg < 20)
    minutes = minutes[flags]
    net_rtg = net_rtg[flags]
    player_names = player_names[flags]
    player_imgs = player_imgs[flags]

    fig, ax = plt.subplots()  # グラフ宣言
    imscatter(minutes, net_rtg, player_imgs, labels=player_names, ax=ax, zoom=0.3)  # 散布図, zoomはplot画像の倍率
    ax.plot(minutes, net_rtg, "ko", alpha=0)
    ax.set_xlabel("minites played")
    ax.set_ylabel("net rating")
    plt.savefig("cactus_plot.png", dpi=600, transparent=False)
    plt.show()
