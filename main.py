import os
import platform
import sys
import subprocess

from files_generation import generate_files
from crypto import generate_rsa_keypair
from benchmark import (
    run_aes_benchmark,
    run_aes_variability_benchmark,
    run_rsa_benchmark,
    run_sha_benchmark,
)
from plot import plot_results

def _get_total_ram():
    """Deteta a RAM total do sistema (funciona em Linux e macOS)."""
    if os.path.exists("/proc/meminfo"):
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        kb = int(line.split()[1])
                        return f"{kb / (1024 * 1024):.2f} GB"
        except Exception:
            pass
    try:
        if platform.system() == "Darwin":
            out = subprocess.check_output(
                ["sysctl", "-n", "hw.memsize"], text=True
            ).strip()
            return f"{int(out) / (1024 ** 3):.2f} GB"
    except Exception:
        pass
    return "Unknown"


def _get_cpu_model():
    """Deteta o modelo do CPU (funciona em Linux e macOS)."""
    if os.path.exists("/proc/cpuinfo"):
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass
    return platform.processor() or "Unknown"


def print_experimental_setup():
    """Imprime informação sobre o ambiente de execução (requisito do enunciado)."""
    try:
        import cryptography
        crypto_ver = cryptography.__version__
    except Exception:
        crypto_ver = "Unknown"
    try:
        import numpy
        numpy_ver = numpy.__version__
    except Exception:
        numpy_ver = "Unknown"
    try:
        import matplotlib
        mpl_ver = matplotlib.__version__
    except Exception:
        mpl_ver = "Unknown"

    print("=" * 55)
    print("           EXPERIMENTAL SETUP")
    print("=" * 55)
    print(f"  Python version      : {sys.version.split()[0]}")
    print(f"  Operating system    : {platform.system()} {platform.release()}")
    print(f"  OS version          : {platform.version()}")
    print(f"  Architecture        : {platform.machine()}")
    print(f"  CPU model           : {_get_cpu_model()}")
    print(f"  CPU cores (logical) : {os.cpu_count()}")
    print(f"  Total RAM           : {_get_total_ram()}")
    print(f"  cryptography lib    : {crypto_ver}")
    print(f"  numpy lib           : {numpy_ver}")
    print(f"  matplotlib lib      : {mpl_ver}")
    print("=" * 55)

def main():
    print_experimental_setup()

    generate_files()

    print("\n[B] AES-CTR benchmarks")
    aes_results = run_aes_benchmark()

    print("\n[B extra] AES variability analysis")
    aes_var_results = run_aes_variability_benchmark()

    print("\n[C]")
    e, d, n = generate_rsa_keypair(2048)
    rsa_results = run_rsa_benchmark(e, d, n)

    print("\n[D] SHA-256 benchmarks")
    sha_results = run_sha_benchmark()

    plot_results(aes_results, rsa_results, sha_results)

    print("\n" + "=" * 55)
    print("  AES VARIABILITY ANALYSIS (Point B)")
    print("=" * 55)
    for r in aes_var_results:
        print(
            f"  Size {r['size']:>7d} B | same-file: {r['same_mean']:8.2f} us "
            f"(CI: +/-{r['same_ci']:.2f}) | random-files: {r['random_mean']:8.2f} us "
            f"(CI: +/-{r['random_ci']:.2f})"
        )
        
if __name__ == "__main__":
    main()
