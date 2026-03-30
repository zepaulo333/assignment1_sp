import os
import platform
import sys
import subprocess

from files_generation import generate_files
from crypto import generate_rsa_keypair
from benchmark import run_aes_benchmark, run_aes_variability_benchmark, run_rsa_benchmark, run_sha_benchmark
from plot import plot_results


def _get_total_ram():
    # Linux preferred path
    if os.path.exists("/proc/meminfo"):
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        kb = int(line.split()[1])
                        gb = kb / (1024 * 1024)
                        return f"{gb:.2f} GB"
        except Exception:
            pass

    # Fallback for other systems (if available)
    try:
        if platform.system() == "Darwin":
            out = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip()
            gb = int(out) / (1024 ** 3)
            return f"{gb:.2f} GB"
    except Exception:
        pass

    return "Unknown"


def _get_cpu_model():
    # Linux preferred path
    if os.path.exists("/proc/cpuinfo"):
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass

    # Generic fallback
    return platform.processor() or "Unknown"


def _print_experimental_setup():
    try:
        import cryptography
        cryptography_version = cryptography.__version__
    except Exception:
        cryptography_version = "Unknown"

    try:
        import numpy as np
        numpy_version = np.__version__
    except Exception:
        numpy_version = "Unknown"

    try:
        import matplotlib
        matplotlib_version = matplotlib.__version__
    except Exception:
        matplotlib_version = "Unknown"

    print("\n=== Experimental Setup (Assignment Requirement) ===")
    print(f"Python version      : {sys.version.split()[0]}")
    print(f"Operating system    : {platform.system()} {platform.release()}")
    print(f"OS version/detail   : {platform.version()}")
    print(f"Machine architecture: {platform.machine()}")
    print(f"CPU model           : {_get_cpu_model()}")
    print(f"CPU cores (logical) : {os.cpu_count()}")
    print(f"Total RAM           : {_get_total_ram()}")
    print(f"cryptography ver.   : {cryptography_version}")
    print(f"numpy ver.          : {numpy_version}")
    print(f"matplotlib ver.     : {matplotlib_version}")
    print("===============================================\n")


def main():
    _print_experimental_setup()
    generate_files()

    aes_results = run_aes_benchmark()
    aes_variability_results = run_aes_variability_benchmark()

    e, d, n = generate_rsa_keypair(2048)
    rsa_results = run_rsa_benchmark(e, d, n)

    sha_results = run_sha_benchmark()

    plot_results(aes_results, rsa_results, sha_results)

    print("\n=== Assignment B extra analysis (same file vs random files, fixed size) ===")
    for r in aes_variability_results:
        print(
            f"Size {r['size']} B -> same-file mean: {r['same_mean']:.2f} µs (±{r['same_ci']:.2f}), "
            f"random-files mean: {r['random_mean']:.2f} µs (±{r['random_ci']:.2f})"
        )


if __name__ == "__main__":
    main()