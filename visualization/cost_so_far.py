import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


def construct_arrays(costs):
    smallest_so_far = np.zeros(len(costs))
    average_so_far = np.zeros(len(costs))

    smallest_num = float('inf')
    sum_so_far = 0

    for i, cost in enumerate(costs):
        smallest_num = min(smallest_num, cost)
        smallest_so_far[i] = smallest_num
        sum_so_far += cost
        average_so_far[i] = sum_so_far / (i + 1)

    return smallest_so_far, average_so_far

def cost_so_far_plot(ax, s_cost, g_cost, title, ylabel=None, xlabel=None):
    steepest_smallest_array, steepest_average_array = construct_arrays(s_cost)
    greedy_smallest_array, greedy_average_array = construct_arrays(g_cost)
    run_ids = np.arange(1, len(s_cost) + 1)

    ax.plot(run_ids, steepest_smallest_array, '--', label='Steepest smallest so far', markersize=2,
            c=mcolors.TABLEAU_COLORS['tab:orange'])
    ax.plot(run_ids, steepest_average_array, '-', label='Steepest average so far', c=mcolors.TABLEAU_COLORS['tab:orange'])
    ax.plot(run_ids, greedy_smallest_array, '--', label='Greedy smallest so far', markersize=2,
            c=mcolors.TABLEAU_COLORS['tab:blue'])
    ax.plot(run_ids, greedy_average_array, '-', label='Greedy average so far', c=mcolors.TABLEAU_COLORS['tab:blue'])

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def cost_so_far_m_instances(df):
    columns = df.Instance.nunique()
    fig, axes = plt.subplots(1, columns, figsize=(5 * columns, 4))
    for i, instance in enumerate(sorted(df.Instance.unique())):
        steepest_costs = df.query(f"Instance == '{instance}' and Algorithm == 'Steepest'")[
            'Cost'].to_numpy()
        greedy_costs = df.query(f"Instance == '{instance}' and Algorithm == 'Greedy'")[
            'Cost'].to_numpy()
        cost_so_far_plot(axes[i], steepest_costs, greedy_costs, instance)

    axes[0].set_ylabel("Cost")
    axes[1].set_xlabel("Run")

    lines, labels = axes[0].get_legend_handles_labels()
    lgd = fig.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncols=5)
    return fig, axes
