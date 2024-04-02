def quality_time_efficiency_box_plots(df, axes, limits=None,  hide_titles=True):
    ax1, ax2, ax3 = axes
    min_time = df['Time'].min()
    max_time = df['Time'].max()
    df.loc[:, 'Efficiency'] = df['Quality'] / (1 + (df['Time'] - min_time) / (max_time - min_time))

    time_boxplot = df.boxplot(ax=ax1, column='Time', by='AlgShortName')
    time_boxplot.set_title("Time (ms)")

    quality_boxplot = df.boxplot(ax=ax2, column='Quality', by='AlgShortName')
    quality_boxplot.set_title("Quality")

    efficiency_boxplot = df.boxplot(ax=ax3, column='Efficiency', by='AlgShortName')
    efficiency_boxplot.set_title("Efficiency")

    for ax in axes:
        ax.set_xlabel(None)
        ax.set_ylabel(None)
        if hide_titles:
            ax.set_title(None)

    if limits is not None:
        ax1.set_ylim(limits[0])
        ax2.set_ylim(limits[1])
        ax3.set_ylim(limits[2])

    '''
    Example usage:
    
    features = ['Time', 'Quality', 'Efficiency']
    limits = [(0, 3), (0, 1), (0, 1)]
    fig, axs = plt.subplots(3, 5, figsize=(20, len(features) * 5))
    
    for i, (feature, limit) in enumerate(zip(features, limits)):
        all_alg_feature_box_plot(axs[i], df, feature, hide_titles=False if i==0 else True, y_limits=limit)
        axs[i, 0].set_ylabel(feature, rotation=90, ha='right', fontsize='large', fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    '''


def box_plot(ax, x, xticklabels, title=None, y_limits=None, xtick_rotation=45):
    ax.boxplot(x)
    ax.set_xticklabels(xticklabels, rotation=xtick_rotation)
    ax.set_title(title)
    ax.set_ylim(y_limits)

    '''
    Example usage:
    
    fig, ax = plt.subplots(figsize=(15, 5))
    box_plot(ax, df['Time'], df['AlgShortName'].unique(), title="Time (ms)")
    plt.show()
    '''


def all_alg_feature_box_plot(axs, df, feature, hide_titles=True, y_limits=None):
    algs = df['Algorithm'].unique()
    ticks = df['Instance'].unique().tolist()
    for i, alg in enumerate(algs):
        x = df.query("Algorithm == @alg").groupby('Instance')[feature].apply(list).to_list()
        box_plot(axs[i], x, ticks, title=None if hide_titles else alg, y_limits=y_limits)

    '''
    Example usage:
    
    fig, axs = plt.subplots(1, 5, figsize=(15, 5))
    all_alg_feature_box_plot(axs, df, 'Time', hide_titles=False)
    plt.show()
    '''
