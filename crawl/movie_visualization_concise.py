from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd


DEFAULT_DATA_PATH = Path("crawl/movie_processed.csv")


def load_movie_data(data_path: Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """读取电影数据并添加电影年份字段。"""
    movie_data = pd.read_csv(data_path)
    movie_data["movie_year"] = movie_data["movie_data"].str[:4].astype(int)
    return movie_data


def count_movies_by_year(movie_data: pd.DataFrame) -> Tuple[list[int], list[int]]:
    """生成连续年份和每年的电影数量。"""
    yearly_counts = movie_data["movie_year"].value_counts().sort_index()
    min_year = int(movie_data["movie_year"].min())
    max_year = int(movie_data["movie_year"].max())
    years = list(range(min_year, max_year + 1))
    counts = [int(yearly_counts.get(year, 0)) for year in years]
    return years, counts


def count_movies_by_language(movie_data: pd.DataFrame) -> Tuple[list[str], list[int]]:
    """统计各电影语言的数量，并按数量降序排列。"""
    language_counts = movie_data["movie_lang"].value_counts()
    return language_counts.index.tolist(), language_counts.values.tolist()


def count_movies_by_type(movie_data: pd.DataFrame) -> Tuple[list[str], list[int]]:
    """统计各电影类型的数量。"""
    type_counts: dict[str, int] = {}
    for movie_types in movie_data["movie_type"].dropna():
        for movie_type in movie_types.split(","):
            type_counts[movie_type] = type_counts.get(movie_type, 0) + 1
    return list(type_counts), list(type_counts.values())


def count_movies_by_score(movie_data: pd.DataFrame) -> Tuple[list, list[int]]:
    """保留数量大于 10 的评分，其余评分合并为“其他”。"""
    score_counts = movie_data["movie_scores"].value_counts()
    large_scores = score_counts[score_counts > 10].copy()
    small_scores = score_counts[score_counts <= 10]
    if not small_scores.empty:
        large_scores.loc["其他"] = small_scores.sum()
    return large_scores.index.tolist(), large_scores.values.tolist()


def plot_year_counts(ax: Axes, years: list[int], counts: list[int]) -> None:
    """绘制不同年份电影数量折线图。"""
    ax.plot(years, counts, color="purple")
    ax.set_xticks(years[::10])
    ax.grid(alpha=0.3, linestyle=":")
    ax.set_xlabel("年份")
    ax.set_ylabel("数量")
    ax.set_title("年份-数量折线图")
    ax.xaxis.set_label_coords(1.01, -0.04)


def plot_language_counts(ax: Axes, languages: list[str], counts: list[int]) -> None:
    """绘制电影语言数量柱状图。"""
    ax.bar(languages, counts, color="pink")
    ax.tick_params(rotation=-90)
    ax.set_title("语言-数量柱状图")
    ax.set_xlabel("语言")
    ax.set_ylabel("数量")
    ax.xaxis.set_label_coords(1.01, -0.04)


def plot_type_counts(ax: Axes, movie_types: list[str], counts: list[int]) -> None:
    """绘制电影类型数量柱状图。"""
    ax.bar(movie_types, counts, color="plum")
    ax.tick_params(rotation=-90)
    ax.set_title("类型-数量柱状图")
    ax.set_xlabel("类型")
    ax.set_ylabel("数量")
    ax.xaxis.set_label_coords(1.01, -0.04)


def plot_score_counts(ax: Axes, scores: list, counts: list[int]) -> None:
    """绘制电影评分饼状图。"""
    ax.pie(counts)
    ax.legend(
        ncols=4,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.25),
        labels=scores,
    )
    ax.set_title("电影评分饼状图")


def create_movie_visualization(
    data_path: Path = DEFAULT_DATA_PATH,
) -> Tuple[plt.Figure, list[Axes]]:
    """创建电影数据可视化图表并返回图形和坐标轴。"""
    movie_data = load_movie_data(data_path)
    figure, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
    year_ax, language_ax, type_ax, score_ax = axes.flat

    plt.rcParams["font.sans-serif"] = ["SimHei"]
    figure.suptitle("TMTD-TOP300", fontsize=30)
    figure.subplots_adjust(hspace=0.6)

    plot_year_counts(year_ax, *count_movies_by_year(movie_data))
    plot_language_counts(language_ax, *count_movies_by_language(movie_data))
    plot_type_counts(type_ax, *count_movies_by_type(movie_data))
    plot_score_counts(score_ax, *count_movies_by_score(movie_data))
    return figure, [year_ax, language_ax, type_ax, score_ax]


def main() -> None:
    """生成并显示电影可视化图表。"""
    create_movie_visualization()
    plt.show()


if __name__ == "__main__":
    main()
