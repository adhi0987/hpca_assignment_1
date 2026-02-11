import subprocess
import json
import os

GEM5 = "../../gem5/build/RISCV/gem5.opt"
CONFIG = "../configs/cache_config.py"
BINARY = "../benchmarks/matrix_multiply"

OUTDIR = "../results/full_sweep_results"
os.makedirs(OUTDIR, exist_ok=True)

L1D_SIZES = ["16kB", "32kB", "64kB"]
L2_SIZES = ["128kB", "256kB", "512kB", "1MB"]
L1_ASSOCS = [2, 4, 8]
L2_ASSOCS = [4, 8, 16]

results = []

run_id = 0

for l1d in L1D_SIZES:
    for l2 in L2_SIZES:
        for l1a in L1_ASSOCS:
            for l2a in L2_ASSOCS:
                run_id += 1
                run_dir = f"{OUTDIR}/run_{run_id}"
                os.makedirs(run_dir, exist_ok=True)

                print(f"\nRun {run_id}: L1D={l1d}, L2={l2}, L1A={l1a}, L2A={l2a}")

                cmd = [
                    GEM5,
                    "-d", run_dir,
                    CONFIG,
                    f"--binary={BINARY}",
                    "--l1i_size=16kB",
                    f"--l1d_size={l1d}",
                    f"--l2_size={l2}",
                    f"--l1_assoc={l1a}",
                    f"--l2_assoc={l2a}",
                ]

                subprocess.run(cmd, check=True)

                stats_file = os.path.join(run_dir, "stats.txt")

                sim_ticks = None
                l1_hits = l1_accesses = None
                l2_hits = l2_accesses = None

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
                    "L1D_size": l1d,
                    "L2_size": l2,
                    "L1_assoc": l1a,
                    "L2_assoc": l2a,
                    "simTicks": sim_ticks,
                    "L1D_hit_rate": l1_hits / l1_accesses if l1_accesses else 0,
                    "L2_hit_rate": l2_hits / l2_accesses if l2_accesses else 0
                })

with open(f"{OUTDIR}/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nFull sweep complete!")