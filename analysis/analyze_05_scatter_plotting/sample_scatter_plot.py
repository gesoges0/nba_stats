import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def imscatter(x, y, image_path, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image_path = plt.imread(image_path)
    except TypeError:
        pass
    im = OffsetImage(image_path, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x_, y_ in zip(x, y):  # 画像の配列 imgsを作って, ここを zip(x, y, imgs)にすれば行けそう
        ab = AnnotationBbox(im, (x_, y_), xycoords="data", frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists


if __name__ == '__main__':
    x, y = np.random.rand(2, 20)  # (2, 20) の行列
    image_path = "cactus5.png"  # plotする画像のimage
    fig, ax = plt.subplots()  # グラフ宣言
    imscatter(x, y, image_path, ax=ax, zoom=0.1)  # 散布図, zoomはplot画像の倍率
    ax.plot(x, y, "ko", alpha=0)
    plt.savefig("cactus_plot.png", dpi=200, transparent=False)
    plt.show()
