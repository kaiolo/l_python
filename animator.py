import matplotlib.pyplot as plt
import imageio
import numpy as np
from io import BytesIO

class AnimatorGif:
    def __init__(self, xlabel=None, ylabel=None, legend=None, xlim=None,
                 ylim=None, xscale='linear', yscale='linear',
                 fmts=('-', 'm--', 'g-.', 'r:'), figsize=(3.5, 2.5), dpi=120):
        if legend is None:
            legend = []
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.legend = legend
        self.xlim = xlim
        self.ylim = ylim
        self.xscale = xscale
        self.yscale = yscale
        self.fmts = fmts
        self.X = None
        self.Y = None
        self.frames = []
        self.figsize = figsize
        self.dpi = dpi

    def add(self, x, y):
        if not hasattr(y, "__len__"):
            y = [y]
        n = len(y)
        if not hasattr(x, "__len__"):
            x = [x] * n
        if self.X is None:
            self.X = [[] for _ in range(n)]
        if self.Y is None:
            self.Y = [[] for _ in range(n)]
        for i, (a, b) in enumerate(zip(x, y)):
            if a is not None and b is not None:
                self.X[i].append(a)
                self.Y[i].append(b)

        # 固定画布，禁止自动裁剪！！
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        for xd, yd, fmt in zip(self.X, self.Y, self.fmts):
            ax.plot(xd, yd, fmt)

        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_xscale(self.xscale)
        ax.set_yscale(self.yscale)
        if self.xlim:
            ax.set_xlim(self.xlim)
        if self.ylim:
            ax.set_ylim(self.ylim)
        if self.legend:
            ax.legend(self.legend)
        ax.grid()

        buf = BytesIO()
        # 重点：去掉 bbox_inches="tight"，否则尺寸漂移
        plt.savefig(buf, format='png', dpi=self.dpi)
        buf.seek(0)

        # 直接读图片字节，转numpy数组
        im = plt.imread(buf)
        self.frames.append((im * 255).astype(np.uint8))
        plt.close(fig)

    def save_gif(self, path="train.gif", duration=0.2):
        # 校验所有帧shape一致（调试用）
        shapes = {f.shape for f in self.frames}
        if len(shapes) > 1:
            raise RuntimeError(f"帧尺寸不统一！各帧shape：{shapes}")
        imageio.mimsave(path, self.frames, duration=duration)
        print(f"✅ gif已保存至 {path}")


# --------测试示例 可直接运行--------
if __name__ == "__main__":
    animator = AnimatorGif(xlabel="epoch", ylabel="loss", legend=["train loss"])
    for i in range(20):
        loss = 5/(i+1) + 0.1*np.random.randn()
        animator.add(i, loss)
    animator.save_gif("loss_curve.gif")
