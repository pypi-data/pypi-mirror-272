"""
This module provides a class for creating microarray visualizations of
dataframes, representing occurrences of specific words in scientific literature
as processed and analyzed by the PDFMicroarray class.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class PlotMicroarray:
    """
    A class designed to generate microarray visualizations of pandas
    dataframes, displaying the results from text analysis of PDF documents.
    """

    @classmethod
    def plot(
        cls,
        data_path,
        image_path=None,
        threshold=90,
        empty=False,
        split=60,
        width=60,
        height=30,
    ):
        """
        Plots one or multiple microarrays of the provided dataframe using a
        predefined color palette.

        Args:
            data_path (str): Path to the CSV file containing data to plot.
            image_path (str, optional): If provided, the plot will be saved
            to this path. Otherwise, the plot will be shown directly.
            Defaults to None.
            threshold (int): Minimum Levenshtein distance score (0-100) to
            consider a match. Defaults to 90.
            empty (bool): If True, shows rows with no values. Defaults to
            False.
            width (int): Width of the figure in inches. Defaults to 60.
            height (int): Height of the figure in inches. Defaults to 30.
            split (int, optional): Maximum number of rows each plot should
            have. Defaults to 60.
        """

        df = pd.read_csv(data_path, index_col=0, dtype={0: str})
        df = (df >= threshold).astype(int)

        if not empty:
            df = df.loc[~(df == 0).all(axis=1)]

        split_dfs = cls._split_dataframe(df, split)
        if len(split_dfs) > 1:
            for idx, split_df in enumerate(split_dfs):
                if image_path:
                    img_base, img_ext = os.path.splitext(image_path)
                    split_path = f"{img_base}_{idx+1}{img_ext}"
                else:
                    split_path = None
                cls._plot_dataframe(split_df, split_path, width, height)
        else:
            cls._plot_dataframe(df, image_path, width, height)

    @classmethod
    def _split_dataframe(cls, df, split):
        number_of_splits = (len(df) + split - 1) // split
        split_dfs = []
        for idx in range(number_of_splits):
            start_row = idx * split
            end_row = min(start_row + split, len(df))

            split_df = df.iloc[start_row:end_row]
            split_dfs.append(split_df)

        return split_dfs

    @classmethod
    def _plot_dataframe(cls, df, image_path, width, height):
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["font.size"] = "9"
        plt.rcParams["figure.figsize"] = (width, height)

        cmap = sns.color_palette(["white", "cornflowerblue"], as_cmap=True)
        ax = sns.heatmap(
            df, annot=False, cmap=cmap, cbar=False, linewidths=5, square=True
        )

        line_color = "lightgrey"
        line_width = 0.5

        num_rows, num_cols = df.shape
        for idx in range(1, num_rows):
            plt.axhline(idx, color=line_color, lw=line_width)
        for idx in range(1, num_cols):
            plt.axvline(idx, color=line_color, lw=line_width)

        plt.axhline(0, color=line_color, lw=line_width)
        plt.axhline(num_rows, color=line_color, lw=line_width)
        plt.axvline(0, color=line_color, lw=line_width)
        plt.axvline(num_cols, color=line_color, lw=line_width)

        ax.xaxis.tick_top()
        ax.tick_params(top=False)
        ax.tick_params(left=False)
        ax.set_xticklabels(
            ax.get_xticklabels(), rotation=90, horizontalalignment="center"
        )

        plt.tight_layout()

        if not image_path:
            plt.show()
        else:
            plt.savefig(image_path, dpi=300, bbox_inches="tight")

        plt.close()
