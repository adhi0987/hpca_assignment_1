import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- PATH CONFIGURATION ---
# Update these paths to match your local folder structure.
# If your folders are inside a sub-directory, add it here.
# Example: 'hpca_assignment_1-687ad940.../riscvO3CPU/...'
o3_csv_path = 'riscvO3CPU/results/single_param_sweep/MATRIX_64/results.csv'
timing_csv_path = 'riscvTimingSimpleCPU/results/single_param_sweep/MATRIX_64/results.csv'

def generate_plots(o3_path, timing_path):
    # Check if files exist
    if not os.path.exists(o3_path) or not os.path.exists(timing_path):
        print(f"Error: Could not find one of the CSV files.")
        print(f"Looking for: {os.path.abspath(o3_path)}")
        print(f"Looking for: {os.path.abspath(timing_path)}")
        print("\nPlease check your folder names and update the paths in the script.")
        return

    # Load data
    df_o3 = pd.read_csv(o3_path)
    df_timing = pd.read_csv(timing_path)

    l1_sizes = df_o3['L1D_Size'].tolist()
    x = np.arange(len(l1_sizes))
    width = 0.35

    # --- Plot 1: Execution Ticks (Performance) ---
    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, df_o3['Execution_Ticks'], width, label='O3CPU', color='skyblue')
    plt.bar(x + width/2, df_timing['Execution_Ticks'], width, label='TimingSimpleCPU', color='salmon')
    
    plt.xlabel('L1 Data Cache Size')
    plt.ylabel('Execution Ticks (Log Scale)')
    plt.title('CPU Performance: Execution Ticks Comparison')
    plt.xticks(x, l1_sizes)
    plt.yscale('log') # Log scale because TimingSimpleCPU is ~10x slower
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save the performance plot
    plt.savefig('performance_comparison.png')
    print("Saved performance_comparison.png")

    # --- Plot 2: L1D Hit Rate (Cache Efficiency) ---
    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, df_o3['L1D_Hit_Rate'], width, label='O3CPU', color='skyblue')
    plt.bar(x + width/2, df_timing['L1D_Hit_Rate'], width, label='TimingSimpleCPU', color='salmon')
    
    plt.xlabel('L1 Data Cache Size')
    plt.ylabel('L1D Hit Rate')
    plt.title('Cache Efficiency: L1D Hit Rate Comparison')
    plt.xticks(x, l1_sizes)
    plt.ylim(0, 1.1)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save the cache plot
    plt.savefig('cache_hit_rate_comparison.png')
    print("Saved cache_hit_rate_comparison.png")

if __name__ == "__main__":
    generate_plots(o3_csv_path, timing_csv_path)