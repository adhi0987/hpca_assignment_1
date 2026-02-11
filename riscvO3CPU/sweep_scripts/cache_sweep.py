import subprocess
import os
import csv

GEM5 = "../../gem5/build/RISCV/gem5.opt"
CONFIG = "../configs/cache_config.py"
BINARY_BASE = "../benchmarks/matrix_multiply_" # Assuming binary name ends with size

OUTDIR = "../results/full_sweep_results"
os.makedirs(OUTDIR, exist_ok=True)

L1D_SIZES = ["16kB", "32kB", "64kB"]
L2_SIZES = ["128kB", "256kB", "512kB", "1MB"]
L1_ASSOCS = [2, 4, 8]
L2_ASSOCS = [4, 8, 16]
MATRIX_SIZES = ["64", "128", "256"]

run_id = 0
for matrixsize in MATRIX_SIZES:
    results = []
    # Create a subfolder for the specific matrix size results
    matrix_outdir = os.path.join(OUTDIR, matrixsize)
    os.makedirs(matrix_outdir, exist_ok=True)
    
    # Update binary path based on current matrix size if necessary
    current_binary = f"{BINARY_BASE}{matrixsize}"

    for l1d in L1D_SIZES:
        for l2 in L2_SIZES:
            for l1a in L1_ASSOCS:
                for l2a in L2_ASSOCS:
                    run_id += 1
                    run_dir = os.path.join(matrix_outdir, f"run_{run_id}")
                    os.makedirs(run_dir, exist_ok=True)

                    print(f"\nMatrix {matrixsize} - Run {run_id}: L1D={l1d}, L2={l2}, L1A={l1a}, L2A={l2a}")

                    cmd = [
                        GEM5,
                        "-d", run_dir,
                        CONFIG,
                        f"--binary={current_binary}",
                        "--l1i_size=16kB",
                        f"--l1d_size={l1d}",
                        f"--l2_size={l2}",
                        f"--l1_assoc={l1a}",
                        f"--l2_assoc={l2a}",
                    ]

                    try:
                        subprocess.run(cmd, check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Error running gem5: {e}")
                        continue

                    stats_file = os.path.join(run_dir, "stats.txt")
                    sim_ticks = None
                    l1_hits = l1_accesses = 0
                    l2_hits = l2_accesses = 0

                    # Parse stats.txt
                    if os.path.exists(stats_file):
                        with open(stats_file) as f:
                            for line in f:
                                if "simTicks" in line:
                                    sim_ticks = int(line.split()[1])
                                if "system.cpu.dcache.overallHits::total" in line:
                                    l1_hits = int(line.split()[1])
                                if "system.cpu.dcache.overallAccesses::total" in line:
                                    l1_accesses = int(line.split()[1])
                                if "system.l2cache.overallHits::total" in line:
                                    l2_hits = int(line.split()[1])
                                if "system.l2cache.overallAccesses::total" in line:
                                    l2_accesses = int(line.split()[1])

                        results.append({
                            "M_Size": matrixsize,
                            "L1D_size": l1d,
                            "L2D_size": l2,
                            "L1_assoc": l1a,
                            "L2_assoc": l2a,
                            "simTicks": sim_ticks,
                            "L1D_hit_rate": l1_hits / l1_accesses if l1_accesses else 0,
                            "L2D_hit_rate": l2_hits / l2_accesses if l2_accesses else 0
                        })

    # Write results for this matrix size to CSV
    csv_file = os.path.join(matrix_outdir, "total_sweep_results.csv")
    with open(csv_file, "w", newline="") as f:
        fieldnames = ["M_Size", "L1D_size", "L2D_size", "L1_assoc", "L2_assoc", "simTicks", "L1D_hit_rate", "L2D_hit_rate"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

print("\nFull sweep complete!")