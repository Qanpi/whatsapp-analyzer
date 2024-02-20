from matplotlib import pyplot as plt
import numpy as np

class Visualizer:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.__i = 0  # index of current plot

        self.fig, self.axs = plt.subplots(rows, cols)

        # watermark
        self.fig.text(
            0.999,
            0.001,
            "Whatsapp Analyzer by Qanpi",
            horizontalalignment="right",
            verticalalignment="bottom",
            alpha=0.3,
            family="monospace",
            size=9,
        )

    def _ax(self) -> plt.Axes:
        ax = self.axs[self.__i // self.cols][self.__i % self.cols]
        self.__i += 1
        return ax

    def bar(self, labels, data, title=None, ylabel=None):
        ax = self._ax()

        ax.set_title(title)
        ax.grid(False, "major", "x")
        ax.set_ylabel(ylabel)

        if len(labels) >= 10:
            ax.tick_params(axis="x", rotation=55, labelsize=10)

        ax.bar(labels, data)

        return ax

    def line(self, labels, data, average=None, title=None):
        ax = self._ax()

        ax.set_title(title)

        if average is not None:
            ax.axhline(
                average, alpha=0.3, c="r", ls="dashed", label="average"
            )  # The average line

        if len(labels) > 5:
            labels = [
                label if i % 2 == 0 else "\n" + label for i, label in enumerate(labels)
            ]  # so that the ticks do not overlap

        ax.plot(labels, data, label="messages")  # The data itself

        return ax

    def heatmap(self, data, title=None, xlabels=None, ylabels=None):
        ax = self._ax()

        ax.set_xticks(np.arange(len(xlabels)))
        ax.set_yticks(np.arange(len(ylabels)))

        ax.set_xticklabels(xlabels)
        ax.set_yticklabels(ylabels)

        ax.tick_params(axis="x", rotation=85, labelsize=10)

        ax.set_title(title)
        # ax.grid()

        ax.imshow(data, cmap="Blues", norm=None)
