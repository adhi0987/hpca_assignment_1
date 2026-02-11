import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


csv_path = '../results/full_sweep_results/64/total_sweep_results.csv'
output_dir = '../results/full_sweep_analysis'


if not os.path.exists(output_dir):
    os.makedirs(output_dir)


df = pd.read_csv(csv_path)


# Metrics: simTicks (Performance), L1D Hit Rate, L2D Hit Rate
metrics = ['simTicks', 'L1D_hit_rate', 'L2D_hit_rate']
stats = df[metrics].agg(['mean', 'min', 'max']).transpose()
print("--- Summary Statistics ---")
print(stats)
stats.to_csv(os.path.join(output_dir, 'summary_statistics.csv'))

# 2. Plotting Impact of L1D and L2 Sizes on Performance (simTicks)
def create_impact_plot(param, title, filename):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=param, y='simTicks', data=df)
    plt.title(title)
    plt.xlabel(f'{param} (Bytes/KB)')
    plt.ylabel('Execution Time (simTicks)')
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

# L1D size impact
create_impact_plot('L1D_size', 'Impact of L1D Cache Size on Performance', 'l1d_size_impact.png')

# L2 size impact
create_impact_plot('L2D_size', 'Impact of L2 Cache Size on Performance', 'l2_size_impact.png')

# 3. Associativity Impact Analysis
plt.figure(figsize=(10, 6))
sns.pointplot(x='L1_assoc', y='simTicks', data=df, label='L1 Associativity')
sns.pointplot(x='L2_assoc', y='simTicks', data=df, color='orange', label='L2 Associativity')
plt.title('Impact of Cache Associativity on Performance')
plt.xlabel('Associativity')
plt.ylabel('Average simTicks')
plt.legend()
plt.savefig(os.path.join(output_dir, 'associativity_impact.png'))
plt.close()

print(f"\nAnalysis complete. Statistics and plots saved to: {output_dir}")