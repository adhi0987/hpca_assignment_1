from m5.objects import *
import m5
import argparse
import os

# -----------------------------
# warning remover
# -----------------------------
# m5.util.disableAllWarnings() 
# -----------------------------
# Arguments
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--binary", type=str, required=True)

parser.add_argument("--l1i_size", type=str, default="16kB")
parser.add_argument("--l1d_size", type=str, default="16kB")
parser.add_argument("--l2_size", type=str, default="256kB")

parser.add_argument("--l1_assoc", type=int, default=4)
parser.add_argument("--l2_assoc", type=int, default=8)

args = parser.parse_args()

binary = os.path.abspath(args.binary)

# -----------------------------
# System
# -----------------------------
system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

# -----------------------------
# CPU
# -----------------------------
system.cpu = RiscvTimingSimpleCPU()
system.cpu.createInterruptController()

# -----------------------------
# L1 Instruction Cache
# -----------------------------
system.cpu.icache = Cache(
    size=args.l1i_size,
    assoc=args.l1_assoc,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=20
)

# -----------------------------
# L1 Data Cache
# -----------------------------
system.cpu.dcache = Cache(
    size=args.l1d_size,
    assoc=args.l1_assoc,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=20
)

# -----------------------------
# L2 Cache
# -----------------------------
system.l2cache = Cache(
    size=args.l2_size,
    assoc=args.l2_assoc,
    tag_latency=20,
    data_latency=20,
    response_latency=20,
    mshrs=16,
    tgts_per_mshr=20
)

# -----------------------------
# Buses
# -----------------------------
system.l2bus = L2XBar()
system.membus = SystemXBar()

# -----------------------------
# Cache Connections (CORRECT for gem5 v23)
# -----------------------------
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port

system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

system.l2cache.cpu_side = system.l2bus.mem_side_ports
system.l2cache.mem_side = system.membus.cpu_side_ports

system.system_port = system.membus.cpu_side_ports

# -----------------------------
# Memory Controller
# -----------------------------
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# -----------------------------
# Workload 
# -----------------------------
process = Process()
process.cmd = [binary]

system.workload = SEWorkload.init_compatible(binary)
system.cpu.workload = process
system.cpu.createThreads()

# -----------------------------
# Root
# -----------------------------
root = Root(full_system=False, system=system)
m5.instantiate()

print("Starting simulation")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")