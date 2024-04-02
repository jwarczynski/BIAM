to_plot_df = df[['Instance', 'Algorithm', 'Evaluations']]
to_plot_df = to_plot_df.query("Algorithm in ['Greedy', 'Steepest', 'RandomSearch', 'RandomWalk']")
to_plot_df = to_plot_df.query("Instance in ['chr12a', 'chr15a', 'chr18a', 'chr20a', 'chr22a', 'chr25a']")
to_plot_df = to_plot_df.pivot_table(index='Instance', columns='Algorithm', values='Evaluations', aggfunc=list)
to_plot_df = to_plot_df.reset_index()
to_plot_df = to_plot_df.explode('Greedy').explode('Steepest').explode('RandomSearch').explode('RandomWalk')
to_plot_df.reset_index(drop=True, inplace=True)
to_plot_df
to_plot_dd = pd.melt(to_plot_df, id_vars="Instance", value_vars=['Greedy', 'Steepest', 'RandomSearch', 'RandomWalk'], var_name='Algorithm', value_name='Evaluations')
to_plot_dd
sns.boxplot(x='Instance', y='Evaluations', data=to_plot_dd, hue='Algorithm')