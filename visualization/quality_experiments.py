import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def get_corr(df, instance, algorithm, features=("Quality", "InitialQuality")):
    return \
    df.query(f"Instance == '{instance}' and Algorithm == '{algorithm}'")[[features[0], features[1]]].corr().loc[
        features[0], features[1]]


def create_corr_df(df, features=("Quality", "InitialQuality")):
    instances = sorted(df.Instance.unique())
    algs = sorted(df.Algorithm.unique())
    corr_df = pd.DataFrame(index=instances, columns=algs, dtype=float)
    for instance in instances:
        for alg in algs:
            corr_df.loc[instance, alg] = get_corr(df, instance, alg, features)
    return corr_df


def quality_scatter(ax, x, y, title, xlabel, ylabel):
    ax.scatter(x, y, s=5, alpha=0.5)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def initial_quality_to_quality_scatter(df):
    instances = sorted(df.Instance.unique())
    algs = sorted(df.Algorithm.unique())
    fig, axes = plt.subplots(len(instances), len(algs), figsize=(4 * len(algs), 2 * len(instances)))
    for i, instance in enumerate(instances):
        for j, alg in enumerate(algs):
            df.query("Instance == @instance and Algorithm == @alg").plot(kind='scatter', x="InitialQuality",
                                                                         y="Quality", ax=axes[i, j],
                                                                         title=f"{alg}" if i == 0 else None,
                                                                         ylabel="Quality" if j == 1 else instances[i],
                                                                         s=5, alpha=0.5)

    for i in range(len(instances)):
        axes[i, 0].set_ylabel(instances[i], rotation=0, ha='right', fontsize='large', fontweight='bold')

    plt.tight_layout()
    plt.show()


def plots_with_correlation_heatmap(df, features=("InitialQuality", "Quality")):
    # plt.figure(figsize=(10, 6))
    rows = df.Instance.unique().size
    axes = []
    for i in range(rows * 2):
        axes.append(plt.subplot2grid((rows, 3), (i // 2, i % 2), ))
    ax7 = plt.subplot2grid((rows, 3), (0, 2), rowspan=rows)
    alg_axes_mapping = {'Greedy': axes[::2], 'Steepest': axes[1::2]}
    for alg, alg_axes in alg_axes_mapping.items():
        for ax, instance in zip(alg_axes, sorted(df.Instance.unique())):
            x = df.query(f"Instance == '{instance}' and Algorithm == '{alg}'")[features[0]]
            y = df.query(f"Instance == '{instance}' and Algorithm == '{alg}'")[features[1]]
            quality_scatter(ax, x, y, None, None, "Quality")
    corr_df = create_corr_df(df, features=features)
    sns.heatmap(corr_df, annot=True, ax=ax7, )
    for ax, instance in zip(axes[::2], sorted(df.Instance.unique())):
        ax.set_ylabel(instance, rotation=0, ha='right', fontsize='large', fontweight='bold')
    axes[0].set_title("Greedy")
    axes[1].set_title("Steepest")
    axes[-2].set_xlabel(features[0])
    axes[-1].set_xlabel(features[0])
    # plt.tight_layout()
    # plt.show()
    axes.append(ax7)
    return axes

