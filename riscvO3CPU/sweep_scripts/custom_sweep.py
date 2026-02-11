import subprocess
import os
import csv
import warnings

warnings.filterwarnings("ignore")


GEM5 = "../../../gem5/build/RISCV/gem5.opt"
CONFIG = "../configs/cache_config_riscvO3CPU.py"
BINARY = "../../benchmarks/matrix_multiply_"
OUTPUT_DIR = "../results/single_param_sweep"

L1D_SIZES = ["16kB", "32kB", "64kB"]
MATRIX_SIZES  = ["64","128","256"]

os.makedirs(OUTPUT_DIR, exist_ok=True)
for matrixsize in MATRIX_SIZES:
    RESULTS = []
    for size in L1D_SIZES:
        outdir = f"{OUTPUT_DIR}/MATRIX_{matrixsize}/l1d_{size}"
        os.makedirs(outdir, exist_ok=True)

        print(f"\nRunning simulation for L1D size = {size} and matrix size {matrixsize} binary file ")
        BINARY_TYPE = f"{BINARY}{matrixsize}"
        cmd = [
            GEM5,
            "-q",
            "-d",
            outdir,
            CONFIG,
            f"--binary={BINARY_TYPE}",
            "--l1i_size=16kB",
            f"--l1d_size={size}",
            "--l2_size=256kB",
            "--l1_assoc=4",
            "--l2_assoc=8",
        ]

        subprocess.run(cmd,check=True)

        # Parse stats.txt
        stats_file = os.path.join(outdir, "stats.txt")

        exec_ticks = None
        l1d_hits = None
        l1d_accesses = None

        with open(stats_file) as f:
            for line in f:
                if "simTicks" in line:
                    exec_ticks = int(line.split()[1])
                if "system.cpu.dcache.overallHits::total" in line:
                    l1d_hits = int(line.split()[1])
                if "system.cpu.dcache.overallAccesses::total" in line:
                    l1d_accesses = int(line.split()[1])

        hit_rate = (l1d_hits / l1d_accesses) if l1d_accesses else 0

        RESULTS.append([size, exec_ticks, hit_rate])
    # Save CSV
    csv_path = f"{OUTPUT_DIR}/MATRIX_{matrixsize}/results.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["L1D_Size", "Execution_Ticks", "L1D_Hit_Rate"])
        writer.writerows(RESULTS)
    print(f"matrix of size {matrixsize} is simulated with varying l1D sizes")


print("\nSweep complete!")
print(f"Results saved")