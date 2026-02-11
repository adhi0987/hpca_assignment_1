import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to the results file provided in your directory
csv_file = '../results/single_param_sweep/MATRIX_256/results.csv'

# Load data
df = pd.read_csv(csv_file)

# Plot 1: L1D Size vs Execution Time (Ticks)
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(df['L1D_Size'], df['Execution_Ticks'], marker='o', color='b', linestyle='-')
plt.title('L1D Size vs Execution Time')
plt.xlabel('L1D Cache Size')
plt.ylabel('Execution Time (Ticks)')
plt.grid(True)

# Plot 2: L1D Size vs Hit Rate
plt.subplot(1, 2, 2)
plt.plot(df['L1D_Size'], df['L1D_Hit_Rate'], marker='s', color='r', linestyle='-')
plt.title('L1D Size vs Hit Rate')
plt.xlabel('L1D Cache Size')
plt.ylabel('Hit Rate')
plt.grid(True)

plt.tight_layout()
plt.savefig('l1d_performance_analysis.png')
plt.show()

print("Analysis plots saved as 'l1d_performance_analysis.png'")